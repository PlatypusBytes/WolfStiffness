class Layers:
    """ Based on Foundation vibration analysis: A strength of materials approach
        Wolf & Deeks
        """

    def __init__(self, data):
        import numpy as np

        # create variables
        self.name = []
        self.G = []
        self.thickness = []
        self.qsi = []
        self.rho = []
        self.nu = []
        self.c = []
        self.cp = []
        self.cs = []
        self.z0_r = []
        self.delta_M = []  # trapped mass
        self.P = []
        self.u0 = 1.  # initial displacement
        self.amplitude = []
        self.Gn = []
        self.K_dyn = []

        # assign data
        for idx, layer in enumerate(data):
            if layer[0] != 'Force':
                # read data for soil layers
                self.name.append(layer[0])
                self.G.append(float(layer[1]))
                self.nu.append(float(layer[2]))
                self.rho.append(float(layer[3]))
                self.qsi.append(float(layer[4]))
                self.amplitude.append([])
                try:
                    self.thickness.append(float(layer[5]))
                except ValueError:
                    self.thickness.append("halfspace")
            elif layer[0] == 'Force':
                # read force layer
                self.radius = float(layer[6])
                self.direction = str(layer[7])
                self.load_idx = idx + 1

                self.name.append(layer[0])
                self.thickness.append(np.nan)
                self.G.append(np.nan)
                self.nu.append(np.nan)
                self.rho.append(np.nan)
                self.qsi.append(np.nan)
                self.amplitude.append([])
        return

    def assign_properties(self):
        import numpy as np
        import sys

        for i in range(len(self.name)):
            G_star = self.G[i] * (1. + 2. * 1j * self.qsi[i])
            Ec = (1. - self.nu[i]) / (1. - 2. * self.nu[i]) * 2 * G_star

            self.cp.append(np.sqrt(Ec / self.rho[i]))
            self.cs.append(np.sqrt(G_star / self.rho[i]))

            if self.direction == "V":
                self.c.append(self.cp[-1])
            elif self.direction == "H":
                self.c.append(self.cs[-1])
            else:
                sys.exit("direction is not valid. must be V or H")

        return

    def dynamic_stiffness(self, omega):
        import numpy as np

        # generate variable amplitude
        for i in range(len(self.amplitude)):
            self.amplitude[i] = np.zeros(len(omega)).astype(np.complex128)

        self.amplitude[self.load_idx - 1] = np.ones(len(omega)) * (self.u0 + 1j * 0.)

        # wave moving downwards and not halfspace
        if self.load_idx <= len(self.name):
            dir = 1  # direction down
            self.transmit(dir, self.load_idx, self.radius, self.u0, omega)

        # wave moving upwards and not halfspace
        if self.load_idx > 1:
            dir = -1  # direction up
            self.transmit(dir, self.load_idx - 1, self.radius, self.u0, omega)

        # force applied to the disk
        self.stiff_cone(omega)

        # Green's function at the disk
        self.Gn = self.amplitude[self.load_idx - 1] / self.P[self.load_idx]

        # Dynamic stiffness
        self.K_dyn = 1. / self.Gn

        return

    def transmit(self, direction, index, radius, u0, omega):
        import numpy as np

        if direction == -1:  # up
            idx_layer_A = index + 1
            idx_layer_B = index
        else:  # down
            idx_layer_A = index
            idx_layer_B = index + 1

        radius_new = radius + self.thickness[idx_layer_A] / self.z0_r[idx_layer_A]

        # function f
        # pg 56 Eq: 4.5
        f = radius / radius_new * np.exp(-1j * omega / self.c[idx_layer_A] * self.thickness[idx_layer_A]) * u0

        if np.linalg.norm(f) >= 0.0001:
            # function g
            # pg 59 Eq: 4.19
            g = -self.alpha(idx_layer_A, idx_layer_B, radius_new, omega) * f
            # function h
            # pg 57 Eq: 4.10
            h = f + g
            # amplitude of displacement is the summation of h
            # pg 57 Eq: 4.10
            self.amplitude[index] += h

            # reflected wave - changes direction
            self.transmit(-direction, index - direction, radius_new, g, omega)
            if self.thickness[idx_layer_B] != np.inf:
                self.transmit(direction, index + direction, radius_new, h, omega)

        return

    def alpha(self, idx_A, idx_B, rad, omega):
        # alpha
        # pg 58 Eq: 4.16-4.18
        beta_A = self.rho[idx_A] * self.c[idx_A]**2 * (1. / (self.z0_r[idx_A] * rad) +
                                                       1j * omega / self.c[idx_A])

        beta_B = self.rho[idx_B] * self.c[idx_B]**2 * (1. / (self.z0_r[idx_B] * rad) +
                                                       1j * omega / self.c[idx_B])

        if self.name[idx_A] == 'Force':
            beta_A = len(omega) * [0.]
        elif self.name[idx_B] == 'Force':
            beta_B = len(omega) * [0.]

        alpha = - (beta_A - beta_B) / (beta_A + beta_B)

        return alpha

    def static_cone(self):
        import numpy as np

        # compute static cone apex
        for i in range(len(self.name)):
            if self.direction == "V":
                # compute static cone apex - vertical
                # pg. 33 Eq: 3.28
                z0_r0 = np.pi / 4. * (1. - self.nu[i]) * (self.cp[i] / self.cs[i]) ** 2
            elif self.direction == "H":
                # compute static cone apex - horizontal
                # pg. 34 Eq: 3.31
                z0_r0 = np.pi / 8 * (2. - self.nu[i])

            self.z0_r.append(z0_r0)
        return

    def correction_incompressible(self):
        import numpy as np
        # correction for incompressible solids
        # the compression wave, as poisson gets to 0.5 tends to infinite
        # pg. 44 section: 3.4
        # only for vertical direction
        for i in range(len(self.name)):
            if float(self.nu[i]) >= 1 / 3. and self.direction == "V":
                # maximum compression speed = 2 * shear speed
                self.cp[i] = 2. * self.cs[i]
                self.c[i] = 2. * self.cs[i]

                # trapped mass
                # pg. 44 Eq: 3.84
                self.delta_M.append(2.4 * (self.nu[i] - 1. / 3.) * self.rho[i] * np.pi * self.radius ** 3.)
            else:
                self.delta_M.append(0.)
        return

    def stiff_cone(self, omega):
        import numpy as np
        # dynamic load
        # pg 32 Eq: 3.16 (trapped mass pg. 45 Eq: 3.87)
        for i in range(len(self.name)):
            self.P.append(self.rho[i] * self.c[i] ** 2 * np.pi * self.radius ** 2 / self.z0_r[i] +
                          1j * omega * self.rho[i] * self.c[i] * np.pi * self.radius +
                          - omega ** 2 * self.delta_M[i])

        return


