# Appendix A: Mathematical Background

## A.1 Complex Numbers

These notes are intended as a summary and review of complex numbers. I’m assuming that the deﬁnition, notation, and arithmetic of complex numbers are known to you, but we’ll put the basic facts on the record. In the course we’ll also use calculus operations involving complex numbers, usually complex valued functions of a real variable. For what we’ll do, this will not involve the area of mathematics referred to as “Complex Analysis”.

For our purposes, the extensions of the formulas of calculus to complex numbers are straightforward and reliable.

Declaration of principles Without apology I will write

$$
i = √\overline{−1}.
$$

In many areas of science and engineering it’s common to use $j$ for $√\overline{−1.}$ If you want to use $j$ in your own work I won’t try to talk you out of it. But I’ll use $i$.

Before we plunge into notation and formulas there are two points to keep in mind:

- Using complex numbers greatly simpliﬁes the algebra we’ll be doing. This isn’t the only reason they’re

used, but it’s a good one.

- We’ll use complex numbers to represent real quantities — real signals, for example. At this point in

your life this should not cause a metaphysical crisis, but if it does my only advice is to get over it.

Let’s go to work.

Complex numbers, real and imaginary parts, complex conjugates A complex number is determined by two real numbers, its real and imaginary parts. We write

$$
z = x + iy
$$

where $x$ and $y$ are real and

$$
i^{2} = −1.
$$

$x$ the real part and $y$ is the imaginary part, and we write $x$ = Re$z, y$ = Im$z$. Note: it’s $y$ that is the imaginary part of $z$ = $x$ +$iy,$ not $iy$. One says that $iy$ is an imaginary number or is purely imaginary. One

says that $z$ has positive real part (resp., positive imaginary part) if $x$ (resp., $y)$ is positive. The set of all complex numbers is denoted by C. (The set of all real numbers is denoted by R.) Elementary operations on complex numbers are deﬁned according to what happens to the real and imaginary parts. For example, if $z$ = $a$ + $ib$ and $w$ = $c$ + $di$ then their sum and product are given by

$$
z + w = (a + c) + (b + d)i
$$

$$
zw = (ac − bd) + i(ad + bc)
$$

I’ll come back to the formula for the general quotient $z/w,$ but here’s a particular little identity that’s used often: Since $i · i$ = $i^{2}$ = $−$1 we have 1 $i$ = $−i$ and $i(−i)$ = 1$.$ The complex conjugate of $z$ = $x$ + $iy$ is

$$
z¯ = x − iy.
$$

Other notations for the complex conjugate are $z^{∗}$ and sometimes even $z^{†}$. It’s useful to observe that $z$ = $z$¯ if and only if $z$ is real, i.e., $y$ = 0.

Note also that

$$
\overline{z+w} = z + \overline{w}, \overline{z w} = z\overline{w}, z = z .
$$

We can ﬁnd expressions for the real and imaginary parts of a complex number using the complex conjugate.

If $z$ = $x$ + $iy$ then $z$ = $x − iy$ so that in the sum $z$ + $z$ the imaginary parts cancel. That is $z$ + $z$ = 2$x,$ or $x$ = Re$z$ = $\frac{z+z}{2} .$ Similarly, in the diﬀerence, $z − z$¯, the real parts cancel and $z − z$¯ = 2$iy,$ or $y$ = Im$z$ = $\frac{z−z¯}{2 i} .$ Don’t forget the $i$ in the denominator here.

The formulas $\overline{z+w}$ = $z$¯+ $w$¯ and $\overline{z s w u}$ = $z$¯ $w$¯ extend to sums and products of more than two complex numbers, and to integrals (being limits of ms), leading to formulas like

$$
\overline{\int f(t)g(t)d t} \int
$$

= $\overline{f(t)} \overline{g(t)}dt ($here $dt$ is a real quantity.) This overextended use of the overline notation for complex conjugates shows why it’s useful to have alternate notations, such as

$$
(\int f(t)g(t)dt)^{∗} = \int f(t^{∗}) g(t^{∗}) dt.
$$

It’s best not to mix stars and bars in a single formula, so please be mindful of this. I wrote these formulas for “indeﬁnite integrals” but in our applications it will be deﬁnite integrals that come up.

The magnitude of $z$ = $x$ + $iy$ is

$$
|z| = \sqrt{x^{2}+y^{2}} .
$$

