# Line and Surface Integrals

## Line Integrals
Line integrals are typically defined over a vector field $\mathbf{F}(x, y, z) = (P, Q, R)$ along a curve $C$. 


The standard form of a line integral is:
$$\int_C \mathbf{F} \cdot d\mathbf{r} = \int_C (P \cdot dx + Q \cdot dy + R \cdot dz)$$ 

where 
- $\mathbf{r}(t) = (x(t), \hspace{0.5mm} y(t), \hspace{0.5mm} z(t))$ parameterizes the curve $C$, and
- $d\mathbf{r} = (dx, \hspace{0.5mm} dy, \hspace{0.5mm} dz)$ is the differential tangent vector along the curve.

### Why a vector function? 
The vector field $\mathbf{F}$ represents a quantity with both _magnitude_ **and** _direction_ (e.g., force, velocity, or electric field) at each point in space. The line integral measures how much the vector field aligns with the direction of the curve $C$.  
  - For example, in physics, this often corresponds to work done by a force field along a path, where the dot product $\mathbf{F} \cdot d\mathbf{r}$ picks out the component of $\mathbf{F}$ parallel to the curve’s tangent vector. 


### Scalar line integrals exist too.
It's worth noting that line integrals can also be defined over scalar functions, e.g., $\int_C f \, ds$, where $f(x, y, z)$ is a scalar field (like temperature or density), and $ds$ is the arc length element. This measures the accumulation of the scalar quantity along the curve's length.

### Example: Work Done by a Force Field
Compute the work done by the force field $\mathbf{F} = (y, \, x, \, 0)$ along the path $C$ from $(0, 0, 0)$ to $(1, 1, 0)$ along the curve $\mathbf{r}(t) = (t, \, t, \, 0)$ for $t \in [0, 1]$.

**Solution:**
The work is given by $W = \int_C \mathbf{F} \cdot d\mathbf{r}$.

First, compute $d\mathbf{r}$:
$$d\mathbf{r} = \frac{d\mathbf{r}}{dt} dt = (1, \, 1, \, 0) \, dt$$

Along the curve, $x = t$ and $y = t$, so $\mathbf{F} = (t, \, t, \, 0)$.

The dot product is:
$$\mathbf{F} \cdot d\mathbf{r} = (t)(1) + (t)(1) + (0)(0) = 2t \, dt$$

Integrating:
$$W = \int_0^1 2t \, dt = \left[ t^2 \right]_0^1 = 1$$

## Surface Integrals

Surface integrals over vector fields are typically of the form:

$$\iint_S \mathbf{F} \cdot d\mathbf{A} = \iint_S \mathbf{F} \cdot \mathbf{n} \times dA,$$
where 
- $\mathbf{F}$ is a vector field,
- $\mathbf{n}$ is the unit normal vector to the surface $S$, and
- $d\mathbf{A} = \mathbf{n} \times dA$ is the vector area element.

### Why a vector function?
Surface integrals over vector fields are often used to compute flux—the amount of a vector field (e.g., fluid flow, magnetic field) passing **through** a surface. The dot product $\mathbf{F} \cdot \mathbf{n}$ measures the component of the vector field **perpendicular** to the surface, which is relevant for flux calculations.

### Scalar surface integrals exist too.
Similar to line integrals, surface integrals can be defined over scalar functions, e.g., $\iint_S f \, dA$, where $f$ is a scalar field, and $dA$ is the scalar area element. This computes the total scalar quantity (e.g., mass or charge) over the surface area. 

### Example: Flux Through a Surface
Compute the flux of the vector field $\mathbf{F} = (0, \, 0, \, z)$ through the surface $S$, where $S$ is the portion of the paraboloid $z = 1 - x^2 - y^2$ above the $xy$-plane, with outward (upward) normal.

**Solution:**
The flux is $\Phi = \iint_S \mathbf{F} \cdot d\mathbf{A}$.

