import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PARAMETERS (fixed)
# -----------------------------
L = 1.0
Nx = 150
dx = L / Nx

g = 1
H = 1
c = np.sqrt(g * H)

t_final = 0.4

x = np.linspace(0, L, Nx)

# -----------------------------
# DERIVATIVE MATRIX (CENTERED)
# -----------------------------
Dx = np.zeros((Nx, Nx))
for i in range(1, Nx-1):
    Dx[i, i+1] = 1/(2*dx)
    Dx[i, i-1] = -1/(2*dx)

I = np.eye(Nx)

# -----------------------------
# FUNCTION: RUN SIMULATION
# -----------------------------
def run_sim(mu):

    dt = mu * dx / c
    Nt = int(t_final / dt)

    # initial condition
    u_nm1 = np.zeros(Nx)
    h_nm1 = np.zeros(Nx)

    for i in range(Nx):
        if 0.4 < x[i] < 0.6:
            h_nm1[i] = 0.5 + 0.5*np.cos(10*np.pi*(x[i]-0.5))

    # matrix depends on dt → rebuild!
    A = np.block([
        [I, dt * g * Dx],
        [dt * H * Dx, I]
    ])

    # Euler step
    u_n = u_nm1 - dt * g * (Dx @ h_nm1)
    h_n = h_nm1 - dt * H * (Dx @ u_nm1)

    H_store = np.zeros((Nt, Nx))

    # time loop
    for n in range(Nt):

        RHS_u = u_nm1 - dt * g * (Dx @ h_nm1)
        RHS_h = h_nm1 - dt * H * (Dx @ u_nm1)

        RHS = np.concatenate([RHS_u, RHS_h])

        sol = np.linalg.solve(A, RHS)

        u_np1 = sol[:Nx]
        h_np1 = sol[Nx:]

        u_nm1, u_n = u_n, u_np1
        h_nm1, h_n = h_n, h_np1

        H_store[n, :] = h_n

    return H_store, dt, Nt

# -----------------------------
# CFL VALUES
# -----------------------------
mus = [0.5, 1.0, 2.0, 5.0]

# -----------------------------
# PLOT
# -----------------------------
fig, axes = plt.subplots(1, 3, figsize=(10,3), sharey=True)

cmap = plt.cm.YlOrBr.copy()
cmap.set_over('black')
cmap.set_under('black')

vmin = -0.15
vmax = 1.15

for ax, mu in zip(axes, mus):

    H_store, dt, Nt = run_sim(mu)

    im = ax.imshow(H_store,
                   aspect=2.8,
                   cmap=cmap,
                   origin='lower',
                   extent=[0, L, 0, Nt*dt],
                   vmin=vmin,
                   vmax=vmax)

    ax.set_title(fr'$\mu={mu}$')
    ax.set_xlabel('x [arb. unit]')

axes[0].set_ylabel('t [arb. unit]')

# shared colorbar
fig.colorbar(im, ax=axes.ravel().tolist(),
             label='h(x,t)  [arb. unit]', extend='both')

#plt.suptitle('Semi-implicit SWE: effect of CFL                           ', fontsize=15)
plt.savefig("Figures/sol.png", dpi=300)
plt.show()