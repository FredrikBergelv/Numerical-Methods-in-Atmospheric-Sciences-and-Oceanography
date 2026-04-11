import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# Load data
# ----------------------------
data_analytic = np.loadtxt("a)unstaggered/leapfrog.txt")
data_leapfrog = np.loadtxt("a)unstaggered/leapfrog.txt")

# ----------------------------
# Parameters
# ----------------------------
Nt, Nx = data_analytic.shape
Nt_numerical, Nx__numerical = data_leapfrog.shape

dx = 0.025
dt = 0.02
dt_numerical = 0.9*0.02

t = np.arange(0, Nt * dt, dt/10)
t_numerical = np.arange(0, Nt_numerical * dt_numerical, dt_numerical/10)


# Correct extent 
extent = [0, Nx * dx, 0, Nt * dt]
extent_numerical = [0, Nx * dx, 0, Nt_numerical * dt_numerical]

# ----------------------------
# Select times to plot
# ----------------------------
times_to_plot = [0, 1, 4, 10, 20, 70]
x = np.linspace(0, Nx * dx, Nx)

# ----------------------------
# Plot
# ----------------------------
plt.figure(figsize=(6,4))

for n in times_to_plot:
    #plt.plot(x, data_analytic[n, :], linestyle='--', label=f"Analytic t={n*dt:.2f}")
    plt.plot(x, data_leapfrog[n, :], linestyle='-', label=f"Leapfrog t={n*dt_numerical:.2f}")

plt.xlabel(r"$x$ [arb. length unit]")
plt.ylabel(r"$h(x,t)$")
plt.title(r"Unstaggered grid ($\mu=0.9$)")
plt.legend()
plt.ylim(-1.2, 1.2)
plt.grid()

# ----------------------------
# Save
# ----------------------------
output_dir = "../The-shallow-water-equation-report/Figures"
os.makedirs(output_dir, exist_ok=True)

plt.savefig(f"{output_dir}/unstaggered-lineplot.png", dpi=300)
plt.show()