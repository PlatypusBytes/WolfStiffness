import os
# import wolf packages
from . import LayeredHalfSpace


def wolf_stiffness(layer_file, omega, freq=False, output_folder="./"):
    """Dynamic stiffness according to Wolf and Deeks
       Layered soil solution
       Only considers the translational cones. The rotational cones are not considered
       """

    layers = LayeredHalfSpace.read_file(layer_file)

    data = LayeredHalfSpace.Layers(layers)

    data.assign_properties()
    data.correction_incompressible()
    data.static_cone()
    data.dynamic_stiffness(omega)

    LayeredHalfSpace.write_output(output_folder, os.path.splitext(os.path.split(layer_file)[-1])[0],
                                  data, omega, freq)

    return data
