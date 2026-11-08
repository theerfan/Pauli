#!/usr/bin/env python3
"""Turn a Computer Modern PDF (dvips output) into Markdown with LaTeX math.

The EE 261 course reader was distilled from book.dvi. Its text layer still
has the CM fonts and the position of every glyph, but not the TeX source.
Plain extraction prints a sum as the letter X and glues c_n e^{2\\pi i n t}
into cne2πint. This script rebuilds scripts, fractions, radicals and large
operators from those positions, one chapter per Markdown file.

    python pdf_to_markdown.py book-fall-07.pdf -o ../library/ee261
    python pdf_to_markdown.py book-fall-07.pdf --pages 17-18 -o /tmp/sample

Requires PyMuPDF (see requirements.txt).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import pymupdf

_CMEX = {
    0x50: r"\sum",
    0x58: r"\sum",
    0x51: r"\prod",
    0x59: r"\prod",
    0x52: r"\int",
    0x5A: r"\int",
    0x48: r"\oint",
    0x49: r"\oint",
    0x53: r"\bigcup",
    0x5B: r"\bigcup",
    0x54: r"\bigcap",
    0x5C: r"\bigcap",
    0x55: r"\biguplus",
    0x5D: r"\biguplus",
    0x56: r"\bigwedge",
    0x5E: r"\bigwedge",
    0x57: r"\bigvee",
    0x5F: r"\bigvee",
    0x4E: r"\bigotimes",
    0x4F: r"\bigotimes",
    0x4C: r"\bigoplus",
    0x4D: r"\bigoplus",
    0x4A: r"\bigodot",
    0x4B: r"\bigodot",
    0x46: r"\bigsqcup",
    0x47: r"\bigsqcup",
    0x60: r"\coprod",
    0x61: r"\coprod",
    0x62: r"\widehat",
    0x63: r"\widehat",
    0x65: r"\widetilde",
    0x66: r"\widetilde",
    0x70: r"\sqrt",
    0x71: r"\sqrt",
    0x72: r"\sqrt",
    0x73: r"\sqrt",
}

_DELIM = {}
for _codes, _tok in (
    ({0x00, 0x10, 0x12, 0x20, 0x28, 0xF8EB, 0xF8EC, 0xF8ED}, "("),
    ({0x01, 0x11, 0x13, 0x21, 0x29, 0xF8F6, 0xF8F7, 0xF8F8}, ")"),
    ({0x02, 0x68, 0x14}, "["),
    ({0x03, 0x69, 0x15}, "]"),
    ({0xF8F1, 0xF8F2}, r"\{"),
    ({0xF8F3, 0xF8F4}, r"\}"),
    ({0x0A, 0x44, 0x1C}, r"\langle"),
    ({0x0B, 0x45, 0x1D}, r"\rangle"),
    ({0x0C}, "|"),
    ({0x0D}, r"\|"),
):
    for _code in _codes:
        _DELIM[_code] = _tok

_BIG = {
    r"\sum",
    r"\prod",
    r"\int",
    r"\oint",
    r"\bigcup",
    r"\bigcap",
    r"\biguplus",
    r"\bigwedge",
    r"\bigvee",
    r"\bigotimes",
    r"\bigoplus",
    r"\bigodot",
    r"\bigsqcup",
    r"\coprod",
}
_NOT = {"=": r"\neq", "<": r"\nless", ">": r"\ngtr", "∈": r"\notin", "∼": r"\nsim", "≡": r"\not\equiv"}


@dataclass
class Glyph:
    x0: float
    y0: float
    x1: float
    y1: float
    size: float
    text: str
    kind: str  # text, math, space
    line: int = 0

    @property
    def w(self) -> float:
        return self.x1 - self.x0

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2


@dataclass
class Rule:
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def w(self) -> float:
        return self.x1 - self.x0

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2


def _family(font: str) -> str:
    name = font.upper()
    for prefix in ("CMEX", "CMSY", "CMMIB", "CMMI", "CMTI", "CMBX", "CMR", "CMSS"):
        if name.startswith(prefix):
            return prefix
    return "OTHER"


def _token(font: str, ch: str) -> tuple[str, str]:
    if ch.strip() == "":
        fam = _family(font)
        if fam in {"CMR", "CMTI", "CMBX", "CMSS", "OTHER"}:
            return "space", " "
        return "math", ""
    if ch == "•":
        return "text", "•"
    fam = _family(font)
    code = ord(ch) if len(ch) == 1 else None
    if fam == "CMEX" and code is not None:
        if code in _CMEX:
            return "math", _CMEX[code]
        if code in _DELIM:
            return "math", _DELIM[code]
        return "math", ch
    if fam == "CMSY":
        # Inline radicals are the CMSY glyph, which PyMuPDF already decoded as √.
        if ch == "√":
            return "math", r"\sqrt"
        if len(ch) == 1 and "A" <= ch <= "Z":
            return "math", rf"\mathcal{{{ch}}}"
        return "math", ch
    if fam == "CMMIB":
        return "math", rf"\mathbf{{{ch}}}"
    if fam == "CMMI":
        return "math", ch
    return "text", ch


def extract_page(page: pymupdf.Page) -> tuple[list[Glyph], list[Rule], list[pymupdf.Rect]]:
    glyphs: list[Glyph] = []
    raw = page.get_text("rawdict")
    line_id = 0
    for block in raw["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            line_id += 1
            for span in line["spans"]:
                size = float(span["size"])
                for ch in span["chars"]:
                    kind, text = _token(span["font"], ch["c"])
                    if kind == "math" and not text:
                        continue
                    x0, y0, x1, y1 = ch["bbox"]
                    glyphs.append(Glyph(x0, y0, x1, y1, size, text, kind, line_id))
    rules: list[Rule] = []
    for info in page.get_image_info():
        x0, y0, x1, y1 = info["bbox"]
        if (y1 - y0) <= 1.4 and (x1 - x0) >= 4:
            rules.append(Rule(x0, y0, x1, y1))
    strokes: list[pymupdf.Rect] = []
    for drawing in page.get_drawings():
        rect = pymupdf.Rect(drawing["rect"])
        if rect.height <= 1.4 and 4 <= rect.width < 260:
            rules.append(Rule(rect.x0, rect.y0, rect.x1, rect.y1))
            continue
        if rect.width > 8 and rect.height > 8:
            strokes.append(rect)
    return glyphs, _dedupe_rules(rules), _cluster(strokes)


def _dedupe_rules(rules: list[Rule]) -> list[Rule]:
    kept: list[Rule] = []
    for rule in rules:
        if any(abs(rule.cy - other.cy) < 0.8 and abs(rule.x0 - other.x0) < 1.5 and abs(rule.w - other.w) < 1.5 for other in kept):
            continue
        kept.append(rule)
    return kept


def _cluster(rects: list[pymupdf.Rect]) -> list[pymupdf.Rect]:
    if not rects:
        return []
    parent = list(range(len(rects)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    expanded = [pymupdf.Rect(r.x0 - 8, r.y0 - 8, r.x1 + 8, r.y1 + 8) for r in rects]
    for i in range(len(rects)):
        ri = find(i)
        for j in range(i + 1, len(rects)):
            if expanded[i].intersects(expanded[j]):
                parent[find(j)] = ri
    groups: dict[int, pymupdf.Rect] = {}
    for i, rect in enumerate(rects):
        root = find(i)
        groups[root] = rect if root not in groups else groups[root] | rect
    out = []
    for rect in groups.values():
        if rect.width >= 80 and rect.height >= 40:
            # Keep the pad inside the body. A larger pad swallows the header
            # and the first line under the figure.
            top = max(rect.y0 - 2, 48)
            out.append(pymupdf.Rect(rect.x0 - 4, top, rect.x1 + 6, rect.y1 + 5))
    return out


def _span(glyphs: list[Glyph]) -> tuple[float, float, float, float]:
    return (
        min(g.x0 for g in glyphs),
        min(g.y0 for g in glyphs),
        max(g.x1 for g in glyphs),
        max(g.y1 for g in glyphs),
    )


def _join(glyphs: list[Glyph]) -> str:
    """Glue glyphs in x-order. A real gap becomes a space; touching letters do not."""
    parts: list[str] = []
    prev: Glyph | None = None
    for g in sorted(glyphs, key=lambda g: (g.x0, g.y0)):
        if g.kind == "space" or not g.text:
            continue
        command_then_letter = bool(parts and re.search(r"\\[a-zA-Z]+$", parts[-1]) and g.text[:1].isalpha())
        letter_then_command = bool(parts and parts[-1][-1:].isalnum() and g.text.startswith("\\"))
        if prev is not None and (g.x0 - prev.x1 > 1.3 or command_then_letter or letter_then_command):
            parts.append(" ")
        parts.append(g.text)
        prev = g
    return "".join(parts)


def _replace(glyphs: list[Glyph], drop: set[int], made: Glyph) -> list[Glyph]:
    return [made] + [g for i, g in enumerate(glyphs) if i not in drop]


def _script_of_neighbor(g: Glyph, glyphs: list[Glyph]) -> bool:
    """A subscript on c_k sits beside the integral. It belongs to c, not the integral."""
    for other in glyphs:
        if other is g or other.size < 9 or other.kind == "space" or other.text in _BIG:
            continue
        if not any(ch.isalpha() for ch in other.text):
            continue
        # The right edge of a letter on another line can share an x with a
        # limit. A real script sits a few points off its own base.
        if abs(g.cy - other.cy) > 11:
            continue
        if other.x1 - 1 <= g.x0 <= other.x1 + 3.2 and (g.cy < other.cy - 0.8 or g.cy > other.cy + 1.2):
            return True
    return False


def _limit_side(op: Glyph, g: Glyph, glyphs: list[Glyph]) -> str | None:
    """Script-sized glyphs sitting on a large operator, not the formula beside it.

    CMEX reports a font size of about 10 even for a tall display sum, so the
    limit test cannot use op.size. Body text is 10.9pt; limits in this book
    are 8pt.
    """
    if g.size >= 9 or g.kind == "space" or g.text in _BIG or not g.text:
        return None
    if _script_of_neighbor(g, glyphs):
        return None
    if not (op.x0 - 16 <= g.cx <= op.x1 + 18):
        return None
    height = max(op.y1 - op.y0, 1)
    if g.y0 >= op.y0 - 12 and g.cy <= op.y0 + 0.55 * height:
        return "above"
    if op.y1 - 8 <= g.y0 <= op.y1 + 14 and g.cy >= op.cy:
        return "below"
    return None


def _grow(glyphs: list[Glyph], seeds: list[int], op: Glyph) -> list[int]:
    chosen = set(seeds)
    changed = True
    while changed:
        changed = False
        xs0 = min(glyphs[i].x0 for i in chosen)
        xs1 = max(glyphs[i].x1 for i in chosen)
        y0 = min(glyphs[i].y0 for i in chosen)
        for i, g in enumerate(glyphs):
            if i in chosen or g.kind == "space" or g.size >= 9:
                continue
            if abs(g.cx - op.cx) > 46 or abs(g.y0 - y0) > 2.8:
                continue
            gap_r = g.x0 - xs1
            gap_l = xs0 - g.x1
            if -1.5 <= gap_r <= 4.5 or -1.5 <= gap_l <= 4.5:
                chosen.add(i)
                changed = True
    return sorted(chosen, key=lambda i: glyphs[i].x0)


def bind_limits_safe(glyphs: list[Glyph]) -> list[Glyph]:
    """Attach each operator's limits once. The result keeps the operator's line."""
    pending = [i for i, g in enumerate(glyphs) if g.text in _BIG]
    consumed: set[int] = set()
    made: list[Glyph] = []
    for op_i in pending:
        if op_i in consumed:
            continue
        op = glyphs[op_i]
        above, below = [], []
        for i, g in enumerate(glyphs):
            if i in consumed or i == op_i:
                continue
            side = _limit_side(op, g, glyphs)
            if side == "above":
                above.append(i)
            elif side == "below":
                below.append(i)
        drop = {op_i}
        upper = lower = ""
        if above:
            above = [i for i in _grow(glyphs, above, op) if i not in consumed]
            upper = _join([glyphs[i] for i in above])
            drop.update(above)
        if below:
            below = [i for i in _grow(glyphs, below, op) if i not in consumed and i not in drop]
            lower = _join([glyphs[i] for i in below])
            drop.update(below)
        text = op.text
        if lower:
            text += "_{" + lower + "}"
        if upper:
            text += "^{" + upper + "}"
        made.append(Glyph(op.x0, op.y0, op.x1, op.y1, op.size, text, "math", op.line))
        consumed.update(drop)
    return made + [g for i, g in enumerate(glyphs) if i not in consumed]


def bind_overlays(glyphs: list[Glyph]) -> list[Glyph]:
    used = set()
    out: list[Glyph] = []
    for i, g in enumerate(glyphs):
        if i in used or g.text not in {"̸", "/", "∕"}:
            continue
        sx0, sx1 = g.x0 - 3, max(g.x1, g.x0 + 0.4) + 3
        for j, other in enumerate(glyphs):
            if i == j or j in used or other.text not in _NOT:
                continue
            ox = min(sx1, other.x1) - max(sx0, other.x0)
            oy = min(g.y1, other.y1) - max(g.y0, other.y0)
            if oy > 1 and (ox > 0.4 or other.x0 - 4 <= g.cx <= other.x1):
                used.add(i)
                used.add(j)
                out.append(Glyph(min(g.x0, other.x0), min(g.y0, other.y0), max(g.x1, other.x1), max(g.y1, other.y1), other.size, _NOT.get(other.text, rf"\not{{{other.text}}}"), "math", other.line))
                break
    return out + [g for i, g in enumerate(glyphs) if i not in used]


# Roman operator names. A following math argument is wrapped in parentheses.
# English words (cosine, single, detail) are a longer letter run, so they stay.
_FUNCS = {
    "arcsin", "arccos", "arctan",
    "sinh", "cosh", "tanh",
    "sin", "cos", "tan", "sec", "csc", "cot",
    "sinc", "log", "ln", "exp", "arg", "det",
}
_ARG_STOP = set("+−-=,;:?.!")


def _func_cmd(name: str) -> str:
    if name == "sinc":
        return r"\operatorname{sinc}"
    return "\\" + name


def _skip_space(line: list[Glyph], index: int) -> int:
    while index < len(line) and (line[index].kind == "space" or not line[index].text.strip()):
        index += 1
    return index


def _balanced(line: list[Glyph], index: int) -> tuple[list[Glyph], int]:
    """index points at an opening parenthesis. Return the group, including the fences."""
    group = [line[index]]
    depth = 1
    index += 1
    while index < len(line) and depth:
        g = line[index]
        if g.kind != "space" and g.text.strip():
            if g.text == "(":
                depth += 1
            elif g.text == ")":
                depth -= 1
            group.append(g)
        index += 1
        if depth == 0:
            break
    return group, index


def _argument(line: list[Glyph], index: int) -> tuple[list[Glyph], int]:
    """The math that follows an operator. Parentheses keep what is inside them."""
    index = _skip_space(line, index)
    if index >= len(line):
        return [], index
    if line[index].text == "(":
        return _balanced(line, index)
    group: list[Glyph] = []
    prev: Glyph | None = None
    while index < len(line):
        g = line[index]
        if g.kind == "space" or not g.text.strip():
            index += 1
            continue
        if prev is not None and g.x0 - prev.x1 > 8:
            break
        if g.kind == "text" and any(ch.isalpha() for ch in g.text):
            break
        # A math comma is the end of "cos 4πt,", not part of the argument.
        if group and g.text in ",;:":
            break
        if group and g.kind == "text" and g.text in _ARG_STOP:
            break
        if not group and g.kind == "text" and g.text in "+−-":
            group.append(g)
            prev = g
            index += 1
            continue
        if g.text == "(":
            nested, index = _balanced(line, index)
            group.extend(nested)
            prev = nested[-1]
            continue
        if g.text == ")":
            break
        group.append(g)
        prev = g
        index += 1
    return group, index


def _arg_is_math(group: list[Glyph]) -> bool:
    for g in group:
        if g.kind == "math" or g.text.startswith("\\") or g.text in "([":
            return True
        if re.fullmatch(r"[0-9.]", g.text or ""):
            return True
    return False


def _operators(line: list[Glyph]) -> list[Glyph]:
    """Turn a roman cos/sin plus its argument into \\cos(...), \\sin(...)."""
    line = sorted(line, key=lambda g: (g.x0, g.y0))
    out: list[Glyph] = []
    index = 0
    while index < len(line):
        g = line[index]
        if g.kind != "text" or len(g.text) != 1 or not g.text.isalpha():
            out.append(g)
            index += 1
            continue
        if index > 0:
            prev = line[index - 1]
            if prev.kind == "text" and prev.text[:1].isalpha() and g.x0 - prev.x1 <= 1.5:
                out.append(g)
                index += 1
                continue
        chars = [g.text]
        end = index + 1
        last = g
        while end < len(line):
            nxt = line[end]
            if not (nxt.kind == "text" and len(nxt.text) == 1 and nxt.text.isalpha()):
                break
            if nxt.x0 - last.x1 > 1.5 or abs(nxt.size - g.size) > 1.5:
                break
            chars.append(nxt.text)
            last = nxt
            end += 1
        name = "".join(chars)
        if name not in _FUNCS:
            out.append(g)
            index += 1
            continue
        cursor = end
        sup: list[Glyph] = []
        while cursor < len(line):
            nxt = line[cursor]
            if nxt.kind == "space" or not nxt.text.strip():
                cursor += 1
                continue
            if nxt.size <= g.size * 0.85 and nxt.cy < g.cy - 0.7 and nxt.x0 <= last.x1 + 14:
                sup.append(nxt)
                cursor += 1
                continue
            break
        arg, after = _argument(line, cursor)
        if not _arg_is_math(arg):
            out.append(g)
            index += 1
            continue
        body = _join(arg)
        if not body.startswith("("):
            body = "(" + body + ")"
        text = _func_cmd(name)
        if sup:
            text += "^{" + _join(sup) + "}"
        text += body
        x1 = arg[-1].x1
        out.append(Glyph(g.x0, g.y0, x1, max(g.y1, arg[-1].y1), g.size, text, "math", g.line))
        index = after
    return out


def _narrow_fraction(glyphs: list[Glyph], above: list[int], below: list[int]) -> bool:
    """A bar only a few points wide is a one-symbol fraction, such as 1/2 or 1/ν."""
    if not above or not below or len(above) + len(below) > 6:
        return False
    for i in above + below:
        g = glyphs[i]
        if g.size >= 11.5 or len(g.text) > 4:
            return False
    return True


def _baseline(glyphs: list[Glyph], ids: list[int]) -> tuple[float, float]:
    """Sit on the line that owns the radical or fraction, not on the line above it."""
    anchor = _line_anchor(glyphs, ids)
    hosts = [g for g in glyphs if g.line == anchor and g.kind != "space" and g.size >= 9.5 and g.text != r"\sqrt"]
    if hosts:
        ys = sorted(g.y0 for g in hosts)
        y0 = ys[len(ys) // 2]
        return y0, y0 + 11
    members = [glyphs[i] for i in ids if glyphs[i].text != r"\sqrt"]
    host = members[0] if members else glyphs[ids[0]]
    return host.y0, host.y1


def _line_anchor(glyphs: list[Glyph], ids: list[int]) -> int:
    """Put a rebuilt radical or fraction on the line that holds the rest of the formula."""
    lines = {glyphs[i].line for i in ids}
    if len(lines) == 1:
        return next(iter(lines))
    counts = {line: 0 for line in lines}
    for g in glyphs:
        if g.line in counts:
            counts[g.line] += 1
    return max(counts, key=lambda line: counts[line])


def bind_fractions(glyphs: list[Glyph], rules: list[Rule]) -> list[Glyph]:
    consumed: set[int] = set()
    made: list[Glyph] = []
    for rule in sorted(rules, key=lambda r: r.w):
        # Header rules are page-wide. Footnote rules are short and sit in the left margin.
        # A vinculum over a single digit is only about 5pt, and 1/2 is about 4pt.
        if rule.w < 3.2 or rule.w > 220 or rule.y0 < 50:
            continue
        if rule.x0 < 80 and rule.w < 30:
            continue
        above, below = [], []
        for i, g in enumerate(glyphs):
            if i in consumed or g.kind == "space":
                continue
            # A following letter can sit a point past the bar. Two points of slop pulls it in.
            if not (rule.x0 - 0.6 <= g.cx <= rule.x1 + 0.6):
                continue
            # A one-symbol bar sits under a digit or a math symbol, not under the next word.
            if rule.w < 7 and g.kind == "text" and any(ch.isalpha() for ch in g.text):
                continue
            # A short bar is a one-symbol fraction. The previous line is about 13pt away
            # and must not be read as its numerator.
            above_lim = 9 if rule.w < 7 else 16
            below_lim = 9 if rule.w < 7 else 18
            if rule.cy - above_lim <= g.cy < rule.cy - 0.4:
                above.append(i)
            elif rule.cy + 0.4 < g.cy <= rule.cy + below_lim:
                below.append(i)
        radical = None
        for i, g in enumerate(glyphs):
            if g.text == r"\sqrt" and i not in consumed and g.x1 >= rule.x0 - 4 and g.x0 <= rule.x0 + 12 and abs(g.cy - rule.cy) < 22:
                radical = i
                break
        if radical is not None and below:
            ids = below + [radical]
            body = _join(_operators([glyphs[i] for i in sorted(below, key=lambda k: glyphs[k].x0)]))
            box = [glyphs[i] for i in ids]
            x0, _, x1, _ = _span(box)
            y0, y1 = _baseline(glyphs, ids)
            made.append(Glyph(x0, y0, x1, y1, 10.9, r"\sqrt{" + body + "}", "math", _line_anchor(glyphs, ids)))
            consumed.update(ids)
            continue
        # A bar this short is a one-character fraction, not an overline.
        if rule.w < 7 and not _narrow_fraction(glyphs, above, below):
            continue
        if above and below:
            num = _join(_operators([glyphs[i] for i in sorted(above, key=lambda k: glyphs[k].x0)]))
            den = _join(_operators([glyphs[i] for i in sorted(below, key=lambda k: glyphs[k].x0)]))
            if not num or not den:
                continue
            if sum(ch.isalpha() for ch in num) > 24 or sum(ch.isalpha() for ch in den) > 24:
                continue
            box = [glyphs[i] for i in above + below]
            x0, _, x1, _ = _span(box)
            y0, y1 = _baseline(glyphs, above + below)
            made.append(Glyph(x0, y0, x1, y1, 10.9, r"\frac{" + num + "}{" + den + "}", "math", _line_anchor(glyphs, above + below)))
            consumed.update(above)
            consumed.update(below)
            continue
        if below and not above and rule.w < 120:
            body = _join(_operators([glyphs[i] for i in sorted(below, key=lambda k: glyphs[k].x0)]))
            if not body or sum(ch.isalpha() for ch in body) > 24:
                continue
            width = max(glyphs[i].x1 for i in below) - min(glyphs[i].x0 for i in below)
            if rule.w > width * 1.6 + 6:
                continue
            box = [glyphs[i] for i in below]
            x0, y0, x1, y1 = _span(box)
            made.append(Glyph(x0, y0, x1, y1, box[0].size, r"\overline{" + body + "}", "math", box[0].line))
            consumed.update(below)
    # Hats sit on the glyph beneath them.
    for i, g in enumerate(glyphs):
        if i in consumed or g.text not in {r"\widehat", r"\widetilde"}:
            continue
        covered = [j for j, o in enumerate(glyphs) if j not in consumed and j != i and min(g.x1, o.x1) - max(g.x0, o.x0) > 0 and o.cy > g.cy]
        if not covered:
            continue
        body = _join([glyphs[j] for j in sorted(covered, key=lambda k: glyphs[k].x0)])
        cmd = r"\hat" if len(covered) == 1 and len(glyphs[covered[0]].text) == 1 and "hat" in g.text else (r"\widehat" if "hat" in g.text else r"\widetilde")
        box = [g] + [glyphs[j] for j in covered]
        x0, y0, x1, y1 = _span(box)
        made.append(Glyph(x0, y0, x1, y1, glyphs[covered[0]].size, cmd + "{" + body + "}", "math", glyphs[covered[0]].line))
        consumed.add(i)
        consumed.update(covered)
    return made + [g for i, g in enumerate(glyphs) if i not in consumed]


def _columns(glyphs: list[Glyph], width: float) -> list[list[Glyph]]:
    """Split only when line starts form two columns, as in the index."""
    starts: dict[int, float] = {}
    for g in glyphs:
        if g.kind == "space":
            continue
        starts[g.line] = min(g.x0, starts.get(g.line, g.x0))
    xs = list(starts.values())
    # The index is two tight clusters of line starts. A displayed formula
    # also starts right of center, but those starts are spread across the page.
    right = [x for x in xs if x > width * 0.42]
    left = [x for x in xs if x < width * 0.22]
    if len(right) >= 8 and len(left) >= 8 and max(right) - min(right) < 70:
        split = min(right) - 8
        left_ids = {lid for lid, x in starts.items() if x < split}
        return [
            [g for g in glyphs if g.line in left_ids],
            [g for g in glyphs if g.line not in left_ids],
        ]
    return [glyphs]


def _is_prose(line: list[Glyph]) -> bool:
    return sum(1 for g in line if g.kind == "text" and g.text.isalpha()) >= 2


def _box_gap(a0: float, a1: float, b0: float, b1: float) -> float:
    if a1 < b0:
        return b0 - a1
    if b1 < a0:
        return a0 - b1
    return 0


def _baselines(glyphs: list[Glyph]) -> list[list[Glyph]]:
    """One PyMuPDF line stays one line. Merge only math pieces of one formula.

    A sum, its limits and the terms beside it come out of dvips as separate
    lines whose boxes overlap. Two stacked equations, and every line of prose,
    stay apart so a later x-sort cannot zip them together.
    """
    groups: dict[int, list[Glyph]] = {}
    for g in glyphs:
        groups.setdefault(g.line, []).append(g)
    lines = list(groups.values())

    def row_y(line: list[Glyph]) -> float:
        body = [g for g in line if g.kind != "space" and g.size >= 9] or line
        return sum(g.y0 for g in body) / len(body)

    # PyMuPDF splits "1.1" and its title into two lines on one baseline.
    merged = True
    while merged and len(lines) > 1:
        merged = False
        lines.sort(key=row_y)
        for i in range(len(lines) - 1):
            a, b = lines[i], lines[i + 1]
            if abs(row_y(a) - row_y(b)) > 2.6:
                continue
            ax0, ax1 = min(g.x0 for g in a), max(g.x1 for g in a)
            bx0, bx1 = min(g.x0 for g in b), max(g.x1 for g in b)
            if _box_gap(ax0, ax1, bx0, bx1) > 28:
                continue
            lines[i] = a + b
            del lines[i + 1]
            merged = True
            break
    merged = True
    while merged and len(lines) > 1:
        merged = False
        lines.sort(key=lambda ln: min(g.y0 for g in ln))
        for i in range(len(lines) - 1):
            a, b = lines[i], lines[i + 1]
            if _is_prose(a) or _is_prose(b):
                continue
            ay0, ay1 = min(g.y0 for g in a), max(g.y1 for g in a)
            by0, by1 = min(g.y0 for g in b), max(g.y1 for g in b)
            vgap = _box_gap(ay0, ay1, by0, by1)
            ax0, ax1 = min(g.x0 for g in a), max(g.x1 for g in a)
            bx0, bx1 = min(g.x0 for g in b), max(g.x1 for g in b)
            hgap = _box_gap(ax0, ax1, bx0, bx1)
            short = (ax1 - ax0 < 90) or (bx1 - bx0 < 90)
            # Tall integrals overlap the next equation's box. Stacked formulas
            # have different baselines; pieces of one formula share one.
            def body_cy(line: list[Glyph]) -> float:
                body = [g for g in line if g.kind != "space" and g.size >= 9]
                group = body or line
                return sum(g.cy for g in group) / len(group)

            stacked = abs(body_cy(a) - body_cy(b)) > 9 and (ax1 - ax0) > 110 and (bx1 - bx0) > 110
            if stacked:
                continue
            overlaps = vgap == 0 and hgap < 36 and abs(body_cy(a) - body_cy(b)) <= 12
            satellite = short and vgap <= 14 and hgap < 30 and abs(body_cy(a) - body_cy(b)) <= 10
            if not overlaps and not satellite:
                continue
            lines[i] = a + b
            del lines[i + 1]
            merged = True
            break
    # A tall parenthesis is drawn as its own line beside the formula it wraps.
    fences = {"(", ")", "[", "]", r"\{", r"\}", "|", r"\|", r"\langle", r"\rangle"}
    merged = True
    while merged and len(lines) > 1:
        merged = False
        for i, line in enumerate(lines):
            solid = [g for g in line if g.kind != "space" and g.text.strip()]
            if not solid or len(solid) > 2 or any(g.text not in fences for g in solid):
                continue
            ax0, ax1 = min(g.x0 for g in line), max(g.x1 for g in line)
            ay0, ay1 = min(g.y0 for g in line), max(g.y1 for g in line)
            best: tuple[float, int] | None = None
            for j, other in enumerate(lines):
                if j == i:
                    continue
                bx0, bx1 = min(g.x0 for g in other), max(g.x1 for g in other)
                by0, by1 = min(g.y0 for g in other), max(g.y1 for g in other)
                if _box_gap(ay0, ay1, by0, by1) > 1:
                    continue
                gap = _box_gap(ax0, ax1, bx0, bx1)
                if gap < 18 and (best is None or gap < best[0]):
                    best = (gap, j)
            if best is None:
                continue
            j = best[1]
            lines[j] = lines[j] + line
            del lines[i]
            merged = True
            break
    for line in lines:
        line.sort(key=lambda g: (g.x0, g.y0))
    lines.sort(key=lambda ln: min(g.cy for g in ln))
    return lines


def _on_rule(g: Glyph, rules: list[Rule]) -> bool:
    """A digit stacked on a fraction bar is not a superscript of the letter before it."""
    for rule in rules:
        # Only the bar of a one-symbol fraction. A wider bar also covers subscripts.
        if rule.w < 3.2 or rule.w > 8:
            continue
        if rule.x0 - 1 <= g.cx <= rule.x1 + 1 and abs(g.cy - rule.cy) <= 12:
            return True
    return False


def _scripts(line: list[Glyph], rules: list[Rule] | None = None) -> list[Glyph]:
    """Attach the raised run and the lowered run to the glyph on their left.

    An evaluation bar has t=1 above and t=0 below at the same x. Taking the
    glyphs in x-order alternates the two stacks, so they are partitioned by
    height instead.
    """
    line = sorted(line, key=lambda g: (g.x0, g.y0))
    used: set[int] = set()
    out: list[Glyph] = []
    for i, g in enumerate(line):
        if i in used:
            continue
        roman_digit = g.kind == "text" and bool(re.fullmatch(r"[0-9]", g.text or ""))
        if g.kind == "space" or g.size < 9 or (g.kind != "math" and not roman_digit):
            out.append(g)
            continue
        raised: list[int] = []
        lowered: list[int] = []
        edge = g.x1
        for j in range(i + 1, len(line)):
            nxt = line[j]
            if j in used or nxt.kind == "space":
                continue
            if rules and _on_rule(nxt, rules):
                break
            if nxt.size > g.size * 0.92:
                if nxt.x0 > g.x1 + 1.6:
                    break
                continue
            if nxt.x0 > max(edge, g.x1) + 5:
                break
            up = nxt.cy < g.cy - 0.8
            down = nxt.cy > g.cy + 1.2
            if not up and not down:
                continue
            (raised if up else lowered).append(j)
            edge = max(edge, nxt.x1)
            used.add(j)
        text = g.text
        if raised:
            text += "^{" + _join(_operators([line[j] for j in raised])) + "}"
        if lowered:
            text += "_{" + _join(_operators([line[j] for j in lowered])) + "}"
        out.append(Glyph(g.x0, g.y0, edge, g.y1, g.size, text, g.kind, g.line))
    return out


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("$", r"\$").replace("*", r"\*").replace("_", r"\_")


_MATH_TEXT = set("=+−-·,;:()[]")


def _emit(line: list[Glyph], left: float) -> str:
    line = _operators(_scripts(line))
    chunks: list[str] = []
    run: list[str] = []
    prev: Glyph | None = None

    def flush() -> None:
        if not run:
            return
        body = "".join(run).strip()
        run.clear()
        if body:
            chunks.append("$" + body + "$")

    for index, g in enumerate(line):
        if prev is not None and g.kind != "space" and prev.kind != "space" and g.x0 - prev.x1 > 2.2:
            gap = " "
        else:
            gap = ""
        if g.kind == "space":
            nxt = next((line[k] for k in range(index + 1, len(line)) if line[k].kind != "space"), None)
            if run and nxt is not None and nxt.kind == "math":
                run.append(" ")
            else:
                flush()
                chunks.append(" ")
            prev = g
            continue
        nxt_solid = next((line[k] for k in range(index + 1, len(line)) if line[k].kind != "space" and line[k].text.strip()), None)
        digit = bool(re.fullmatch(r"[0-9]", g.text or ""))
        # A roman digit printed against a math glyph (2π, 1.4t) belongs in the run.
        touches_math = digit and gap == "" and (
            bool(run) or (nxt_solid is not None and nxt_solid.kind == "math" and nxt_solid.x0 - g.x1 <= 2.2)
        )
        joins_math = g.kind == "math" or (run and g.text in _MATH_TEXT) or (run and g.size < 9 and bool(re.fullmatch(r"[0-9()\[\].,+\-−=]", g.text or ""))) or touches_math
        if joins_math:
            if gap and run:
                run.append(" ")
            elif gap:
                flush()
                chunks.append(" ")
            run.append(g.text)
            prev = g
            continue
        flush()
        if gap:
            chunks.append(" ")
        chunks.append(_escape(g.text))
        prev = g
    flush()
    text = re.sub(r"[ \t]+", " ", "".join(chunks)).strip()
    text = re.sub(r" +", " ", text)
    if not text:
        return ""
    letters = sum(1 for g in line if g.kind == "text" and g.text.isalpha())
    indented = min(g.x0 for g in line) > left + 28
    if letters <= 1 and "$" in text and (indented or any(tok in text for tok in (_BIG | {r"\frac", r"\sqrt", r"\overline", r"\hat", r"\mathcal"}))):
        body = text.replace("$", "").strip()
        # A radical or a fence that lost its formula is not a displayed equation.
        leftover = re.fullmatch(r"[()\[\]√|\s]+|\\sqrt", body or "")
        if body and not leftover:
            return "$$\n" + body + "\n$$"
    if text.startswith("•"):
        return "- " + text.lstrip("•").strip()
    return text


def _visible(line: str) -> str:
    """Drop math delimiters but keep the letters inside, so a heading stays readable."""

    def repl(match: re.Match[str]) -> str:
        inner = re.sub(r"\\mathbf\{([^}]*)\}", r"\1", match.group(1))
        inner = re.sub(r"\\[a-zA-Z]+", "", inner)
        return inner

    return re.sub(r"\s+", " ", re.sub(r"\$([^$]*)\$", repl, line)).strip()


def _headings(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        plain = _visible(line)
        if line.startswith("$$") or line.startswith("- ") or line.startswith("!["):
            out.append(line)
            i += 1
            continue
        if re.fullmatch(r"Chapter\s+\d+", plain) or re.fullmatch(r"Appendix\s+[A-Z]", plain) or plain == "Index":
            title = plain
            if plain != "Index" and i + 1 < len(lines) and not lines[i + 1].startswith("$$"):
                nxt = _visible(lines[i + 1])
                if nxt and len(nxt) < 80 and not re.match(r"\d+\.\d+", nxt):
                    title = f"{plain}: {nxt}"
                    i += 1
                    if i + 1 < len(lines) and not lines[i + 1].startswith("$$"):
                        extra = _visible(lines[i + 1])
                        if extra and len(extra) < 24 and " " not in extra and title[-1] not in ".!?":
                            title = f"{title} {extra}"
                            i += 1
            out.append("# " + title)
            i += 1
            continue
        if re.match(r"^(\d+\.\d+(?:\.\d+)?|[A-Z]\.\d+)\s+\S", plain) and len(plain) < 90:
            out.append("## " + plain)
            i += 1
            continue
        out.append(line)
        i += 1
    return out


def _paragraphs(lines: list[str]) -> str:
    blocks: list[str] = []
    buf = ""
    for line in lines:
        if line.startswith("#") or line.startswith("$$") or line.startswith("- ") or line.startswith("!["):
            if buf:
                blocks.append(buf)
                buf = ""
            blocks.append(line)
            continue
        if not buf:
            buf = line
            continue
        # Index entries and other short stacked lines are not wrapped prose.
        if len(buf) < 72 and len(line) < 72:
            blocks.append(buf)
            buf = line
            continue
        if buf.endswith("-") and line[:1].islower():
            buf = buf[:-1] + line
        elif buf[-1:] in ".?!:":
            blocks.append(buf)
            buf = line
        else:
            buf += " " + line
    if buf:
        blocks.append(buf)
    return "\n\n".join(blocks).strip() + "\n"


def render_page(page: pymupdf.Page, figure_dir: Path | None, page_no: int) -> str:
    glyphs, rules, figures = extract_page(page)
    glyphs = [g for g in glyphs if 48 < g.y0 < page.rect.height - 36]
    rules = [r for r in rules if 48 < r.y0 < page.rect.height - 36]
    events: list[tuple[float, int, str]] = []
    for rect in figures:
        clip = rect & page.rect
        if figure_dir is None or clip.width < 40:
            continue
        figure_dir.mkdir(parents=True, exist_ok=True)
        name = f"p{page_no:03d}.png"
        # Disambiguate several figures on one page.
        n = 1 + sum(1 for _, _, text in events if text.startswith("!["))
        if n > 1:
            name = f"p{page_no:03d}-{n}.png"
        page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=clip, alpha=False).save(figure_dir / name)
        events.append((clip.y0, 0, f"![Figure on page {page_no}](figures/{name})"))
        glyphs = [g for g in glyphs if not (clip.x0 <= g.cx <= clip.x1 and clip.y0 <= g.cy <= clip.y1)]
        rules = [r for r in rules if not (clip.x0 <= r.cx <= clip.x1 and clip.y0 <= r.cy <= clip.y1)]
    columns = _columns(glyphs, page.rect.width)
    multi = len(columns) > 1
    for col_index, column in enumerate(columns):
        if not column:
            continue
        lo, hi = min(g.x0 for g in column) - 12, max(g.x1 for g in column) + 12
        col_rules = [r for r in rules if lo <= r.cx <= hi] if multi else rules
        limited = bind_limits_safe(bind_overlays(column))
        # Scripts that share a PyMuPDF line (exponents, c_k) have to be glued
        # before a fraction or overline joins those glyphs as flat text.
        by_line: dict[int, list[Glyph]] = {}
        for g in limited:
            by_line.setdefault(g.line, []).append(g)
        scripted: list[Glyph] = []
        for group in by_line.values():
            scripted.extend(_scripts(group, col_rules))
        prepared = bind_fractions(scripted, col_rules)
        lines = _baselines(prepared)
        left = min((g.x0 for g in column if g.kind == "text"), default=50)
        # A second column is read after the first, not woven in by height.
        column_key = col_index if multi else 0
        for line in lines:
            text = _emit(line, left)
            if text:
                events.append((min(g.y0 for g in line), column_key, text))
    events.sort(key=lambda item: (item[1], item[0]))
    return _paragraphs(_headings([text for _, _, text in events]))


def slug(title: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", title.lower().replace(":", " ")).strip("-")
    return text or "chapter"


def _plain_heading(text: str) -> str:
    text = re.sub(r"\\mathbf\{([^}]*)\}", r"\1", text)
    return text.replace("\\", "").replace("$", "").strip()


def chapter_filename(title: str) -> str:
    """Match the other libraries: '1. Fourier Series.md'."""
    matched = re.match(r"Chapter\s+(\d+)\s*:?\s*(.*)", title)
    if matched:
        name = _plain_heading(matched.group(2).strip() or f"Chapter {matched.group(1)}")
        return f"{matched.group(1)}. {name}.md"
    matched = re.match(r"Appendix\s+([A-Z])\s*:?\s*(.*)", title)
    if matched:
        name = _plain_heading(matched.group(2).strip() or f"Appendix {matched.group(1)}")
        return f"{matched.group(1)}. {name}.md"
    if title.lower() == "contents":
        return "0. Contents.md"
    return f"{title}.md"


def chapter_breaks(doc: pymupdf.Document) -> list[tuple[str, int]]:
    found: list[tuple[str, int]] = []
    for i, page in enumerate(doc):
        glyphs, _, _ = extract_page(page)
        rows: dict[int, list[Glyph]] = {}
        for g in glyphs:
            if g.y0 < 80 or g.kind == "space":
                continue
            rows.setdefault(round(g.y0), []).append(g)
        labels: list[tuple[int, str]] = []
        for y in sorted(rows)[:6]:
            parts: list[str] = []
            prev: Glyph | None = None
            for g in sorted(rows[y], key=lambda g: g.x0):
                if g.kind == "space" or (prev is not None and g.x0 - prev.x1 > 2):
                    parts.append(" ")
                if g.kind != "space":
                    parts.append(g.text)
                    prev = g
            labels.append((y, re.sub(r"\s+", " ", "".join(parts)).strip()))
        if not labels:
            continue
        head = labels[0][1]
        chapter = re.match(r"Chapter\s*(\d+)", head)
        appendix = re.match(r"Appendix\s*([A-Z])", head)
        if chapter or appendix or head == "Index":
            if chapter:
                title = f"Chapter {chapter.group(1)}"
            elif appendix:
                title = f"Appendix {appendix.group(1)}"
            else:
                title = "Index"
            if title != "Index":
                name: list[str] = []
                prev_y = labels[0][0]
                for y, text in labels[1:]:
                    if not text or re.match(r"\d", text):
                        break
                    # "Chapter N" sits well above its title. A wrapped title
                    # stays close to the line above it; the first section does not.
                    limit = 80 if not name else 40
                    if y - prev_y > limit:
                        break
                    name.append(_plain_heading(text))
                    prev_y = y
                if name:
                    title = f"{title}: {' '.join(name)}"
            found.append((title, i + 1))
        elif i == 2:
            found.append(("Contents", i + 1))
    found.sort(key=lambda item: item[1])
    return found


def _pages_of(spec: str, count: int) -> list[int]:
    pages: list[int] = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            pages.extend(range(int(a), int(b or count) + 1))
        else:
            pages.append(int(chunk))
    return pages


def _reader_slug(text: str) -> str:
    """Same id the reader gives a heading: ASCII slug of its visible text."""
    text = re.sub(r"[^A-Za-z0-9_\s-]", "", text.strip().lower())
    return re.sub(r"\s+", "-", text)


def _heading_targets(out_dir: Path) -> dict[str, tuple[str, str]]:
    """Map '1.1' to the chapter file and the reader's heading id."""
    found: dict[str, tuple[str, str]] = {}
    for path in sorted(out_dir.glob("*.md")):
        if path.name in {"0. Contents.md", "README.md"}:
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("## "):
                continue
            heading = line[3:].strip()
            # "1.2.2 ..." is a subsection. Only "1.2 " is a contents entry,
            # and a later subsection must not overwrite it.
            matched = re.match(r"^(\d+\.\d+|[A-Z]\.\d+)(?=\s)", heading)
            if matched:
                found.setdefault(matched.group(1), (path.name, _reader_slug(heading)))
    return found


