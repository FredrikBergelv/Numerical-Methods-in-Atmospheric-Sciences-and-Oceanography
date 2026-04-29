import numpy as np
import matplotlib.pyplot as plt

# Load data: t, V, EP, EK
t, V, EP, EK = np.loadtxt("2D-SWE/energy.txt", unpack=True)

E_total = EP + EK

def relerr(values, ref):
    return 100*(values-ref)/ref

fig, axs = plt.subplots(1, 3, figsize=(10, 4))

# --- Energy plot 1 ---
axs[0].plot(t, EP*1e-9, label="Potential energy")
axs[0].plot(t, EK*1e-9, label="Kinetic energy")
axs[0].set_xlabel("Time [s]")
axs[0].set_ylabel("Energy [GJ]")
axs[0].legend()
axs[0].grid(True, linestyle='--', alpha=0.6)
axs[0].set_title("Energy evolution")

# --- Energy plot 2 ---
axs[1].plot(t, relerr(E_total, E_total[0]), c="g")
axs[1].set_xlabel("Time [s]")
axs[1].set_ylabel("Relative error [%]")
axs[1].grid(True, linestyle='--', alpha=0.6)
axs[1].set_title("Total Energy error evolution")

# --- Volume deviation ---

axs[2].plot(t, relerr(V, V[0]), color="black")
axs[2].set_xlabel("Time [s]")
axs[2].set_ylabel("Relative error [%]")
axs[2].grid(True, linestyle='--', alpha=0.6)
axs[2].set_title("Total volume error evolution")


plt.suptitle("Energy and volume conservation", size=14)
plt.tight_layout()

plt.savefig("energy.png", dpi=300)
plt.savefig("2D-SWE-notes/Figures/energy.png", dpi=300)
plt.show()
