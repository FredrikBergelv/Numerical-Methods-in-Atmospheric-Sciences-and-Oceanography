import numpy as np
import matplotlib.pyplot as plt

Nx = 100
Ny = 100
Lt = 1000
Lx = 100000
Ly = 100000
stride = 20


# load data
data = np.loadtxt("2D-SWE/h_array_wall.txt").flatten()

Nt = len(data) // (Nx * Ny)
data = data[:Nt * Nx * Ny]

h = data.reshape(Nt, Ny, Nx)

# ----------------------------
# choose physical timesteps
# ----------------------------
timesteps = np.array([0, 20, 50, stride*Nt-1]) / stride

timesteps = [int(val) for val in timesteps]

fig, axs = plt.subplots(1, len(timesteps)+1, figsize=(12, 4), sharey=True, sharex=True)

minval = np.min(h)
maxval = np.max(h)

for i, n in enumerate(timesteps):
    
    ax=axs[i]
    
    im = ax.imshow(h[n], origin="lower", vmin=int(minval), vmax=int(maxval), cmap="ocean", extent=[0, Lx/1000, 0, Ly/1000])
    
    
    n_real = n * stride
    t = n_real * Lt / (Nt * stride)
    minutes = int((t % 3600) // 60)
    seconds = int(t % 60)

    ax.set_title(f"$t =$ {minutes}' {seconds}''")
    
    ax.set_xlabel(r"$x$ [km]")
    if i == 0:
        ax.set_ylabel(r"$y$ [km]")

    

fig.colorbar(im, ax=axs[len(timesteps)], pad=0, fraction=1, shrink=0.7,  extend="both", label=r"$h(x,y,t)$ [m]")
axs[len(timesteps)].axis("off")

plt.suptitle(r"$h(x,y,t)$ at different times", size=14)
plt.tight_layout()
plt.savefig("ocean-waves.png", dpi=300)
plt.savefig("2D-SWE-notes/Figures/ocean-waves.png", dpi=300)

plt.show()