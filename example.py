r""""
Comparison with the results of Wolf & Deeks (2004) pg: 107-108
"""

import os
import json
import numpy as np
import matplotlib.pylab as plt
# import wolf packages
from wolfStiffness import wolf_stiffness


if __name__ == "__main__":
    # creates files with the hash version of the git
    os.system(r"git describe --all --long > version.txt")
    # runs stiffness
    wolf_stiffness("./example/input.csv", np.linspace(0, 5, 150), output_folder="./example")

    # visualise the results
    with open("./example/Kdyn_input.json", "r") as f:
        data = json.load(f)

    omega = np.array(data["omega"])
    compl = np.array(np.apply_along_axis(lambda args: [complex(*args)], 1, data['complex dynamic stiffness']))
    stiff = np.array(data["stiffness"])
    damp = np.array(data["damping"])

    r0 = 1
    kappa = np.complex(5333.333333333334 + 533.3333333333333j)
    cs1 = np.complex(0.7462847911324338 + 0.037221417490803994j)
    a0 = omega * np.real(r0 / cs1)

    fig, ax = plt.subplots(1, 3, figsize=(12, 5))
    plt.rcParams.update({'font.size': 10})

    ax[0].plot(a0, stiff / np.real(kappa))
    ax[1].plot(a0, damp / np.real(kappa))
    ax[2].plot(a0, np.sqrt(np.real(compl / kappa)**2 + np.imag(compl / kappa) ** 2))
    ax[0].grid()
    ax[0].set_ylim(0, 1.5)
    ax[0].set_xlim(0, 6.2)
    ax[0].set_ylabel("Spring coefficient")
    ax[0].set_xlabel("Omega [rad]")
    ax[1].grid()
    ax[1].set_ylim(0, 2)
    ax[1].set_xlim(0, 6.2)
    ax[1].set_ylabel("Damping coefficient")
    ax[1].set_xlabel("Omega [rad]")
    ax[2].grid()
    ax[2].set_ylim(0, 8)
    ax[2].set_xlim(0, 6.2)
    ax[2].set_ylabel("Magnitude")
    ax[2].set_xlabel("Omega [rad]")
    plt.tight_layout()
    plt.show()
