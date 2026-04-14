import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# Load data
# ----------------------------
h_analytical = np.loadtxt("b)staggered/h-analytic.txt")

h_unstagg = np.loadtxt("c)extra/unstagg.txt")

h_stagg = np.loadtxt("c)extra/stagg.txt")


time_length = 10


# Time grids 
t_a = np.linspace(0, time_length, h_analytical.shape[0])
th_unstagg  = np.linspace(0, time_length, h_unstagg.shape[0])
th_stagg = np.linspace(0, time_length, h_stagg.shape[0])


# space grids
x_unstagg = np.linspace(0, 1.0, h_unstagg.shape[1])
x_stagg = np.linspace(0, 1.0, h_stagg.shape[1])
x_analytical = np.linspace(0, 1.0, h_analytical.shape[1])


# Interpolate to common time grid
def interp_time_full(h, t_old, t_new):
    Nt_new = len(t_new)
    Nx = h.shape[1]
    out = np.zeros((Nt_new, Nx))
    
    for j in range(Nx):
        out[:, j] = np.interp(t_new, t_old, h[:, j])
    
    return out

h_unstagg_t = interp_time_full(h_unstagg, th_unstagg, t_a)
h_stagg_t = interp_time_full(h_stagg, th_stagg, t_a)


# Interpolate to common space grid
def interp_space_full(h, x_old, x_new):
    Nt = h.shape[0]
    Nx_new = len(x_new)
    out = np.zeros((Nt, Nx_new))
    
    for i in range(Nt):
        out[i, :] = np.interp(x_new, x_old, h[i, :])
    
    return out

# Now we have all solutions on the same time and space grid, we can compute the error
h_unstagg_full = interp_space_full(h_unstagg_t, x_unstagg, x_analytical)
h_stagg_full = interp_space_full(h_stagg_t, x_stagg, x_analytical)


# Compute L2 error in time
err_unstagg_t = np.sqrt(np.mean((h_unstagg_full - h_analytical)**2, axis=1)) / np.sqrt(np.mean(h_analytical**2, axis=1)) * 100
err_stagg_t = np.sqrt(np.mean((h_stagg_full - h_analytical)**2, axis=1)) / np.sqrt(np.mean(h_analytical**2, axis=1)) * 100

print("Unstaggered error  mean:", np.mean(err_unstagg_t))
print("Staggered error  mean:", np.mean(err_stagg_t))

# Smooth the error curves for better visualization
def smooth(y, window=25):
    return np.convolve(y, np.ones(window)/window, mode='same')

remove_idx = -20

err_unstagg_s = smooth(err_unstagg_t)[0:remove_idx]
err_stagg_s = smooth(err_stagg_t)[0:remove_idx]


t_s = t_a[0:remove_idx]



fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True, sharex=True)

ax = axs[0]
ax.plot(t_a, err_unstagg_t, label=r"Unstaggered ($\Delta x=0.025$, $\mu=0.45$)")
ax.plot(t_a, err_stagg_t, label=r"Staggered ($\Delta x=0.025$, $\mu=0.45$)")


ax.legend()
ax.set_ylabel(r"Relative error [%]")
ax.set_xlabel(r"$t$ [arbitrary time unit]")
ax.grid(linestyle="--", alpha=0.5)
ax.set_title("Raw error")


ax = axs[1]
ax.plot(t_s, err_unstagg_s, label=r"Unstaggered ($\Delta x=0.025$, $\mu=0.45$)")
ax.plot(t_s, err_stagg_s, label=r"Staggered ($\Delta x=0.025$, $\mu=0.45$)")

ax.set_xlabel(r"$t$ [arbitrary time unit]")
ax.grid(linestyle="--", alpha=0.5)
ax.set_title("Smoothed error")


ax.set_xlabel(r"$t$ [arbitrary time unit]")
ax.grid(linestyle="--", alpha=0.5)
ax.set_title("Smoothed error")


plt.suptitle(f"Time Evolution of the Relative Error on $h$, for same CFL", fontsize=15)
plt.tight_layout()
output_dir = "The-shallow-water-equation-report/Figures"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f"{output_dir}/error-same-CFL.png", dpi=300)
plt.show()