The surface is given by $z = f(x, y) = 1 - x^2 - y^2$. To find the normal vector, think of it this way: we can parameterize the surface using $x$ and $y$ directly as $\mathbf{r}(x, y) = (x, \, y, \, f(x,y))$. The two tangent vectors are then $\mathbf{r}_x = (1, \, 0, \, \frac{\partial f}{\partial x})$ and $\mathbf{r}_y = (0, \, 1, \, \frac{\partial f}{\partial y})$. Their cross product gives a normal vector:
$$\mathbf{r}_x \times \mathbf{r}_y = \begin{vmatrix} \hat{i} & \hat{j} & \hat{k} \\ 1 & 0 & \frac{\partial f}{\partial x} \\ 0 & 1 & \frac{\partial f}{\partial y} \end{vmatrix} = \left( -\frac{\partial f}{\partial x}, \, -\frac{\partial f}{\partial y}, \, 1 \right)$$
This points "upward" (positive $z$-component). For our paraboloid, $\frac{\partial f}{\partial x} = -2x$ and $\frac{\partial f}{\partial y} = -2y$, so:
$$\mathbf{N} = \left( -(-2x), \, -(-2y), \, 1 \right) = (2x, \, 2y, \, 1)$$ 

The vector area element is simply $d\mathbf{A} = \mathbf{N} \, dx \, dy$ — the cross product already encodes both the direction (normal) and the area scaling factor. So:
$$d\mathbf{A} = (2x, \, 2y, \, 1) \, dx \, dy$$

The dot product with $\mathbf{F} = (0, \, 0, \, z) = (0, \, 0, \, 1 - x^2 - y^2)$ is:
$$\mathbf{F} \cdot d\mathbf{A} = (0)(2x) + (0)(2y) + (1 - x^2 - y^2)(1) = (1 - x^2 - y^2) \, dx \, dy$$

The region of integration is the disk $x^2 + y^2 \leq 1$. Converting to polar coordinates ($x = r\cos\theta$, $y = r\sin\theta$):
$$\Phi = \int_0^{2\pi} \int_0^1 (1 - r^2) \, r \, dr \, d\theta = 2\pi \int_0^1 (r - r^3) \, dr = 2\pi \left[ \frac{r^2}{2} - \frac{r^4}{4} \right]_0^1 = 2\pi \cdot \frac{1}{4} = \frac{\pi}{2}$$

## Volume Integrals
Volume integrals are typically defined over a scalar function $f(x, y, z)$ in a region $V$:

$$ \iiint_V f dV $$ 
where

- $dV$ is the volume element (e.g., $dV = (dx, \hspace{0.5mm} dy, \hspace{0.5mm} dz)$ in Cartesian coordinates).

### Why a scalar function?
  - Volume integrals are often used to compute aggregate quantities like total mass, charge, or energy within a 3D region. These quantities are inherently scalar, as they represent a total amount without directional dependence. 
  - The volume element $dV$ is a scalar, and integrating a scalar function over a volume naturally yields a scalar result, which aligns with the physical interpretation of summing up a quantity over a region. 
  - For example, if $f(x, y, z)$ is the density of an object, $\iiint_V f \, dV$ gives the total mass.


### Can volume integrals involve vector functions?
  - While less common, volume integrals can be defined over vector fields in specific contexts. For instance, you might integrate each component of a vector field $\mathbf{F} = (P, Q, R)$ separately over a volume:
  $$\iiint_V \mathbf{F} \, dV = \left( \iiint_V P \, dV, \iiint_V Q \, dV, \iiint_V R \, dV \right).$$
  - This results in a vector, where each component is a scalar volume integral. Such integrals are used in applications like computing the total momentum of a fluid (where $\mathbf{F}$ is the momentum density). However, this is less common than scalar volume integrals because physical quantities integrated over a volume are often scalar (e.g., mass, energy), and vector volume integrals don't have a direct geometric interpretation like flux or work.

### Example: Total Charge in a Region
A charge density is given by $\rho(x, y, z) = x^2 + y^2$ in the region $V$ defined by the cylinder $x^2 + y^2 \leq 1$, $0 \leq z \leq 2$. Find the total charge $Q$.

**Solution:**
The total charge is $Q = \iiint_V \rho \, dV$.

