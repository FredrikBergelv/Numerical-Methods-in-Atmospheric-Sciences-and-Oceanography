import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Load data
# ----------------------------
data_analytic = np.loadtxt("analytic-longtime.txt")
data_10_leapfrog = np.loadtxt("leapfrog_longtime_CFL_1.00.txt")
data_09_leapfrog = np.loadtxt("leapfrog_longtime_CFL_0.90.txt")
data_10_upwind = np.loadtxt("upwind_longtime_CFL_1.00.txt")
data_09_upwind = np.loadtxt("upwind_longtime_CFL_0.90.txt")


# ----------------------------
# Parameters
# ----------------------------
Nt, Nx = data_analytic.shape

delt = 0.02
t = np.arange(0, Nt*delt, delt)

delt_n = 0.9*0.02/1
t_n = np.arange(0, Nt*delt_n, delt_n)

tmax= 10
tmin = 0

t_plot=t[int(tmin/delt):int(tmax/delt)]
tn_plot=t_n[int(tmin/delt_n):int(tmax/delt_n)]

tmax1 = 890
tmin1 = 880

t1_plot=t[int(tmin1/delt):int(tmax1/delt)]
t1n_plot=t_n[int(tmin1/delt_n):int(tmax1/delt_n)]


# ----------------------------
# plot
# ----------------------------
fig, axs = plt.subplots(2, 2, figsize=(9,5), sharey=True)
plt.suptitle(r"Phase and Amplitude Error ($\mu=0.9$)", fontsize=15)

ax=axs[0,0]
ax.set_title("Leapfrog", fontsize=14)
ax.plot(t_plot, data_analytic[int(tmin/delt):int(tmax/delt),0], label="analytic", c="C1", linestyle="--")
ax.plot(tn_plot, data_09_leapfrog[int(tmin/delt_n):int(tmax/delt_n),0], label="numeric", c="C0")
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_ylabel(r"$u(x,t)$ [arb. unit]")

ax=axs[0,1]
ax.set_title("Leapfrog", fontsize=14)
ax.plot(t1_plot, data_analytic[int(tmin1/delt):int(tmax1/delt),0], label="analytic", c="C1", linestyle="--")
ax.plot(t1n_plot, data_09_leapfrog[int(tmin1/delt_n):int(tmax1/delt_n),0], label="numeric", c="C0")
ax.grid(True, linestyle='--', alpha=0.6)

ax=axs[1,0]
ax.set_title("Upwind", fontsize=14)
ax.plot(t_plot, data_analytic[int(tmin/delt):int(tmax/delt),0], label="analytic", c="C1", linestyle="--")
ax.plot(tn_plot, data_09_upwind[int(tmin/delt_n):int(tmax/delt_n),0], label="numeric", c="C0")
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_ylabel(r"$u(x,t)$ [arb. unit]")
ax.set_xlabel(r"$t$ [arb. time unit]")


ax=axs[1,1]
ax.set_title("Upwind", fontsize=14)
ax.plot(t1_plot, data_analytic[int(tmin1/delt):int(tmax1/delt),0], label="analytic", c="C1", linestyle="--")
ax.plot(t1n_plot, data_09_upwind[int(tmin1/delt_n):int(tmax1/delt_n),0], label="numeric", c="C0")
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_xlabel(r"$t$ [arb. time unit]")

plt.tight_layout()

output_dir = "../../The-advection-equation-report/Figures"
plt.savefig(f"{output_dir}/phase-errors.png", dpi=300)
plt.show()