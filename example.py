r""""
Comparison with the results of Wolf & Deeks (2004) pg: 107-108
"""

import os
import json
import numpy as np
import matplotlib.pylab as plt
# import wolf packages
from WolfStiffness.wolfStiffness import wolf_stiffness


def plot(data, kappa, cs1):

    omega = np.array(data["omega"])
    compl = np.array(np.apply_along_axis(lambda args: [complex(*args)], 1, data['complex dynamic stiffness']))
    stiff = np.array(data["stiffness"])
    damp = np.array(data["damping"])

    r0 = 1
    a0 = omega * np.real(r0 / cs1)

    fig, ax = plt.subplots(1, 3, figsize=(12, 5))
    plt.rcParams.update({'font.size': 10})

    ax[0].plot(a0, stiff / np.real(kappa))
    ax[1].plot(a0, damp / np.real(kappa))
    ax[2].plot(a0, np.sqrt(np.real(compl / kappa)**2 + np.imag(compl / kappa) ** 2))
    ax[0].grid()
    ax[0].set_ylim(0, 1.5)
    ax[0].set_xlim(0, 6.2)
    ax[0].set_ylabel("Spring coefficient", fontsize=16)
    ax[0].set_xlabel("Dimensionless frequency", fontsize=16)
    ax[1].grid()
    ax[1].set_ylim(0, 2)
    ax[1].set_xlim(0, 6.2)
    ax[1].set_ylabel("Damping coefficient", fontsize=16)
    ax[1].set_xlabel("Dimensionless frequency", fontsize=16)
    ax[2].grid()
    ax[2].set_ylim(0, 8)
    ax[2].set_xlim(0, 6.2)
    ax[2].set_ylabel("Magnitude", fontsize=16)
    ax[2].set_xlabel("Dimensionless frequency", fontsize=16)

    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    # runs stiffness
    wolf_stiffness("example/input_H.csv", np.linspace(0, 5, 150), output_folder="./example")
    # visualise the results
    with open("./example/Kdyn_input_H.json", "r") as f:
        data = json.load(f)

    kappa = complex(4571.4285714285725 + 457.14285714285717j)
    cs1 = complex(0.7462847911324338 + 0.037221417490803994j)
    plot(data, kappa, cs1)

    # runs stiffness
    wolf_stiffness("example/input_V.csv", np.linspace(0, 5, 150), output_folder="./example")
    # visualise the results
    with open("./example/Kdyn_input_V.json", "r") as f:
        data = json.load(f)

    kappa = complex(5333.333333333334+533.3333333333333j)
    plot(data, kappa, cs1)

