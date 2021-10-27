import os
# import wolf packages
from . import LayeredHalfSpace


class WolfStiffness:
    r"""
    Dynamic stiffness according to Wolf and Deeks
    Layered soil solution
    Only considers the translational cones. The rotational cones are not considered
    """
    def __init__(self, omega, freq=False, output_folder="./"):
        self.omega = omega
        self.freq = freq
        self.output_folder = output_folder

        self.layers = []
        self.data = []
        self.name = []
        return

    def read_csv(self, layer_file):
        self.layers = LayeredHalfSpace.read_file(layer_file)
        self.name = os.path.splitext(os.path.split(layer_file)[-1])[0]
        return

    def read_json(self):
        return

    def compute(self):
        self.data = LayeredHalfSpace.Layers(self.layers)

        self.data.assign_properties()
        self.data.correction_incompressible()
        self.data.static_cone()
        self.data.dynamic_stiffness(self.omega)
        return

    def write(self):

        LayeredHalfSpace.write_output(self.output_folder, self.name,
                                      self.data, self.omega, self.freq)
        return