Multiplying out the real and imaginary parts gives

$$
zz¯ = (x + iy)(x− iy) = x^{2} − i^{2}y^{2} = x^{2} + y^{2} = |z^{2}| .
$$

This formula comes up all the time.

More generally, $|z$ + $w^{2}|$ = $|z^{2}|$ + 2 Re${z w$¯$}$ + $|w^{2}|$ which is also $|z^{2}|$ + 2 Re${z$¯$w}$ + $|w^{2}| .$ To verify this,

$$
|z + w^{2}| = (z + w)(z¯ + w¯)
$$

$$
= zz¯ + z w¯ + wz¯ \frac{+w}{z w¯} w¯
$$

$$
|z^{2}| + (z¯w + \overline{z¯w)} + |w^{2}| .
$$

$$
= |z^{2}| + (z w¯ + + ) + |w^{2}|
$$

which is also The quotient $z/w$ For people who really need to ﬁnd the real and imaginary parts of a quotient $z/w$ here’s how it’s done. Write $z$ = $a$ + $bi$ and $w$ = $c$ + $di$. Then

$$
\frac{z}{w} = \frac{a+b i}{c+d i}
$$

$$
= \frac{a+b i}{c+d i} \frac{c−d i}{c−d i}
$$

$$
= \frac{(a+b i)(c−d i)}{c^{2}+d^{2}} = \frac{(a c+b d)+(b c−a d)i}{c^{2}+d^{2}} .
$$

Thus Re $\frac{a+b i}{c+d i}$ = $\frac{a c+b d}{c^{2}+d^{2}} ,$ Im $\frac{a+b i}{c+d i}$ = $\frac{b c−a d}{c^{2}+d^{2}} .$ Do not memorize this. Remember the “multiply the top and bottom by the conjugate” sort of thing.

Polar form Since a complex number is determined by two real numbers it’s natural to associate$z$ = $x+iy$ with the pair ($x,y) ∈$ R2, and hence to identify $z$ with the point in the plane with Cartesian coordinates ($x,y)$. One also then speaks of the “real axis” and the “imaginary axis”.

We can also introduce polar coordinates $r$ and $θ$ and relate them to the complex number $z$ = $x+iy$ through the equations

$$
\sqrt{x^{2}+y^{2}}
$$

$r$ = = $|z|$ and $θ$ = tan$−1 y$

$$
x .
$$

The angle $θ$ is called the argument or the phase of the complex number. One sees the notation $θ$ = arg$z$ and also $θ$ = ∠$z.$ Going from polar to Cartesian through $x$ = $r$ cos$θ$ and $y$ = $r$ = sin$θ,$ we have the polar form of a complex number:

$x$ + $iy$ = $r$ cos$θ$ + $ir$ sin$θ$ = $r($cos$θ$ + $i$ sin$θ).$

## A.2 The Complex Exponential and Euler’s Formula

The real workhorse for us will be the complex exponential function. The exponential function $e^{z}$ for a complex number $z$ is deﬁned, just as in the real case, by the Taylor series:

$$
e^{z} = 1 + z + \frac{z^{2}}{2!} + \frac{z^{3}}{3!} + ··· = \sum_{n=0}^{∞} \frac{z^{n}}{n!} .
$$

This converges for all $z ∈$ C, but we won’t check that.

Notice also that

$$
\overline{e^{z}} = \overline{\sum_{∞n=0}^{∞})}
$$

$\frac{z^{n}}{n!} ($a heroic use of the bar notation)

$$
= \sum_{n=0} \frac{z^{n}¯}{n!}
$$

$$
= e^{z¯}
$$

Also, $e^{z}$ satisﬁes the diﬀerential equation $y^{′}$ = $y$ with initial condition $y($0) = 1 (this is often taken as a deﬁnition, even in the complex case). By virtue of this, one can verify the key algebraic properties:

$$
e^{z+w} = e^{z}e^{w}
$$

Here’s how this goes. Thinking of $w$ as ﬁxed,

$$
\frac{d}{d z}e^{z+w} = e^{z+w}
$$

hence $e^{z+w}$ must be a constant multiple of $e^{z};$

$$
e^{z+w} = ce^{z} .
$$

What is the constant? At $z$ = 0 we get

$$
e^{w} = ce^{0} = c.
$$

Done. Using similar arguments one can show the other basic property of exponentiation,

