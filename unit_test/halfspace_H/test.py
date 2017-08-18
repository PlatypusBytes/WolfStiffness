# test

import sys
import unittest
# add the src folder to the path to search for files
sys.path.append('../../')
import wolfStiffness
import numpy as np


class TestWolf(unittest.TestCase):
    def setUp(self):
        # read matlab results
        with open(r"./matlab.csv", 'r') as f:
            data = f.read().splitlines()

        data = [i.split(';') for i in data[1:]]
        self.omega = np.array(data)[:, 0].astype(float)

        self.matlab = np.zeros(len(self.omega)).astype(np.complex128)
        for i, c in enumerate(np.array(data)[:, 1]):
            re = float(c.split("+")[0])
            im = float(c.split("+")[1].split("i")[0])
            self.matlab[i] = complex(re, im)

        # maximum allowed error
        self.tol = 1e-6
        return

    def test_wolf(self):

        # run wolf stiffness
        data = wolfStiffness.wolf_stiffness(r"./layers.csv", self.omega)

        # check if the maximum difference is smaller than tolerance
        self.assertTrue(np.max(np.abs((np.real(self.matlab) / np.real(data.K_dyn)) / np.real(self.matlab))) <= self.tol)
        self.assertTrue(np.max(np.abs((np.imag(self.matlab) / np.imag(data.K_dyn)) / np.imag(self.matlab))) <= self.tol)

        return

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