def _md_link(text: str, filename: str, anchor: str = "") -> str:
    dest = filename + (f"#{anchor}" if anchor else "")
    return f"[{text}](<{dest}>)"


def _toc_entries(doc: pymupdf.Document, start: int, end: int) -> list[tuple[str, str, str]]:
    """Entries as (kind, number, title). Titles keep the math the prose pass flattened.

    The contents pages are a two-column list with dot leaders. Reading them as
    paragraphs glues each page number onto the next title, so this walks the
    positioned spans instead.
    """
    entries: list[tuple[str, str, str]] = []
    for number in range(start, end + 1):
        page = doc[number - 1]
        raw: list[dict] = []
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for line in block["lines"]:
                raw.extend(line["spans"])
        raw.sort(key=lambda span: (span["bbox"][1], span["bbox"][0]))
        clusters: list[dict] = []
        for span in raw:
            y = span["bbox"][1]
            if y < 48 or span["size"] > 16:
                continue
            if clusters and y - clusters[-1]["y"] <= 7:
                clusters[-1]["spans"].append(span)
                if span["size"] >= 10:
                    clusters[-1]["y"] = y
            else:
                clusters.append({"y": y, "spans": [span]})
        for cluster in clusters:
            title = _toc_title(cluster["spans"])
            if not title or title.lower() == "contents":
                continue
            section = re.match(r"^(\d+\.\d+|[A-Z]\.\d+)\s+(.*)$", title)
            if section:
                entries.append(("section", section.group(1), section.group(2).strip()))
                continue
            chapter = re.match(r"^(Index|[A-Z]|\d+)\b\s*(.*)$", title)
            if chapter:
                entries.append(("chapter", chapter.group(1), chapter.group(2).strip()))
    return entries