def read_file(file_name):
    import os
    import sys

    if not os.path.isfile(file_name):
        sys.exit("Layers file name does not exist.")

    with open(file_name, 'r') as f:
        data = f.read().splitlines()

    lines = []
    for i in data[1:]:
        lines.append([j for j in i.split(';')])

    return lines


def write_output(path, data, omega, freq):
    import matplotlib.pylab as plt
    import numpy as np
    import os

    path_results, name = os.path.split(path)[:2]
    name = name.split(".csv")[0]

    # write table => frequency ; complex stiffness
    with open(os.path.join(path_results, "Kdyn_" + str(name) + ".csv"), "w") as f:
        f.write("omega [rad/s];dynamic stiffness [N/m2];phase delay [degree]\n")
        for i in range(len(omega)):
            f.write(str(omega[i]) + ";" +
                    str(np.real(data.K_dyn[i])) + ";" +
                    str(np.imag(data.K_dyn[i])) + "\n")

    if freq:
        # make graph
        plt.plot(omega / 2. / np.pi, np.abs(np.real(data.K_dyn)))
        plt.grid('on')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('K$_{dyn}$ [N/m]')
        plt.xlim(omega[0], omega[-1] / 2. / np.pi)
    else:
        # make graph
        plt.plot(omega, np.abs(np.real(data.K_dyn)))
        plt.grid('on')
        plt.xlabel('$\omega$ [rad/s]')
        plt.ylabel('K$_{dyn}$ [N/m]')
        plt.xlim(omega[0], omega[-1])

    plt.ylim(bottom=0)
    plt.savefig(os.path.join(path_results, "Kdyn_" + str(name) + ".png"))
    plt.close()

    return