$$
(e^{z})r = e^{z r}
$$

if $r$ is real. It’s actually a tricky business to deﬁne ($e^{z})w$ when $w$ is complex (and hence to establsh ($e^{z})w$ = $e^{z w})$. This requires introducing the complex logarithm, and special considerations are necessary.

We will not go into this.

The most remarkable thing happens when the exponent is purely imaginary. The result is called Euler’s formula and reads $e^{i θ}$ = cos$θ$ + $i$ sin$θ.$ I want to emphasize that the left hand side has only been deﬁned via a series. The exponential function in the real case has nothing to do with the trig functions sine and cosine, and why it should have anything

to do with them in the complex case is a true wonder.1 Plugging $θ$ = $π$ into Euler’s formula gives $e^{i π}$ = cos$π$ + $i$ sin$π$ = $−$1, better written as

$$
e^{i π} + 1 = 0.
$$

This is sometimes referred to as the most famous equation in mathematics; it expresses a simple relationship — and why should there be any at all? — between the fundamental numbers $e, π,$ 1, and 0, not to mention $i$. We’ll probably never see this most famous equation again, but now we’ve seen it once.

Consequences of Euler’s formula The polar form $z$ = $r($cos$θ$ + $i$ sin$θ)$ can now be written as

$$
z = re^{i θ} ,
$$

where $r$ = $|z|$ is the magnitude and $θ$ is the phase of the complex number $z$. Using the arithmetic properties of the exponential function we also have that if $z_{1}$ = $r_{1}e^{i θ 1}$ and $z_{2}$ = $r_{2}e^{i θ 2}$ then

$$
z_{1}z_{2} = r_{1}r_{2}e^{i(θ 1+θ 2)} .
$$

That is, the magnitudes multiply and the arguments (phases) add.

Euler’s formula also gives a dead easy way of deriving the addition formulas for the sine and cosine. On the one hand,

$$
e^{i(α+β)} = e^{i α}e^{i β}
$$

= (cos$α$ + $i$ sin$α)($cos$β$ + $i$ sin$β)$

= (cos$α$ cos$β −$ sin$α$ sin$β)$ + $i($sin$α$ cos$β$ + cos$α$ sin$β).$

On the other hand,

$e^{i(α+β)}$ = cos($α$ + $β)$ + $i$ sin($α$ + $β).$

Equating the real and imaginary parts gives

cos($α$ + $β)$ = cos$α$ cos$β −$ sin$α$ sin$β$

sin($α$ + $β)$ = sin$α$ cos$β$ + cos$α$ sin$β$ I went through this derivation because it expresses in a simple way an extremely important principle in mathematics and its applications.

1 Euler’s formula is usually proved by substituting into and manipulating the Taylor series for cos$θ$ and sin$θ.$ Here’s another more elegant way of seeing it. It relies on results for diﬀerential equations, but the proofs of those are no more diﬃcult that the proofs of the properties of Taylor series that one needs in the usual approach. Let $f(θ)$ = $eiθ.$ Then $f(0)$ = 1 and $f′(θ)$ = $ieiθ,$ so that $f′(0)$ = $i.$ Moreover

$$
f′′(θ) = i2eiθ = −eiθ = −f(θ)
$$

i.e., $f$ satisﬁes

$$
f′′ +f = 0, f(0) = 1,f′(0) = i.
$$

On the other hand if $g(θ)$ = cos$θ$ +$i$ sin$θ$ then

$g′′(θ)$ = $−$cos$θ−i$ sin$θ$ = $−g(θ),$ or $g′′$ +$g$ = 0

and also

$$
g(0) = 1, g′(0) = i.
$$

Thus $f$ and $g$ satisfy the same diﬀerential equation with the same initial conditions, so $f$ and $g$ must be equal. Slick. I prefer using the second order ordinary diﬀerential equation here since that’s the one naturally associated with the sine and cosine.

We could also do the argument with the ﬁrst order equation $y′$ = $y.$ Indeed, if $f(θ)$ = $eiθ$ then $f′(θ)$ = $ieiθ$ = $if(θ)$ and $f(0)$ = 1. Likewise, if $g(θ)$ = cos$θ$ +$i$ sin$θ$ then $g′(θ)$ = $−$sin$θ$ +$i$ cos$θ$ = $i(cosθ$ +$i$ sin$θ)$ = $ig(θ)$ and $g(0)$ = 1. This implies that $f(θ)$ = $g(θ)$ for all $θ.$

