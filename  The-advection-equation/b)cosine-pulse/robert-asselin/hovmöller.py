import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# Load data
# ----------------------------
data_analytic = np.loadtxt("analytic.txt")
data_leapfrog = np.loadtxt("leapfrog_RA_CFL_0.90.txt")
data2_leapfrog = np.loadtxt("leapfrog_RA2_CFL_0.90.txt")
data3_leapfrog = np.loadtxt("leapfrog_RA3_CFL_0.90.txt")



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
fig, axs = plt.subplots(1, 4, figsize=(9, 3.4), sharey=True, sharex=True, gridspec_kw={"width_ratios": [1, 1, 1, 0.15]})


plt.suptitle(r"Cosine-pulse Initial Condition, Robert-Asselin ($\mu=0.9$)", fontsize=15)

# --- Row 0: Analytic ---
ax = axs[0]
im = ax.imshow(data_leapfrog,
               origin='lower',
               aspect='auto',
               vmin=-1, vmax=1,
               extent=extent_numerical,
               cmap="seismic")

ax.set_title(rf"Leapfrog ($\gamma=0.1$)")
ax.set_ylabel(r"$t$ [arb. time unit]")
ax.set_xlabel(r"$x$ [arb. length unit]")

# --- Row 1: Leapfrog, gamma=0.1 ---
ax = axs[1]
im = ax.imshow(data2_leapfrog,
               origin='lower',
               aspect='auto',
               vmin=-1, vmax=1,
               extent=extent_numerical,
               cmap="seismic")

ax.set_title(rf"Leapfrog ($\gamma=0.05$)")
ax.set_xlabel(r"$x$ [arb. length unit]")

# --- Row 1: Leapfrog, gamma=0.1 ---
ax = axs[2]
im = ax.imshow(data3_leapfrog,
               origin='lower',
               aspect='auto',
               vmin=-1, vmax=1,
               extent=extent_numerical,
               cmap="seismic")

ax.set_title(rf"Leapfrog ($\gamma=0.01$)")
ax.set_xlabel(r"$x$ [arb. length unit]")


ax.set_ylim(0,min([max(t),max(t_numerical)]))
ax.set_ylim(0,1.7)

ax = axs[3]
fig.colorbar(im, ax=axs[3], pad=0,  extend="both", fraction=1,label=r"$u(x,t)$ [arb. unit]")
ax.axis("off")




# ----------------------------
# Layout + Save
# ----------------------------
plt.tight_layout()

output_dir = "../../The-advection-equation-report/Figures"
os.makedirs(output_dir, exist_ok=True)

plt.savefig(f"{output_dir}/cosinepulse-RA-hovmoller.png", dpi=300)
plt.show()