def _toc_title(spans: list[dict]) -> str:
    spans = sorted(spans, key=lambda span: span["bbox"][0])
    tokens: list[tuple[str, str, float]] = []
    prev_x1: float | None = None
    for span in spans:
        if span["bbox"][0] > 510:
            continue
        raw = re.sub(r"(?:\s*\.){2,}.*$", "", span["text"])
        raw = re.sub(r"\s+\.\s*$", "", raw)
        leading = bool(raw[:1].isspace())
        text = raw.strip()
        if not text or re.fullmatch(r"[.\s]+", text):
            continue
        gap = 0.0 if prev_x1 is None else span["bbox"][0] - prev_x1
        if leading:
            gap = max(gap, 2.0)
        font = span["font"]
        if span["size"] < 9.5:
            if re.fullmatch(r"\d", text) and tokens and tokens[-1][0] in {"mi", "btext"} and tokens[-1][1] in {"L", "R"}:
                tokens.append(("sup", text, gap))
                prev_x1 = span["bbox"][2]
            continue
        if font.startswith("CMMIB"):
            kind = "mb"
        elif font.startswith("CMMI"):
            kind = "mi"
        elif font.startswith("CMBX"):
            kind = "btext"
        elif font.startswith("CMBSY"):
            kind = "sym"
        else:
            kind = "text"
        tokens.append((kind, text, gap))
        prev_x1 = span["bbox"][2]
    parts: list[str] = []
    index = 0
    while index < len(tokens):
        kind, text, gap = tokens[index]
        nxt = tokens[index + 1] if index + 1 < len(tokens) else None
        space = " " if gap > 1.2 and parts else ""
        if kind == "mi" and text == "L" and nxt and nxt[0] == "sup":
            parts.append(f"{space}$L^{{{nxt[1]}}}$")
            index += 2
            continue
        if kind == "btext" and text == "R" and nxt and nxt[0] == "sup":
            parts.append(space + r"$\mathbf{R}^{" + nxt[1] + "}$")
            index += 2
            continue
        if kind == "btext" and text == "1" and nxt and nxt[0] == "mb" and nxt[1] == "/x":
            parts.append(space + r"$\mathbf{1/x}$")
            index += 2
            continue
        if kind == "mb" and re.fullmatch(r"[A-Za-z]", text):
            parts.append(space + r"$\mathbf{" + text + "}$")
        elif kind == "mi" and text == "δ":
            parts.append(space + r"$\delta$")
        elif kind == "mi" and text == ",":
            parts.append(",")
        elif kind == "sym":
            parts.append(r" $\ast$ ")
        elif kind == "btext" and text == "sinc":
            parts.append(space + r"$\operatorname{sinc}$")
        else:
            parts.append(space + text)
        index += 1
    title = re.sub(r" {2,}", " ", "".join(parts))
    title = re.sub(r" +([,.;:?])", r"\1", title).strip().rstrip(".")
    # The superscript of L^2 is its own span, so the ([0, 1]) that follows
    # would otherwise sit outside the math.
    return title.replace(r"$L^{2}$([0, 1])", r"$L^{2}([0, 1])$")


