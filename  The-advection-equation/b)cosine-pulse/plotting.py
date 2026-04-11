import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Load data
# ----------------------------
data_analytic = np.loadtxt("analytic.txt")
data_leapfrog = np.loadtxt("leapfrog_CFL_0.90.txt")
data_upwind  = np.loadtxt("upwind_CFL_0.90.txt")



Nt, Nx = data_analytic.shape
delX = 0.02
x = np.arange(0, Nx*delX, delX)
times_to_plot = [0, 4, 8, 40]


# ----------------------------
# Create 3x1 subplot grid
# ----------------------------
fig, axs = plt.subplots(3, 1, figsize=(5,6), sharex=True, sharey=True)
plt.suptitle(r"Cosine-pulse Initial Condition ($\mu$ = 0.9)", fontsize=14)

# --- Row 0: Analytic ---
for t in times_to_plot:
    axs[0].plot(x, data_analytic[t, :], label=f"n={t}")
axs[0].set_title("Analytic")
axs[0].set_ylabel("u")
axs[0].grid(True, linestyle='--', alpha=0.6)
axs[0].legend()

# --- Row 1: Leapfrog ---
axs[1].set_title("Leapfrog")
for t in times_to_plot:
    axs[1].plot(x, data_leapfrog[t, :])
axs[1].set_ylabel("u")
axs[1].grid(True, linestyle='--', alpha=0.6)

# --- Row 3: Upwind ---
axs[2].set_title("Upwind")
for t in times_to_plot:
    axs[2].plot(x, data_upwind[t, :])
axs[2].set_ylabel("u")
axs[2].set_xlabel("x")
axs[2].grid(True, linestyle='--', alpha=0.6)

# --- Limits ---
for ax in axs:
    ax.set_xlim(0,1)

plt.tight_layout()
output_dir = "../The-advection-equation-report/Figures"
#plt.savefig(f"{output_dir}/cosine-pulse.png", dpi=300)
plt.show()