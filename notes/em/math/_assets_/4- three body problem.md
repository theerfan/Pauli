# Physics Concepts: Three-Body Problem & Electromagnetic Unification

---

## 1. Why is the Three-Body Problem Hard to Solve?

### The Setup

Consider three masses $m_1$, $m_2$, $m_3$ interacting via gravity. The force on mass $i$ from mass $j$ is:

$$
\vec{F}_{ij} = -G \frac{m_i m_j}{|\vec{r}_i - \vec{r}_j|^3} (\vec{r}_i - \vec{r}_j)
$$

For each body, Newton's second law gives:

$$
m_i \frac{d^2 \vec{r}_i}{dt^2} = \sum_{j \neq i} \vec{F}_{ij}
$$

### Why It's Hard

**1. Non-integrability (No Closed-Form Solution)**

The two-body problem has 10 conserved quantities (energy, momentum, angular momentum, center of mass motion) which reduce it to a solvable 1D problem. For three bodies, we still only have 10 conserved quantities, but we need 18 to fully integrate the system (6 coordinates × 3 bodies). This means:

$$
\text{Degrees of freedom} = 18 - 10 = 8 \quad \text{(too many!)}
$$

**2. Chaotic Dynamics**

The system exhibits extreme sensitivity to initial conditions. Two nearly identical starting configurations diverge exponentially:

$$
|\delta \vec{r}(t)| \sim |\delta \vec{r}(0)| \cdot e^{\lambda t}
$$

where $\lambda > 0$ is the Lyapunov exponent. This means tiny measurement errors make long-term prediction impossible.

**3. No Separable Potential**

In the two-body problem, we can transform to center-of-mass coordinates and get a separable Hamiltonian. For three bodies, the potential:

$$
U = -G\left( \frac{m_1 m_2}{r_{12}} + \frac{m_2 m_3}{r_{23}} + \frac{m_1 m_3}{r_{13}} \right)
$$

cannot be separated into independent terms—every body's motion depends on both others simultaneously.

**4. Singularities**

When any two bodies collide ($r_{ij} \to 0$), the potential $U \to -\infty$. These singularities create mathematical and numerical nightmares.

### What We Can Do

- **Numerical integration**: Approximate solutions (but chaos limits prediction horizons)
- **Restricted three-body problem**: One mass is negligible (e.g., spacecraft near Earth-Moon)
- **Special solutions**: Lagrange points, figure-8 orbits, etc.

---

## 2. How Are Electricity and Magnetism the "Same"?

### The Apparent Difference

At first glance, they seem completely different:

| Electric | Magnetic |
|----------|----------|
| Charges exist ($q$) | No monopoles |
| Forces on stationary charges | Forces only on moving charges |
| $\vec{F} = q\vec{E}$ | $\vec{F} = q\vec{v} \times \vec{B}$ |

### The Unification: Special Relativity

The key insight is that **what you call "electric" vs "magnetic" depends on your reference frame**.

Consider a wire with current $I$ (moving charges) and a test charge $q$ moving parallel to the wire with velocity $v$.

**In the lab frame**: The wire is neutral (equal $+$ and $-$ charges), so $\vec{E} = 0$. But there's a magnetic field:

$$
\vec{B} = \frac{\mu_0 I}{2\pi r} \hat{\phi}
$$

The force is purely magnetic: $\vec{F} = q\vec{v} \times \vec{B}$

**In the charge's rest frame**: The charge is stationary, so $\vec{v} = 0$ and magnetic force is zero! But due to length contraction, the charge densities of the moving electrons and stationary protons are different, creating a net electric field. The force is purely electric!

$$
\vec{F}' = q\vec{E}'
$$

Both frames agree on the physical outcome (the force magnitude), but disagree on whether it's "electric" or "magnetic."

### The Electromagnetic Field Tensor

In special relativity, $\vec{E}$ and $\vec{B}$ combine into a single object—the electromagnetic field tensor $F^{\mu\nu}$:

$$
F^{\mu\nu} = \begin{pmatrix}
0 & -E_x/c & -E_y/c & -E_z/c \\
E_x/c & 0 & -B_z & B_y \\
E_y/c & B_z & 0 & -B_x \\
E_z/c & -B_y & B_x & 0
\end{pmatrix}
$$

Under Lorentz transformations, $\vec{E}$ and $\vec{B}$ mix into each other:

$$
E'_\parallel = E_\parallel \qquad B'_\parallel = B_\parallel
$$

$$
E'_\perp = \gamma(E_\perp + \vec{v} \times \vec{B}) \qquad B'_\perp = \gamma\left(B_\perp - \frac{\vec{v} \times \vec{E}}{c^2}\right)
$$

where $\gamma = 1/\sqrt{1 - v^2/c^2}$.

### Why "More the Same" at High Energies?

At high energies (high velocities, $v \to c$):

1. **Lorentz factor $\gamma \to \infty$**: The mixing terms become dominant. A purely electric field in one frame looks like a huge magnetic field in another.

2. **Relativistic invariants**: There are only two Lorentz-invariant quantities:

$$
\vec{E} \cdot \vec{B} = \text{invariant}
$$

$$
|\vec{E}|^2 - c^2|\vec{B}|^2 = \text{invariant}
$$

At high energies, the distinction between $E$ and $B$ becomes increasingly frame-dependent and therefore "unphysical."

3. **Quantum electrodynamics (QED)**: At the quantum level, both electric and magnetic interactions are mediated by the same particle—the photon. The photon doesn't care whether you call the interaction "electric" or "magnetic."

### Summary

Electricity and magnetism are two aspects of **one unified electromagnetic field**. The split into $\vec{E}$ and $\vec{B}$ is an artifact of choosing a reference frame. At low velocities, this split seems natural. At high velocities (high energies), the split becomes arbitrary, revealing their fundamental unity.

$$
\boxed{\text{Electromagnetism} = \text{Electricity} \oplus \text{Magnetism} \quad \text{(unified by relativity)}}
$$