If you can compute the same thing two diﬀerent ways, chances are you’ve done something signiﬁcant.

Take this seriously.2 Symmetries of the sine and cosine: eve nd $\frac{o}{i θ}$dd functions Using the identity

$$
\frac{n a}{e^{i θ}} = e = e^{−i θ}
$$

we can express the cosine and the sine as the real and imaginary parts, respectively, of $e^{i θ}:$ cos$θ$ = $\frac{e^{i θ}+e^{−i θ}}{2}$ and sin$θ$ = $\frac{e^{i θ}−e^{−i θ}}{2 i}$ Once again this is a simple observation. Once again there is something more to say.

You are very familiar with the symmetries of the sine and cosine function. That is, cos$θ$ is an even function, meaning cos($−θ)$ = cos$θ,$ and sin$θ$ is an odd function, meaning sin($−θ)$ = $−$sin$θ.$ Why is this true? There are many ways of seeing it (Taylor series, diﬀerential equations), but here’s one you may not have thought of before, and it ﬁts into a general framework of evenness and oddness that we’ll ﬁnd useful when discussing symmetries of the Fourier transform.

If $f(x)$ is any function, then the function deﬁned by

$$
f_{e}(x) = \frac{f(x)+f(−x)}{2}
$$

is even. Check it out:

$$
f_{e}(−x) = \frac{f(−x)+f(−(−x))}{2} = \frac{f(−x)+f(x)}{2} = f_{e}(x).
$$

Similarly, the function deﬁned by

$$
f_{o}(x) = \frac{f(x)−f(−x)}{2}
$$

is odd. Moreover

$$
f_{e}(x) + f_{0}(x) = \frac{f(x)+f(−x)}{2} + \frac{f(x)−f(−x)}{2} = f(x)
$$

The conclusion is that any function can be written as the sum of an even function and an odd function. Or, to put it another way, $f_{e}(x)$ and $f_{o}(x)$ are, respectively, the even and odd parts of $f(x),$ and the function is the sum of its even and odd parts. We can ﬁnd some symmetries in a function even if it’s not symmetric.

And what are the even and odd parts of the function $e^{i θ}$? For the even part we have $\frac{e^{i θ}+e^{−i θ}}{2}$ = cos$θ$ and for the odd part we have $\frac{e^{i θ}−e^{−i θ}}{2} = i$ sin$θ .$ Nice.

2 In some ways this is a maxim for the Fourier transform class. As we shall see, the Fourier transform allows us to view a signal in the time domain and in the frequency domain; two diﬀerent representations for the same thing. Chances are this is something signiﬁcant.

## A.3 Algebra and Geometry

To wrap up this review I want to say a little more about the complex exponential and its use in representing sinusoids. To set the stage for this we’ll consider the mix of algebra and geometry — one of the reasons why complex numbers are often so handy.

We not only think of a complex number $z$ = $x$ + $iy$ as a point in the plane, we also think of it as a vector with tail at the origin and tip at ($x,y)$. In polar form, either written as $re^{i θ}$ or as $r($cos$θ$ + $i$ sin$θ),$ we recognize $|z|$ = $r$ as the length of the vector and $θ$ as the angle that the vector makes with the $x-$axis (the real axis). Note that

$$
\sqrt{c o s 2 θ+s i n 2 θ}
$$

$|e^{i θ}|$ = $|$ cos$θ$ + $i$ sin$θ|$ =

$$
= 1.
$$

Many is the time you will use $|e^{i(s o m e t h i n g r e a l)} |$ = 1.

Once we make the identiﬁcation of a complex number with a vector we have an easy back-and-forth between the algebra of complex numbers and the geometry of vectors. Each point of view can help the other.

Take addition. The sum of $z$ = $a$ + $bi$ and $w$ = $c$ + $di$ is the complex number $z$ + $w$ = ($a$ + $c)$ + ($c$ + $d)i$.

Geometrically this is given as the vector sum. If $z$ and $w$ are regarded as vectors from the origin then $z$ +$w$ is the vector from the origin that is the diagonal of the parallelogram determined by $z$ and $w$.