def _chapter_filename_for(number: str, title: str) -> str:
    if number == "Index":
        return "Index.md"
    plain = re.sub(r"\$\\mathbf\{([^}]*)\}\$", r"\1", title)
    plain = re.sub(r"\$\\operatorname\{([^}]*)\}\$", r"\1", plain)
    plain = plain.replace("$", "").replace("\\", "")
    plain = re.sub(r"\s+", " ", plain).strip()
    return f"{number}. {plain}.md"


def render_contents(doc: pymupdf.Document, start: int, end: int, out_dir: Path) -> str:
    targets = _heading_targets(out_dir)
    lines = ["# Contents", ""]
    current_file = ""
    for kind, number, title in _toc_entries(doc, start, end):
        if kind == "chapter":
            if lines and lines[-1].startswith("- "):
                lines.append("")
            filename = _chapter_filename_for(number, title)
            if not (out_dir / filename).exists():
                match = next((path.name for path in out_dir.glob("*.md") if path.name.startswith(f"{number}. ")), "")
                if match:
                    filename = match
            current_file = filename
            label = number if number == "Index" or not title else f"{number} {title}"
            lines.append(f"## {_md_link(label, filename)}")
            lines.append("")
            continue
        filename, anchor = targets.get(number, (current_file, ""))
        if filename:
            lines.append(f"- {_md_link(f'{number} {title}', filename, anchor)}")
        else:
            lines.append(f"- {number} {title}")
    text = "\n".join(lines).rstrip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text)


