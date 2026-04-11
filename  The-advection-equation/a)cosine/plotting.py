import numpy as np
import matplotlib.pyplot as plt

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

delX = 0.02
x = np.arange(0, Nx*delX, delX)
times_to_plot = [0, 100]

lins = ["-", "-", "-", "-"]

# ----------------------------
# Create 3x3 subplot grid
# ----------------------------
fig, axs = plt.subplots(3, 3, figsize=(9,9), sharey=True)
plt.suptitle("Cosine Initial Condition", fontsize=15)

# --- Row 0: Analytic ---
for col in range(3):
    ax = axs[0, col]
    if col == 0:  # only left plot shows the analytic
        ax.hlines(0,0,1,linestyle='--', alpha=0.6, color="gray", linewidth=0.8)
        ax.hlines(1,0,1,linestyle='--', alpha=0.6, color="gray", linewidth=0.8)
        ax.hlines(-1,0,1,linestyle='--', alpha=0.6, color="gray",linewidth=0.8)
        for i, t in enumerate(times_to_plot):
            ax.plot(x, data_analytic[t, :], label=f"t={t*0.02}", linestyle=lins[i])
        ax.legend(fontsize=10, loc="lower left")
        ax.set_ylabel("u")
        ax.grid(True, linestyle='--', alpha=0.6)
        

        ax.set_title("Analytic Solution")
    else:
        # Make top-middle and top-right completely blank
        ax.set_frame_on(False)

# --- Row 1: Leapfrog ---
for col in range(3):
    ax = axs[1, col]
    ax.hlines(0,0,1,linestyle='--', alpha=0.6, color="gray", linewidth=0.8)
    ax.hlines(1,0,1,linestyle='--', alpha=0.6, color="gray", linewidth=0.8)
    ax.hlines(-1,0,1,linestyle='--', alpha=0.6, color="gray",linewidth=0.8)
    
    for t in times_to_plot:
        ax.plot(x, leapfrog_data[col][t, :])
        #ax.plot(x, data_analytic[t, :], label=f"n={t}", linestyle=lins[i], color="gray")
    ax.set_title(rf"Leapfrog $\mu$ = {CFL_values[col]}")
    if col == 0:
        ax.set_ylabel("u")
    ax.grid(True, linestyle='--', alpha=0.6)

# --- Row 2: Upwind placeholder ---
for col in range(3):
    ax = axs[2, col]
    ax.hlines(0,0,1,linestyle='--', alpha=0.6, color="gray", linewidth=0.8)
    ax.hlines(1,0,1,linestyle='--', alpha=0.6, color="gray", linewidth=0.8)
    ax.hlines(-1,0,1,linestyle='--', alpha=0.6, color="gray",linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_title(rf"Upwind $\mu$ = {CFL_values[col]}")
    for t in times_to_plot:
        ax.plot(x, upwind_data[col][t, :])
        #ax.plot(x, data_analytic[t, :], label=f"n={t}", linestyle=lins[i], color="gray")
        
    if col == 0:
        ax.set_ylabel("u")
    ax.grid(True, linestyle='--', alpha=0.6)

# --- Axis limits ---
for i in range(3):
    for j in range(3):
        axs[i,j].set_xlim(0,1)
        axs[i,j].set_ylim(-1.1,1.1)

# --- Only remove ticks for the blank top plots ---
axs[0,1].set_xticks([])
axs[0,1].set_yticks([])
axs[0,2].set_xticks([])
axs[0,2].set_yticks([])

plt.tight_layout()
output_dir = "../The-advection-equation-report/Figures"
#plt.savefig(f"{output_dir}/cosine.png", dpi=300)
plt.show()