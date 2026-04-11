import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# Load data
# ----------------------------
data_analytic = np.loadtxt("analytic.txt")
data_1_leapfrog = np.loadtxt("leapfrog_CFL_1.00.txt")
data_11_leapfrog = np.loadtxt("leapfrog_CFL_1.10.txt")
data_9_leapfrog = np.loadtxt("leapfrog_CFL_0.90.txt")

data_1_upwind = np.loadtxt("upwind_CFL_1.00.txt")
data_11_upwind = np.loadtxt("upwind_CFL_1.10.txt")
data_9_upwind = np.loadtxt("upwind_CFL_0.90.txt")



leapfrog_data = [data_9_leapfrog, data_1_leapfrog, data_11_leapfrog]
upwind_data = [data_9_upwind, data_1_upwind, data_11_upwind]
CFL_values = [0.9, 1.0, 1.1]

# ----------------------------
# Parameters
# ----------------------------
Nt, Nx = data_analytic.shape
Nt_11, Nx_11= data_11_leapfrog.shape
Nt_09, Nx_09 = data_9_leapfrog.shape

delX = 0.02
delt_10 = 0.02
delt_11 = 1.1*0.02
delt_09 = 0.9*0.02


t_10 = np.arange(0, Nt * delt_10, delt_10/10)
t_11 = np.arange(0, Nt_11 * delt_11, delt_11/10)
t_09 = np.arange(0, Nt_09 * delt_09, delt_09/10)
t_values = [t_09, t_10, t_11]

# Correct extent 
extent_10 = [0, Nx * delX, 0, Nt * delt_10]
extent_11 = [0, Nx * delX, 0, Nt_11 * delt_11]
extent_09 = [0, Nx * delX, 0, Nt_09 * delt_09]
extent_values = [extent_09, extent_10, extent_11]

# Propagation line (c = 1, periodic domain)
x_line_10 = (0.5 + t_10) % 1.0
x_line_11 = (0.5 + t_11) % 1.0
x_line_09 = (0.5 + t_09) % 1.0
x_values = [x_line_09, x_line_10, x_line_11]


# ----------------------------
# Plot
# ----------------------------
fig, axs = plt.subplots(3, 3, figsize=(9, 9), sharey=True, sharex=True)
plt.suptitle("Cosine Initial Condition", fontsize=15)

# --- Row 0: Analytic ---
for col in range(3):
    ax = axs[0, col]
    if col == 0:
        im = ax.imshow(data_analytic,
            origin='lower',
            aspect='auto',
            vmin=-1.01, vmax=1.01,
            extent=extent_values[1],
            cmap="coolwarm"
        )
        im.cmap.set_under("white")
        im.cmap.set_over("white")
        ax.scatter(x_line_10, t_10, s=0.3, color="black")
        ax.set_title("Analytic")
        ax.set_ylabel(r"$t$ [arb. time unit]")
    else:
        ax.axis("off")
        if col == 1:
            
            fig.colorbar(im, ax=ax, orientation="vertical", fraction=1,label=r"$u(x,t)$ [arb. unit]", extend="both", pad=0)
     

  

# --- Row 1: Leapfrog ---
for col in range(3):
    ax = axs[1, col]
    im = ax.imshow(
        leapfrog_data[col],
        origin='lower',
        aspect='auto',
        vmin=-1.01, vmax=1.01,
        extent=extent_values[col],
        cmap="coolwarm"
    )
    im.cmap.set_under("white")
    im.cmap.set_over("white")       
    ax.scatter(x_values[col], t_values[col], s=0.3, color="black")
    ax.set_title(rf"Leapfrog $\mu$ = {CFL_values[col]}")
    if col == 0:
        ax.set_ylabel(r"$t$ [arb. time unit]")

# --- Row 2: Upwind ---
for col in range(3):
    ax = axs[2, col]
    im = ax.imshow(
        upwind_data[col],
        origin='lower',
        aspect='auto',
        vmin=-1.01, vmax=1.01,
        extent=extent_values[col],
        cmap="coolwarm"
    )
    im.cmap.set_under("white")
    im.cmap.set_over("white")   
    ax.scatter(x_values[col], t_values[col], s=0.3, color="black")
    ax.set_title(rf"Upwind $\mu$ = {CFL_values[col]}")
    ax.set_xlabel(r"$x$ [arb. length unit]")
    ax.set_ylim(0,min([max(t_10),max(t_11),max(t_09)]))
    if col == 0:
        ax.set_ylabel(r"$t$ [arb. time unit]")

# ----------------------------
# Layout + Save
# ----------------------------
plt.tight_layout()

output_dir = "../The-advection-equation-report/Figures"
os.makedirs(output_dir, exist_ok=True)

plt.savefig(f"{output_dir}/cosine-hovmoller.png", dpi=300)
plt.show()