Using cylindrical coordinates $(r, \theta, z)$ where $x = r\cos\theta$, $y = r\sin\theta$, and $dV = r \, dr \, d\theta \, dz$:
$$\rho = x^2 + y^2 = r^2$$

The integral becomes:
$$Q = \int_0^2 \int_0^{2\pi} \int_0^1 r^2 \cdot r \, dr \, d\theta \, dz = \int_0^2 dz \int_0^{2\pi} d\theta \int_0^1 r^3 \, dr$$

Evaluating each integral:
$$Q = (2)(2\pi) \left[ \frac{r^4}{4} \right]_0^1 = 4\pi \cdot \frac{1}{4} = \pi$$

<br/>


#### Going deeper into **Surface Integrals**:

## What is $dA$ in Surface Integrals?

### Explanation
In a surface integral, $dA$ (or sometimes written as $dS$) is the infinitesimal scalar area element on a surface $S$. It represents the area of an infinitesimally small patch of the surface at a given point. Think of it as a tiny piece of the surface’s area, used to sum up quantities (like a scalar field or the flux of a vector field) over the entire surface.

### Geometric Interpretation of $dA$
Imagine the surface $S$ as a curved sheet in 3D space. To compute an integral over $S$, we break the surface into tiny pieces, each approximated as a flat patch. The area of each patch is $dA$, and the integral sums the contributions of these patches. For example:

- For a flat plane, $dA$ might simply be $dx \, dy$ in Cartesian coordinates.
- For a curved surface like a sphere, $dA$ accounts for the curvature and is expressed in terms of the surface’s parameterization or coordinates.

The key is that $dA$ is a scalar quantity representing the area of the infinitesimal patch, independent of the surface’s orientation. The orientation is handled separately (e.g., by $\mathbf{n}$ in vector integrals).

### How is $dA$ Derived?
The expression for $dA$ depends on how the surface is defined. Let’s explore the main ways surfaces are represented and how $dA$ is computed in each case.

#### For a Parametric Surface
A surface $S$ is often parameterized by a vector-valued function $\mathbf{r}(u, v) = (x(u, v), y(u, v), z(u, v))$, where $u$ and $v$ are parameters (like coordinates on the surface). The area element $dA$ comes from the geometry of the surface’s tangent vectors.

Compute the tangent vectors:

$$\mathbf{r}_u = \frac{\partial \mathbf{r}}{\partial u} = \left( \frac{\partial x}{\partial u}, \frac{\partial y}{\partial u}, \frac{\partial z}{\partial u} \right), \quad \mathbf{r}_v = \frac{\partial \mathbf{r}}{\partial v} = \left( \frac{\partial x}{\partial v}, \frac{\partial y}{\partial v}, \frac{\partial z}{\partial v} \right).$$

The vector area element $d\mathbf{A}$ is related to the cross product of these tangent vectors, which gives a normal vector to the surface:

$$\mathbf{r}_u \times \mathbf{r}_v$$

The magnitude of this cross product, $|\mathbf{r}_u \times \mathbf{r}_v|$, gives the area of the parallelogram formed by the tangent vectors corresponding to increments $du$ and $dv$. Thus, the scalar area element is:

$$dA = |\mathbf{r}_u \times \mathbf{r}_v| \hspace{0.5mm} du dv.$$

####  Why Does This Work?
Geometrically, a small rectangle in the $uv$-plane with sides $du$ and $dv$ **maps** to a small parallelogram on the surface with sides $\mathbf{r}_u \, du$ and $\mathbf{r}_v \, dv$. The area of this parallelogram is exactly $|\mathbf{r}_u \times \mathbf{r}_v| \, du \, dv$, from the definition of the cross product's magnitude. Summing these over the surface gives the total area or the integral.
This method is universal for parameterizable surfaces (which covers most cases in vector calculus). If the surface is given implicitly (e.g., $f(x, y, z) = c$), you first need to choose a parameterization, as the implicit form doesn't directly give tangent vectors.

The above is a lot of words, just try to imagine the infinitesimal surface element in your head, morphing itself from a cartesian surface (e.g. rectangle) to a curved surface. You'll see the connection.