Similarly, as a vector, $z − w$ = ($a − c)$ + ($b − d)i$ is the vector that goes from the tip of $w$ to the tip of $z,$ i.e., along the other diagonal of the parallelogram determined by $z$ and $w$. Notice here that we allow for the customary ambiguity in placing vectors; on the one hand we identify the complex number $z − w$ with the vector with tail at the origin and tip at ($a − c,b− d)$. On the other hand we allow ourselves to place the (geometric) vector anywhere in the plane as long as we maintain the same magnitude and direction of the vector.

It’s possible to give a geometric interpretation of $zw$ (where, you will recall, the magnitudes multiply and the arguments add) in terms of similar triangles, but we won’t need this.

Complex conjugation also has a simple geometric interpretation. If $z$ = $x$ +$iy$ then the complex conjugate $z$¯ = $x−iy$ is the mirror image of $z$ in the $x-$axis. Think either in terms of reﬂecting the point ($x,y)$ to the point ($x,−y)$ or reﬂecting the vector. This gives a natural geometric reason why $z$ + $z$¯ is real — since $z$ and $z$¯ are symmetric about the real axis, the diagonal of the parallelogram determined by $z$ and $z$¯ obviously goes along the real axis. In a similar vein, $−z$¯ = $−(x − iy)$ = $−x$ + $iy$ is the reﬂection of $z$ = $x$ + $iy$ in the $y-$axis, and now you can see what $z − z$¯ is purely imaginary.

There are plenty of examples of the interplay between the algebra and geometry of complex numbers, and the identiﬁcation of complex numbers with points in the plane (Cartesian or polar coordinates) often leads to some simple approaches to problems in analytic geometry. Equations in $x$ and $y$ (or in $r$ and $θ)$ can often be recast as equations in complex numbers, and having access to the arithmetic of complex numbers frequently simpliﬁes calculations.

## A.4 Further Applications of Euler’s Formula

We’ve already done some work with Euler’s formula $e^{i θ}$ = cos$θ$ + $i$ sin$θ,$ and we agree it’s a ﬁne thing to know. For additional applications we’ll replace $θ$ by $t$ and think of

$e^{i t}$ = cos$t$ + $i$ sin$t$ as describing a point in the plane that is moving in time. How does it move? Since $|e^{i t}|$ = 1 for every $t,$ the point moves along the unit circle. In fact, from looking at the real and imaginary parts separately, $x$ = cos$t, y$ = sin$t$ we see that $e^{i t}$ is a (complex-valued) parametrization of the circle; the circle is traced out exactly once in the counterclockwise direction as $t$ goes from 0 to 2$π$. We can also think of the vector from the origin to $z$ as rotating counterclockwise about the origin, like a (backwards moving) clock hand.

For our eﬀorts I prefer to work with

$e^{2 π i t}$ = cos 2$πt$ + $i$ sin2$πt$ as the “basic” complex exponential. Via its real and imaginary parts, the complex exponential $e^{2 π i t}$ contains the sinusoids cos 2$πt$ and sin 2$πt,$ each of frequency 1 Hz. If you like, including the 2$π$ or not is the diﬀerence between working with frequency in units of Hz, or cycles per second, and “angular frequency” in units of radians per second. With the 2$π,$ as $t$ goes from 0 to 1 the point $e^{2 π i t}$ traces out the unit circle exactly once (one cycle) in a counterclockwise direction. The units in the exponential $e^{2 π i t}$ are (as they are in cos 2$πt$ and sin 2$πt)$

$$
e^{2 π r a d i a n s/c y c l e·i·1 c y c l e s/s e c·t s e c} .
$$

Without the 2$π$ the units in $e^{i t}$ are

$$
e^{i·1 r a d i a n s/s e c·t s e c} .
$$

We can always pass easily between the “complex form” of a sinusoid as expressed by a complex exponential, and the real signals as expressed through sines and cosines. But for many, many applications, calculations, prevarications, etc., it is far easier to stick with the complex representation. As I said earlier in these notes, if you have philosophical trouble using complex entities to represent real entities the best advice I can give you is to get over it.

We can now feel free to change the amplitude, frequency, and to include a phase shift. The general (real) sinusoid is of the form, say, $A$ sin(2$πνt$ + $φ);$ the amplitude is $A,$ the frequency is $ν$ (in Hz) and the phase is $φ$. (We’ll take $A$ to be positive for this discussion.) The general complex exponential that includes this information is then

$$
Ae^{i(2 π ν t+φ)} .
$$

