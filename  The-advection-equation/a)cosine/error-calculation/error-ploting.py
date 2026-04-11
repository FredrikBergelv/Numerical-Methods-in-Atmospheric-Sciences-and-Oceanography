import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Load data
# ----------------------------
dataL = np.loadtxt("leapfrog-errors.txt").T
dataU = np.loadtxt("upwind-errors.txt").T

error_L9, error_L1, error_L11 = dataL
error_U9, error_U1, error_U11 = dataU

# time index
n = np.arange(len(error_L9))

delt10 = 0.02
delt09 = 0.02
delt11 = 0.02

t11 = n*delt11
t09 = n*delt09
t10 = n*delt10


# ----------------------------
# Plot
# ----------------------------
fig, axs = plt.subplots(2, 1, figsize=(6,5), sharex=True, sharey=True)
plt.suptitle("Error for Cosine Initial Condition", fontsize=15)

# --- Leapfrog ---
ax = axs[0]
ax.plot(t09, 100*error_L9, label=r"$\mu=0.9$")
ax.plot(t10, 100*error_L1, label=r"$\mu=1.0$")
ax.plot(t11, 100*error_L11, label=r"$\mu=1.1$")

ax.set_title("Leapfrog", fontsize=14)
ax.set_ylabel("Error [%]")
ax.set_yscale("log")
#ax.set_xscale("log")



ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

# --- Upwind ---
ax = axs[1]
ax.plot(t09, 100*error_U9, label=r"$\mu=0.9$")
ax.plot(t10, 100*error_U1, label=r"$\mu=1.0$")
ax.plot(t11, 100*error_U11, label=r"$\mu=1.1$")

ax.set_title("Upwind", fontsize=14)
ax.set_xlabel(r"$t$ [arb. time unit]")
ax.set_ylabel("Error [%]")
ax.set_yscale("log")
#ax.set_xscale("log")
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

ax.set_xlim(0,5)
ax.set_ylim(0,1e3)

plt.tight_layout()
output_dir = "../../The-advection-equation-report/Figures"
plt.savefig(f"{output_dir}/errors.png", dpi=300)
plt.show()