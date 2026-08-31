#!/usr/bin/env python3
"""Render a PDF into per-page PNG images.

Lecture notes are LaTeX, so text extraction is messy. This dumps a picture of
each page instead. Default target is the Tong notes one directory up.

Usage (from this folder):

    python3 -m venv .venv
    source .venv/bin/activate          # Windows: .venv\\Scripts\\activate
    pip install -r requirements.txt
    python extract_pages.py            # all pages of tong-lecture_notes.pdf
    python extract_pages.py --pages 1-12
    python extract_pages.py --pages 3,8,20-22 --dpi 250
    python extract_pages.py "../Dyson - Advanced QM.pdf" -o dyson_pages
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent
DEFAULT_PDF = ROOT.parent / "tong-lecture_notes.pdf"
DEFAULT_OUT = ROOT / "pages"


def parse_pages(spec: str, page_count: int) -> list[int]:
    """Parse a 1-indexed spec like '1-5,8,20-22' into PDF page numbers."""
    pages: list[int] = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            start_s, end_s = chunk.split("-", 1)
            start, end = int(start_s), int(end_s)
            if start < 1 or end > page_count or start > end:
                raise ValueError(
                    f"range {chunk!r} is outside 1-{page_count}"
                )
            pages.extend(range(start, end + 1))
        else:
            n = int(chunk)
            if n < 1 or n > page_count:
                raise ValueError(f"page {n} is outside 1-{page_count}")
            pages.append(n)

    # Keep order, drop duplicates.
    seen: set[int] = set()
    unique: list[int] = []
    for n in pages:
        if n not in seen:
            seen.add(n)
            unique.append(n)
    return unique


def render_page(page: fitz.Page, dest: Path, dpi: int) -> None:
    zoom = dpi / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    dest.parent.mkdir(parents=True, exist_ok=True)
    pix.save(dest)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render PDF pages to PNGs (one image per page)."
    )
    parser.add_argument(
        "pdf",
        nargs="?",
        type=Path,
        default=DEFAULT_PDF,
        help=f"PDF to render (default: {DEFAULT_PDF.name})",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help="Folder for page images (default: extract/pages/)",
    )
    parser.add_argument(
        "-p",
        "--pages",
        help="Pages to render, 1-indexed as in a PDF viewer. "
        "Examples: 1-20   or   3,8,15-18. Default: all pages.",
    )
    parser.add_argument(
        "-d",
        "--dpi",
        type=int,
        default=200,
        help="Render resolution (default: 200). Use 150 for smaller files, "
        "300 if math looks soft.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-render even if the PNG already exists.",
    )
    args = parser.parse_args(argv)

    pdf_path = args.pdf.expanduser().resolve()
    out_dir = args.output.expanduser().resolve()

    if not pdf_path.is_file():
        print(f"error: PDF not found: {pdf_path}", file=sys.stderr)
        return 1
    if args.dpi < 72:
        print("error: --dpi should be at least 72", file=sys.stderr)
        return 1

    doc = fitz.open(pdf_path)
    try:
        page_count = doc.page_count
        if args.pages:
            try:
                wanted = parse_pages(args.pages, page_count)
            except ValueError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 1
        else:
            wanted = list(range(1, page_count + 1))

        width = len(str(page_count))
        out_dir.mkdir(parents=True, exist_ok=True)

        print(f"source : {pdf_path}")
        print(f"output : {out_dir}")
        print(f"pages  : {len(wanted)} of {page_count}  @ {args.dpi} dpi")

        rendered = skipped = 0
        try:
            for i, page_no in enumerate(wanted, start=1):
                dest = out_dir / f"page-{page_no:0{width}d}.png"
                if dest.exists() and not args.force:
                    skipped += 1
                    print(f"  [{i}/{len(wanted)}] skip {dest.name}")
                    continue
                render_page(doc[page_no - 1], dest, args.dpi)
                rendered += 1
                print(f"  [{i}/{len(wanted)}] {dest.name}")
        except KeyboardInterrupt:
            print("\ninterrupted", file=sys.stderr)
            return 130
    finally:
        doc.close()

    print(f"done   : {rendered} written, {skipped} skipped → {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
