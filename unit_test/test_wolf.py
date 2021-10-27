import unittest
import os
import json
import shutil
import numpy as np
# import package
from ..WolfStiffness.wolfStiffness import WolfStiffness


def compare_dicts(dic1, dic2):

    tol = 1e-6
    if not dic1.keys() == dic2.keys():
        return False
    for k in dic1.keys():
        if np.any(np.array(dic1[k]) - np.array(dic2[k]) >= tol):
            return False
    return True


class TestWolf(unittest.TestCase):
    def setUp(self):
        self.omega = np.linspace(0, 5, 150)
        self.output_folder = "./results"
        self.freq = False

        # load datasets
        with open("./unit_test/files/Kdyn_vertical.json") as f:
            self.vertical = json.load(f)

        with open("./unit_test/files/Kdyn_horizontal.json") as f:
            self.horizontal = json.load(f)

        return

    def test_vertical_solution(self):
        layer_file = "./unit_test/files/input_V.csv"

        wolf = WolfStiffness(self.omega, output_folder=self.output_folder)
        wolf.read_csv(layer_file)
        wolf.compute()
        wolf.write()

        # compare dicts
        with open(os.path.join(self.output_folder, "Kdyn_input_V.json")) as f:
            data = json.load(f)

        self.assertTrue(compare_dicts(data, self.vertical))
        return

    def test_horizontal_solution(self):
        layer_file = "./unit_test/files/input_H.csv"

        wolf = WolfStiffness(self.omega, output_folder=self.output_folder)
        wolf.read_csv(layer_file)
        wolf.compute()
        wolf.write()

        # compare dicts
        with open(os.path.join(self.output_folder, "Kdyn_input_H.json")) as f:
            data = json.load(f)

        self.assertTrue(compare_dicts(data, self.horizontal))
        return

    def test_wolfstiff_files(self):
        layer_file = "./unit_test/files/input_V.csv"

        wolf = WolfStiffness(self.omega, output_folder=self.output_folder)
        wolf.read_csv(layer_file)
        wolf.compute()
        wolf.write()

        # check if folders and files exist
        self.assertTrue(os.path.isdir(self.output_folder))
        self.assertTrue(os.path.isfile(os.path.join(self.output_folder, "Kdyn_input_V.json")))
        self.assertTrue(os.path.isfile(os.path.join(self.output_folder, "input_V.png")))
        self.assertTrue(os.path.isfile(os.path.join(self.output_folder, "input_V.pdf")))

        return

    def tearDown(self):
        shutil.rmtree(self.output_folder)
        return


if __name__ == '__main__':  # pragma: no cover
    unittest.main(unittest.TextTestRunner())
