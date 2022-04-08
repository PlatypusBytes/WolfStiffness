import os
# import wolf packages
from WolfStiffness import LayeredHalfSpace


class WolfStiffness:
    r"""
    Dynamic stiffness according to Wolf and Deeks
    Layered soil solution
    Only considers the translational cones. The rotational cones are not considered
    """
    def __init__(self, omega, freq=False, output_folder="./") -> object:
        """
        Initialisation of the object

        :param omega: frequency list in radians
        :param output_folder: (optional)
        """
        self.omega = omega
        self.freq = freq
        self.output_folder = output_folder

        self.layers = []  # input layers and force
        self.data = []  # data results
        self.name = []  # name of the analysis
        return

    def read_csv(self, layer_file) -> object:
        """
        Reads csv input file and parses to object structure

        :param layer_file: path to the input csv file
        :return:
        """
        self.layers = LayeredHalfSpace.read_file(layer_file)
        self.name = os.path.splitext(os.path.split(layer_file)[-1])[0]
        return

    def parse_layers(self, force, soil, name) -> object:
        """
        Parse the data to object structure

        :param force: force
        :param soil: soil parameters
        :param name: name of the analysis
        """
        # ToDo: work in progress
        self.layers.append(force)
        for so in soil:
            self.layers.append(",".join(so))

        self.name = name
        return

    def compute(self) -> object:
        """
        computes the dynamic stiffness following the wolf model
        """
        self.data = LayeredHalfSpace.Layers(self.layers)

        self.data.assign_properties()
        self.data.correction_incompressible()
        self.data.static_cone()
        self.data.dynamic_stiffness(self.omega)
        return

    def write(self, plot=True, freq=False) -> object:
        """
        writes the results

        :param plot: (optional: default False) plots the graphs
        :param freq: (optional: default False) plots the graphs in Hz instead of rad (only if plots == True)
        """
        LayeredHalfSpace.write_output(self.output_folder, self.name,
                                      self.data, self.omega, plot, freq)
        return
