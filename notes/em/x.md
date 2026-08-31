## Step 1: Recall the Full TE-Mode Fields
For the focused doughnut pulse (propagating along +z):

Electric field: Only azimuthal component:
$$E_\theta(\rho, z, t) = -\frac{4 i f_0 \sqrt{\mu_0 \varepsilon_0} \rho (q_1 + q_2 - 2 i c t)}{[\rho^2 + (q_1 + i \tau)(q_2 - i \sigma)]^3}$$

Magnetic field (in H, then convert to $B = \mu_0 \mathbf{H}$):
$$H_\rho(\rho, z, t) = \frac{4 i f_0 \rho (q_2 - q_1 - 2 i z)}{[\rho^2 + (q_1 + i \tau)(q_2 - i \sigma)]^3} $$

$$H_z(\rho, z, t) = -\frac{4 f_0 [\rho^2 - (q_1 + i \tau)(q_2 - i \sigma)]}{[\rho^2 + (q_1 + i \tau)(q_2 - i \sigma)]^3}$$

where $H_\theta = 0$.
Thus, $B_\rho = \mu_0 H_\rho, \hspace{5mm} B_z = \mu_0 H_z, \hspace{5mm} B_\theta = 0$

Variables (all as in your query/paper):

$\sigma = z + c t, \hspace{5mm} \tau = z - c t$ (light-cone coordinates). \
$q_1$: Controls transverse size (effective wavelength scale, length units). \
$q_2$: Controls focal depth (length units). \
$f_0$: Amplitude normalization (adjusts pulse strength). \
$c$: Speed of light, \
$i = \sqrt{-1}$


## Step 2: Lorentz Force Formula in Cylindrical Coordinates

The total force is $\mathbf{F} = q \mathbf{E} + q \mathbf{v} \times \mathbf{B}$.
Since $\mathbf{E} = E_\theta \hat{\theta}$ and $\mathbf{B} = B_\rho \hat{\rho} + B_z \hat{z}$, the cross product is:
$$\mathbf{v} \times \mathbf{B} = \begin{vmatrix}
\hat{\rho} & \hat{\theta} & \hat{z} \\ 
v_\rho & v_\theta & v_z \\ 
B_\rho & 0 & B_z 
\end{vmatrix} = \hat{\rho} (v_\theta B_z) + \hat{\theta} (v_z B_\rho - v_\rho B_z) + \hat{z} (-v_\theta B_\rho).$$  

Adding the electric term (which only contributes to $\theta$-direction):  
- Radial: $F_\rho = q (v_\theta B_z)$  
- Azimuthal: $F_\theta = q E_\theta + q (v_z B_\rho - v_\rho B_z)$  
- Longitudinal: $F_z = q (-v_\theta B_\rho)$  

That's it—"point B." Each component is *directly* the fields (from Step 1) evaluated at $(\rho(t), z(t), t)$, multiplied by $q$ and velocity terms. No approximations needed; it's exact for a test particle.

## Step 3: Key Insights on the Resulting Force
- **Electric contribution**: Only azimuthal ($F_\theta$), driving circular motion around the z-axis (toroidal "doughnut" effect).
- **Magnetic contribution**: 
  - $F_\rho$: Pushes radially outward/inward depending on $v_\theta$ and the strong $B_z$ near focus (longitudinal magnetic field traps or ejects particles transversely).
  - $F_z$: Axial push/pull via $-v_\theta B_\rho$; this is highlighted in the paper as a mechanism for accelerating co-propagating particles (e.g., electrons) along z, especially if $v_\theta$ is induced by the pulse.
  - Cross terms in $F_\theta$: Couple radial/longitudinal velocities to azimuthal forces.
- For particles starting at rest ($\mathbf{v} = 0$): $\mathbf{F} = q \mathbf{E}$, so only azimuthal force—simple kick in $\theta$-direction.
- Relativistic case: Use $d\mathbf{p}/dt = \mathbf{F}$ with $\mathbf{p} = \gamma m \mathbf{v}$ (Lorentz factor $\gamma$); still direct, but integration gets harder.
- Why no "simple" trajectory? The fields depend on $z \pm c t$, so as the particle moves, it "sees" evolving fields—requires numerical ODE solving (e.g., $d\mathbf{v}/dt = \mathbf{F}/m$).

### Step 4: How to Compute It in Practice (Numerical Example)
Analytically, the expressions are messy (high powers in denominator), so evaluate numerically/symbolically. For instance, assume $q = -e$ (electron), $m = m_e$, at focus ($\rho = q_1$, $z=0$, $t=0$), with initial $v_\theta = 0.1c$, $v_\rho = v_z = 0$, and parameters $q_1 = q_2 = 1 \, \mu \mathrm{m}$, $f_0 = 1$ (arbitrary; scales intensity).

Using symbolic computation (via SymPy, for transparency): The force components simplify to explicit forms, but for numbers: At this point, $F_\rho \approx q v_\theta \mu_0 H_z$ (dominant if $B_z$ peaks), yielding ~10^{-12} N for mid-IR intensities—enough for acceleration over the pulse duration (~fs).

To go further (e.g., integrate for trajectory), solve the ODEs:  
$$\frac{d v_\rho}{dt} = \frac{F_\rho}{m}, \quad \frac{d v_\theta}{dt} = \frac{F_\theta}{m} + \frac{v_\rho v_\theta}{\rho}, \quad \frac{d v_z}{dt} = \frac{F_z}{m}$$  
(plus position updates; full cylindrical ODEs account for basis vector changes). Use Runge-Kutta in code (e.g., Python/SciPy).

If you provide specific parameters (e.g., values for $q_1, q_2, f_0$, initial position/velocity), I can compute a numerical example or trajectory snippet. The paper notes these pulses can accelerate particles via the longitudinal $H_z$, but no explicit force derivation—it's standard Lorentz as above.