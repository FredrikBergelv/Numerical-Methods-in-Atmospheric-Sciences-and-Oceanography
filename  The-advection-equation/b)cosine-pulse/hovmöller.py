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

t = np.arange(0, Nt * delt, delt/10)
t_numerical = np.arange(0, Nt_numerical * delt_numerical, delt_numerical/10)


# Correct extent 
extent = [0, Nx * delX, 0, Nt * delt]
extent_numerical = [0, Nx * delX, 0, Nt_numerical * delt_numerical]


# Propagation line (c = 1, periodic domain)
x_line = (0.5 + t) % 1.0
x_line_numerical = (0.5 + t_numerical) % 1.0



# ----------------------------
# Plot
# ----------------------------
fig, axs = plt.subplots(1, 4, figsize=(9, 3.3), sharey=True, sharex=True, gridspec_kw={"width_ratios": [1, 1, 1, 0.15]})


plt.suptitle(r"Cosine-pulse Initial Condition ($\mu=0.9$)", fontsize=15)

# --- Row 0: Analytic ---
ax = axs[0]
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
ax = axs[1]
im = ax.imshow(data_leapfrog,
               origin='lower',
               aspect='auto',
               vmin=-1, vmax=1,
               extent=extent_numerical,
               cmap="seismic")

#ax.scatter(x_values[col], t_values[col], s=0.3, color="black")
ax.set_title(rf"Leapfrog")
ax.set_xlabel(r"$x$ [arb. length unit]")


# --- Row 2: Upwind ---
ax = axs[2]
im = ax.imshow(data_upwind,
               origin='lower',
               aspect='auto',
               extent=extent_numerical,
               vmin=-1, vmax=1,
               cmap="seismic")

#ax.scatter(x_values[col], t_values[col], s=0.3, color="black")
ax.set_title(rf"Upwind")
ax.set_xlabel(r"$x$ [arb. length unit]")
ax.set_ylim(0,min([max(t),max(t_numerical)]))
ax.set_ylim(0,1.7)

ax = axs[3]
fig.colorbar(im, ax=axs[3], pad=0, fraction=1,  extend="both", label=r"$u(x,t)$ [arb. unit]")
ax.axis("off")




# ----------------------------
# Layout + Save
# ----------------------------
plt.tight_layout()

output_dir = "../The-advection-equation-report/Figures"
os.makedirs(output_dir, exist_ok=True)

plt.savefig(f"{output_dir}/cosinepulse-hovmoller.png", dpi=300)
plt.show()