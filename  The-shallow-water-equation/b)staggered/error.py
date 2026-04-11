import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# Load data
# ----------------------------
h_analytical = np.loadtxt("b)staggered/h-analytic.txt")

hS = np.loadtxt("b)staggered/h-leapfrog-.0125.txt")
hN  = np.loadtxt("b)staggered/h-leapfrog-.0250.txt")
hL = np.loadtxt("b)staggered/h-leapfrog-.0500.txt")
hU = np.loadtxt("a)unstaggered/h-leapfrog.txt")

hRAN = np.loadtxt("b)staggered/h-leapfrog-robert-asselin.txt")
hRA = np.loadtxt("a)unstaggered/h-leapfrog-robert-asselin.txt")



time_length = 10


# Time grids 
t_a = np.linspace(0, time_length, h_analytical.shape[0])
tN  = np.linspace(0, time_length, hN.shape[0])
tS = np.linspace(0, time_length, hS.shape[0])
tL = np.linspace(0, time_length, hL.shape[0])
tU = np.linspace(0, time_length, hU.shape[0])
tRA = np.linspace(0, time_length, hRA.shape[0])
tRAN = np.linspace(0, time_length, hRAN.shape[0])

# space grids
xS = np.linspace(0, 1.0, hS.shape[1])
xN = np.linspace(0, 1.0, hN.shape[1])
xL = np.linspace(0, 1.0, hL.shape[1])
xU = np.linspace(0, 1.0, hU.shape[1])
xA = np.linspace(0, 1.0, h_analytical.shape[1])
xRA = np.linspace(0, 1.0, hRA.shape[1])
xRAN = np.linspace(0, 1.0, hRAN.shape[1])

# Interpolate to common time grid
def interp_time_full(h, t_old, t_new):
    Nt_new = len(t_new)
    Nx = h.shape[1]
    out = np.zeros((Nt_new, Nx))
    
    for j in range(Nx):
        out[:, j] = np.interp(t_new, t_old, h[:, j])
    
    return out

hN_t = interp_time_full(hN, tN, t_a)
hS_t = interp_time_full(hS, tS, t_a)
hL_t = interp_time_full(hL, tL, t_a)
hU_t = interp_time_full(hU, tU, t_a)
hRA_t = interp_time_full(hRA, tRA, t_a)
hRAN_t = interp_time_full(hRAN, tRAN, t_a)

# Interpolate to common space grid
def interp_space_full(h, x_old, x_new):
    Nt = h.shape[0]
    Nx_new = len(x_new)
    out = np.zeros((Nt, Nx_new))
    
    for i in range(Nt):
        out[i, :] = np.interp(x_new, x_old, h[i, :])
    
    return out

# Now we have all solutions on the same time and space grid, we can compute the error
hN_full = interp_space_full(hN_t, xN, xA)
hS_full = interp_space_full(hS_t, xS, xA)
hL_full = interp_space_full(hL_t, xL, xA)
hU_full = interp_space_full(hU_t, xU, xA)
hRA_full = interp_space_full(hRA_t, xRA, xA)
hRAN_full = interp_space_full(hRAN_t, xRAN, xA)

# Compute L2 error in time
errN_t = np.sqrt(np.mean((hN_full - h_analytical)**2, axis=1)) / np.sqrt(np.mean(h_analytical**2, axis=1)) * 100
errS_t = np.sqrt(np.mean((hS_full - h_analytical)**2, axis=1)) / np.sqrt(np.mean(h_analytical**2, axis=1)) * 100
errL_t = np.sqrt(np.mean((hL_full - h_analytical)**2, axis=1)) / np.sqrt(np.mean(h_analytical**2, axis=1)) * 100
errU_t = np.sqrt(np.mean((hU_full - h_analytical)**2, axis=1)) / np.sqrt(np.mean(h_analytical**2, axis=1)) * 100
errRA_t = np.sqrt(np.mean((hRA_full - h_analytical)**2, axis=1)) / np.sqrt(np.mean(h_analytical**2, axis=1)) * 100
errRAN_t = np.sqrt(np.mean((hRAN_full - h_analytical)**2, axis=1)) / np.sqrt(np.mean(h_analytical**2, axis=1)) * 100

# Smooth the error curves for better visualization
def smooth(y, window=25):
    return np.convolve(y, np.ones(window)/window, mode='same')

remove_idx = -10

errS_s = smooth(errS_t)[0:remove_idx]
errN_s = smooth(errN_t)[0:remove_idx]
errL_s = smooth(errL_t)[0:remove_idx]
errU_s = smooth(errU_t)[0:remove_idx]
errRA_s = smooth(errRA_t)[0:remove_idx]
errRAN_s = smooth(errRAN_t)[0:remove_idx]

t_s = t_a[0:remove_idx]



fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True, sharex=True)

ax = axs[0]
ax.plot(t_a, errS_t, label=r"Staggered ($\Delta x=0.0125$)", color="orange")
ax.plot(t_a, errN_t, label=r"Staggered ($\Delta x=0.025$)", color="blue")
ax.plot(t_a, errL_t, label=r"Staggered ($\Delta x=0.05$)", color="green")
ax.plot(t_a, errRAN_t, label=r"Staggered + Robert-Asselin ($\Delta x=0.025, \gamma=0.005$)", color="darkblue", linestyle="--")

ax.plot(t_a, errU_t, label=r"Unstaggered ($\Delta x=0.025$)", color="red")
ax.plot(t_a, errRA_t, label=r"Unstaggered + Robert-Asselin ($\Delta x=0.025, \gamma=0.01$)", color="darkred", linestyle="--")

ax.legend()
ax.set_ylabel(r"Relative error [%]")
ax.set_xlabel(r"$t$ [arbitrary time unit]")
ax.grid(linestyle="--", alpha=0.5)
ax.set_title("Raw error")


ax = axs[1]
ax.plot(t_s, errS_s, label=r"Staggered ($\Delta x=0.0125$)", color="orange")
ax.plot(t_s, errN_s, label=r"Staggered ($\Delta x=0.025$)", color="blue")
ax.plot(t_s, errL_s, label=r"Staggered ($\Delta x=0.05$)", color="green")
ax.plot(t_s, errRAN_s, label=r"Staggered + Robert-Asselin ($\Delta x=0.025, \gamma=0.01$)", color="darkblue", linestyle="--")

ax.plot(t_s, errU_s, label=r"Unstaggered ($\Delta x=0.025$)", color="red")
ax.plot(t_s, errRA_s, label=r"Unstaggered + Robert-Asselin ($\Delta x=0.025, \gamma=0.01$)", color="darkred", linestyle="--")

ax.set_xlabel(r"$t$ [arbitrary time unit]")
ax.grid(linestyle="--", alpha=0.5)
ax.set_title("Smoothed error")


plt.suptitle(f"Time Evolution of the Relative Error on $h$", fontsize=15)
plt.tight_layout()
output_dir = "The-shallow-water-equation-report/Figures"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f"{output_dir}/error.png", dpi=300)
plt.show()