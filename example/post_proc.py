r""""
Comparison with the results of Wolf & Deeks (2004) pg: 107-108
"""

import numpy as np
import matplotlib.pylab as plt


with open("Kdyn_input.csv", "r") as f:
    data = f.read().splitlines()

data = [i.split(";") for i in data[1:]]

omega = np.array([float(i[0]) for i in data])
complex = np.array([np.complex(i[1]) for i in data])
stiff = np.array([float(i[2]) for i in data])
damp = np.array([float(i[3]) for i in data])

r0 = 1
kappa = np.complex(5333.333333333334 + 533.3333333333333j)
cs1 = np.complex(0.7462847911324338 + 0.037221417490803994j)
a0 = omega * np.real(r0 / cs1)

fig, ax = plt.subplots(1, 3, figsize=(10, 4))
plt.rcParams.update({'font.size': 10})

ax[0].plot(a0, stiff / np.real(kappa))
ax[1].plot(a0, damp / np.real(kappa))
ax[2].plot(a0, np.sqrt(np.real(complex / kappa)**2 + np.imag(complex / kappa) ** 2))
ax[0].grid()
ax[0].set_ylim(0, 1.5)
ax[0].set_xlim(0, 6.2)
ax[1].grid()
ax[1].set_ylim(0, 2)
ax[1].set_xlim(0, 6.2)
ax[2].grid()
ax[2].set_ylim(0, 8)
ax[2].set_xlim(0, 6.2)
plt.show()