def convert(pdf: Path, out_dir: Path, pages: list[int] | None) -> list[Path]:
    doc = pymupdf.open(pdf)
    out_dir.mkdir(parents=True, exist_ok=True)
    figure_dir = out_dir / "figures"
    if pages:
        parts = []
        for n in pages:
            print(f"page {n}", file=sys.stderr)
            parts.append(render_page(doc[n - 1], figure_dir, n))
        path = out_dir / "pages.md"
        path.write_text("\n\n".join(p.strip() for p in parts if p.strip()) + "\n", encoding="utf-8")
        return [path]
    breaks = chapter_breaks(doc)
    if not breaks:
        raise SystemExit("no chapter breaks found")
    written = []
    contents_job: tuple[int, int] | None = None
    for number, (title, start) in enumerate(breaks):
        end = breaks[number + 1][1] - 1 if number + 1 < len(breaks) else doc.page_count
        # The contents list is rebuilt after the chapters, so its links can
        # point at the heading ids those files actually got.
        if title == "Contents":
            contents_job = (start, end)
            continue
        print(f"{title} (pdf {start}-{end})", file=sys.stderr)
        parts = []
        for n in range(start, end + 1):
            try:
                parts.append(render_page(doc[n - 1], figure_dir, n))
            except Exception as exc:
                print(f"  page {n} failed: {exc}", file=sys.stderr)
        body = "\n\n".join(p.strip() for p in parts if p.strip()).strip()
        plain_title = _plain_heading(title.split(":", 1)[-1].strip() if title.startswith(("Chapter", "Appendix")) else title)
        if body.startswith(plain_title + "\n"):
            body = body[len(plain_title):].lstrip()
        if not body.startswith("# "):
            body = f"# {_plain_heading(title)}\n\n" + body
        path = out_dir / chapter_filename(title)
        path.write_text(body + "\n", encoding="utf-8")
        written.append(path)
    if contents_job:
        start, end = contents_job
        print(f"Contents (pdf {start}-{end})", file=sys.stderr)
        path = out_dir / "0. Contents.md"
        path.write_text(render_contents(doc, start, end, out_dir), encoding="utf-8")
        written.insert(0, path)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("-o", "--out", type=Path, required=True)
    parser.add_argument("--pages", help="1-based pages, e.g. 17-18. Skips the chapter split.")
    args = parser.parse_args(argv)
    pages = None
    if args.pages:
        pages = _pages_of(args.pages, pymupdf.open(args.pdf).page_count)
    for path in convert(args.pdf, args.out, pages):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
