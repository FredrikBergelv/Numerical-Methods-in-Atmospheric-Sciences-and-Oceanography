import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# Load data
# ----------------------------
h_analytic = np.loadtxt("a)unstaggered/h-analytic.txt")
h_leapfrog = np.loadtxt("a)unstaggered/h-leapfrog.txt")

u_analytic = np.loadtxt("a)unstaggered/u-analytic.txt")
u_leapfrog = np.loadtxt("a)unstaggered/u-leapfrog.txt")

# ----------------------------
# Parameters
# ----------------------------
Nt, Nx = h_analytic.shape
Nt_numerical, Nx__numerical = h_leapfrog.shape

dx = 0.025
dt_numerical = 0.9*0.025
t_numerical = np.arange(0, Nt_numerical * dt_numerical, dt_numerical/10)


# Correct extent 
extent_numerical = [0, Nx * dx, 0, Nt_numerical * dt_numerical]
extent = [0, Nx * dx, 0, Nt_numerical * dt_numerical]


# ----------------------------
# Plot
# ----------------------------
fig, axs = plt.subplots(1, 7, figsize=(12, 5), sharey=True, sharex=True, gridspec_kw={"width_ratios": [1, 1, 0.15, 0.2, 1, 1, 0.15]})


plt.suptitle(r"Unstaggered grid ($\mu = 0.9$)", fontsize=15)

# --- Row 0: Analytic ---
ax = axs[0]

im = ax.imshow(h_analytic,
               origin='lower',
               aspect='equal',
               extent=extent,
               vmin=-1, vmax=1,
               cmap="seismic")


ax.set_title("Analytic")
ax.set_ylabel(r"$t$ [arb. time unit]")
ax.set_xlabel(r"$x$ [arb. length unit]")

# --- Row 1: Leapfrog ---
ax = axs[1]
im = ax.imshow(h_leapfrog,
               origin='lower',
               aspect='equal',
               vmin=-1, vmax=1,
               extent=extent_numerical,
               cmap="seismic")


ax.set_title(rf"Leapfrog")
ax.set_xlabel(r"$x$ [arb. length unit]")

# --- Row 2: colorbar ---
ax = axs[2]

fig.colorbar(im, ax=axs[2], pad=0, fraction=1, shrink=0.8,  extend="both", label=r"$h(x,t)$ [arb. length unit]")
ax.axis("off")

ax = axs[3]
ax.axis("off")


# --- Row 3: Analytic ---
ax = axs[4]

im = ax.imshow(u_analytic,
               origin='lower',
               aspect='equal',
               extent=extent,
               vmin=-1, vmax=1,
               cmap="BrBG")


ax.set_title("Analytic")
ax.set_xlabel(r"$x$ [arb. length unit]")

# --- Row 4: Leapfrog ---
ax = axs[5]
im = ax.imshow(u_leapfrog,
               origin='lower',
               aspect='equal',
               vmin=-1, vmax=1,
               extent=extent_numerical,
               cmap="BrBG")


ax.set_title(rf"Leapfrog")
ax.set_xlabel(r"$x$ [arb. length unit]")
ax.set_xticks([0, 0.5, 1])
ax.set_yticks([0, 0.5, 1, 0.5, 1.0, 1.5, 2.0])
ax.set_ylim(0,2)

# --- Row 5: colorbar ---
ax = axs[6]

fig.colorbar(im, ax=axs[6], pad=0, fraction=1, shrink=0.8,  extend="both", label=r"$u(x,t)$ [arb. velocity unit]")
ax.axis("off")




# ----------------------------
# Layout + Save
# ----------------------------
output_dir = "The-shallow-water-equation-report/Figures"
os.makedirs(output_dir, exist_ok=True)

plt.savefig(f"{output_dir}/unstaggered-hovmoller.png", dpi=300)
plt.show()