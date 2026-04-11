import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# Load data
# ----------------------------
hS_leapfrog = np.loadtxt("b)staggered/h-leapfrog-.0125.txt")
h_leapfrog  = np.loadtxt("b)staggered/h-leapfrog-.0250.txt")
hL_leapfrog = np.loadtxt("b)staggered/h-leapfrog-.0500.txt")
h_unstaggered = np.loadtxt("a)unstaggered/h-leapfrog-.0250.txt")

uS_leapfrog = np.loadtxt("b)staggered/u-leapfrog-.0125.txt")
u_leapfrog  = np.loadtxt("b)staggered/u-leapfrog-.0250.txt")
uL_leapfrog = np.loadtxt("b)staggered/u-leapfrog-.0500.txt")
u_unstaggered = np.loadtxt("a)unstaggered/u-leapfrog-.0250.txt")

# ----------------------------
# Parameters
# ----------------------------
dx = 0.025
CFL = 0.45

# time extents
Nt, Nx = h_leapfrog.shape
dt = CFL * dx
extent_h = [0, Nx*dx, 0, Nt*dt]

# resolutions
NxS = hS_leapfrog.shape[1]
extent_hS = [0, NxS*(dx/2), 0, hS_leapfrog.shape[0]*dt/2]

NxL = hL_leapfrog.shape[1]
extent_hL = [0, NxL*(2*dx), 0, hL_leapfrog.shape[0]*dt*2]

# ----------------------------
# Plot
# ----------------------------
fig, axs = plt.subplots(2, 4, figsize=(9, 10), gridspec_kw={"width_ratios":[1,1,1,0.15]}, sharex=True, sharey=True)

plt.suptitle(r"Staggered grid: Comparison of resolutions", fontsize=15)

# ----------------------------
# Row 0: h
# ----------------------------
ax = axs[0,0]
ax.imshow(hS_leapfrog, origin='lower', aspect='equal', extent=extent_hS, cmap="seismic", vmin=-1, vmax=1)
ax.set_title(r"Δx=0.0125")
ax.set_ylabel(r"$t$ [arb. time unit]")

ax = axs[0,1]
ax.imshow(h_leapfrog, origin='lower', aspect='equal', extent=extent_h, cmap="seismic", vmin=-1, vmax=1)
ax.set_title(r"Δx=0.025")

ax = axs[0,2]
im = ax.imshow(hL_leapfrog, origin='lower', aspect='equal', extent=extent_hL, cmap="seismic", vmin=-1, vmax=1)
ax.set_title(r"Δx=0.05")

# colorbar for h
ax = axs[0,3]
cbar_h = fig.colorbar(im, ax=ax, pad=0, fraction=1, shrink=0.8,  extend="both", label=r"$h(x,t)$ [arb. length unit]")
ax.axis("off")

# ----------------------------
# Row 1: u
# ----------------------------
ax = axs[1,0]
ax.imshow(uS_leapfrog, origin='lower', aspect='equal', extent=extent_hS, cmap="BrBG", vmin=-1, vmax=1)
ax.set_title(r"Δx=0.0125")
ax.set_ylabel(r"$t$ [arb. time unit]")
ax.set_xlabel(r"$x$ [arb. length unit]")

ax = axs[1,1]
ax.imshow(u_leapfrog, origin='lower', aspect='equal', extent=extent_h, cmap="BrBG", vmin=-1, vmax=1)
ax.set_title(r"Δx=0.025")
ax.set_xlabel(r"$x$ [arb. length unit]")

ax = axs[1,2]
im = ax.imshow(uL_leapfrog, origin='lower', aspect='equal', extent=extent_hL, cmap="BrBG", vmin=-1, vmax=1)
ax.set_title(r"Δx=0.05")
ax.set_xlabel(r"$x$ [arb. length unit]")

# colorbar for u
ax = axs[1,3]
cbar_u = fig.colorbar(im, ax=ax, pad=0, fraction=1, shrink=0.8,  extend="both", label=r"$u(x,t)$ [arb. velocity unit]")
ax.axis("off")

# ----------------------------
# Layout + Save
# ----------------------------
output_dir = "The-shallow-water-equation-report/Figures"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f"{output_dir}/staggered-hovmoller-comparison.png", dpi=300)
plt.show()