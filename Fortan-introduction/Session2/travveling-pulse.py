import numpy as np
import matplotlib.pyplot as plt

# load data (each row = time, each column = x)
data = np.loadtxt("travveling-pulse.txt")

Nt, Nx = data.shape

# create x-axis 
delX = 0.05
x = np.arange(0, Nx*delX, delX)

# choose a few time indices to plot
times_to_plot = [0, 4, 10]

colors = ['skyblue', 'salmon', 'lightgreen', 'orange']  # one color per curve

plt.figure(figsize=(8,4))

for idx, t in enumerate(times_to_plot):
    plt.fill_between(x, data[t, :], color=colors[idx], alpha=0.5, label=f"t step {t}")

plt.xlabel("x")
plt.ylabel("Amplitude")
plt.title("Travelling pulse with shaded regions")
plt.ylim(-0.2, 1.2)
plt.legend()
plt.grid(True)

plt.show()