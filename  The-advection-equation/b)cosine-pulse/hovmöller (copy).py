import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# Load data
# ----------------------------
data_analytic = np.loadtxt("analytic.txt")
data_leapfrog = np.loadtxt("leapfrog_CFL_0.90.txt")
data_upwind  = np.loadtxt("upwind_CFL_0.90.txt")

# ----------------------------
# Parameters
# ----------------------------
Nt, Nx = data_analytic.shape
Nt_numerical, Nx__numerical = data_leapfrog.shape

delX = 0.02
delt = 0.02
delt_numerical = 0.9*0.02

t = np.arange(0, Nt * delt, delt)
t_numerical = np.arange(0, Nt_numerical * delt_numerical, delt_numerical)


# Correct extent 
extent = [0, Nx * delX, 0, Nt * delt]
extent_numerical = [0, Nx * delX, 0, Nt_numerical * delt_numerical]


# Propagation line (c = 1, periodic domain)
x_line = (0.5 + t) % 1.0
x_line_numerical = (0.5 + t_numerical) % 1.0



# ----------------------------
# Plot
# ----------------------------
fig, axs = plt.subplots(2, 4, figsize=(9, 5.9), sharey=True, sharex=True, gridspec_kw={"width_ratios": [1, 1, 1, 0.15]})


plt.suptitle(r"Cosine-pulse Initial Condition ($\mu=0.9$)", fontsize=15)

# --- Row 0: Analytic ---
ax = axs[0,0]
im = ax.imshow(data_analytic,
               origin='lower',
               aspect='auto',
               extent=extent,
               vmin=-1, vmax=1,
               cmap="seismic")

#ax.scatter(x_line_10, t_10, s=0.3, color="black")
ax.set_title("Analytic")
ax.set_ylabel(r"$t$ [arb. time unit]")
ax.set_xlabel(r"$x$ [arb. length unit]")

# --- Row 1: Leapfrog ---
ax = axs[0,1]
im = ax.imshow(data_leapfrog,
               origin='lower',
               aspect='auto',
               vmin=-1, vmax=1,
               extent=extent_numerical,
               cmap="seismic")

#ax.scatter(x_values[col], t_values[col], s=0.3, color="black")
ax.set_title(rf"Leapfrog")

# --- Row 2: Upwind ---
ax = axs[0,2]
im = ax.imshow(data_upwind,
               origin='lower',
               aspect='auto',
               extent=extent_numerical,
               vmin=-1, vmax=1,
               cmap="seismic")

#ax.scatter(x_values[col], t_values[col], s=0.3, color="black")
ax.set_title(rf"Upwind")
ax.set_ylim(0,min([max(t),max(t_numerical)]))
ax.set_ylim(0,1.7)

ax = axs[0,3]
fig.colorbar(im, ax=axs[0,3], pad=0, fraction=1,label=r"$u(x,t)$ [arb. unit]")
ax.axis("off")

ax = axs[1,0]
ax.axis("off")

data_analytic_interp = np.zeros_like(data_leapfrog)

for j in range(Nx):
    data_analytic_interp[:, j] = np.interp(
        t_numerical, t, data_analytic[:, j]
    )

# Compute differences
diff_leapfrog = (data_leapfrog - data_analytic_interp) 
diff_upwind   = (data_upwind  - data_analytic_interp) 

ax = axs[1,1]
ax.set_xlabel(r"$x$ [arb. length unit]")
im = ax.imshow(diff_leapfrog,
               origin='lower',
               aspect='auto',
               extent=extent_numerical,
               vmin=-1, vmax=1,
               cmap="PRGn")

ax = axs[1,2]
ax.set_xlabel(r"$x$ [arb. length unit]")
im = ax.imshow(diff_upwind,
               origin='lower',
               aspect='auto',
               extent=extent_numerical,
               vmin=-1, vmax=1,
               cmap="PRGn")

ax = axs[1,3]
fig.colorbar(im, ax=axs[1,3], pad=0, fraction=1,label=r"Error [arb. unit]")


ax.axis("off")






# ----------------------------
# Layout + Save
# ----------------------------
plt.tight_layout()

output_dir = "../The-advection-equation-report/Figures"
os.makedirs(output_dir, exist_ok=True)

#plt.savefig(f"{output_dir}/cosinepulse-hovmoller-error.png", dpi=300)
plt.show()