Note that $i$ is multiplies the entire quantity 2$πνt+φ$. The term phasor is often used to refer to the complex exponential $e^{2 π i ν t}$.

And what is $Ae^{i(2 π ν t+φ)}$ describing as $t$ varies? The magnitude is $|Ae^{i(2 π i ν t+φ)}|$ = $|A|$ = $A$ so the point is moving along the circle of radius $A$. Assume for the moment that $ν$ is positive — we’ll come back to negative frequencies later. Then the point traces out the circle in the counterclockwise direction at a rate of $ν$ cycles per second — 1 second is $ν$ times around (including the possibility of a fractional number of times around). The phase $φ$ determines the starting point on the circle, for at $t$ = 0 the point is $Ae^{i φ}$. In fact, we can write

$$
Ae^{i(2 π ν t+φ)} = e^{2 π i ν t} Ae^{i φ}
$$

and think of this as the (initial) vector $Ae^{i φ}$ set rotating at a frequency $ν$ Hz through multiplication by the time-varying phasor $e^{2 π i ν t}$.

What happens when $ν$ is negative? That simply reverses the direction of motion around the circle from counterclockwise to clockwise. The catch phrase is just so: positive frequencies means counterclockwise rotation and negative frequencies means clockwise rotation. Now, we can write a cosine, say, as cos 2$πνt$ = $\frac{e^{2 π i ν t}+e^{−2 π i ν t}}{2}$ and one sees this formula interpreted through statements like “a cosine is the sum of phasors of positive and negative frequency”, or similar phrases. The fact that a cosine is made up of a positive and negative frequency, so to speak, is important for some analytical considerations, particularly having to do with the Fourier transform (and we’ll see this phenomenon more generally), but I don’t think there’s a geometric interpretation of negative frequencies without appealing to the complex exponentials that go with real sines and cosines —“negative frequency” is clockwise rotation of a phasor, period.

Sums of sinusoids As a brief, ﬁnal application of these ideas we’ll consider the sum of two sinusoids of the same frequency.3 In real terms, the question is what one can say about the superposition of two signals $A_{1}$ sin(2$πνt$ + $φ_{1})$ + $A_{2}$ sin(2$πνt$ + $φ_{2}).$ Here the frequency is the same for both signals but the amplitudes and phases may be diﬀerent.

If you answer too quickly you might say that a phase shift between the two terms is what leads to beats.

Wrong. Perhaps physical considerations (up to you) can lead you to conclude that the frequency of the sum is again $ν$. That’s right, but it’s not so obvious looking at the graphs of the individual sinusoids and trying to imagine what the sum looks like, e.g., (see graph below):

![Figure on page 417](figures/p417.png)

Figure A.1: Two sinusoids of the same frequency. What does their sum look like?

3 The idea for this example comes from A Digital Signal Processing Primer by K. Stieglitz

An algebraic analysis based on the addition formulas for the sine and cosine does not look too promising either. But it’s easy to see what happens if we use complex exponentials.

Consider

$$
A_{1}e^{i(2 π ν t+φ 1)} + A_{2}e^{i(2 π ν t+φ 2)}
$$

whose imaginary part is the sum of sinusoids, above. Before messing with the algebra, think geometrically in terms of rotating vectors. At $t$ = 0 we have the two vectors from the origin to the starting points, $z_{0}$ = $A_{1}e^{i φ 1}$ and $w_{0}$ = $A_{2}e^{i φ 2}$. Their sum $z_{0}$ + $w_{0}$ is the starting point (or starting vector) for the sum of the two motions. But how do those two starting vectors move? They rotate together at the same rate, the motion of each described by $e^{2 π i ν t}z_{0}$ and $e^{2 π i ν t}w_{0},$ respectively. Thus their sum also rotates at that rate — think of the whole parallelogram (vector sum) rotating rigidly about the vertex at the origin. Now mess with the algebra and arrive at the same result:

$$
A_{1}e^{i(2 π ν t+φ 1)} + A_{2}e^{i(2 π ν t+φ 2)} = e^{2 π i ν t}(A_{1}e^{i φ 1} + A_{2}e^{i φ 2}).
$$

And what is the situation if the two exponentials are “completely out of phase”?

Of course, the simple algebraic manipulation of factoring out the common exponential does not work if the frequencies of the two terms are diﬀerent. If the frequencies of the two terms are diﬀerent . . . now that gets interesting.
