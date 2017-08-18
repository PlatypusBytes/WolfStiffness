def wolf_stiffness(layer_file, omega):
    """Dynamic stiffness according to Wolf and Deeks
       Layered soil solution
       Only considers the translational cones. The rotational cones are not considered
       """

    import LayeredHalfSpace

    layers = LayeredHalfSpace.read_file(layer_file)

    data = LayeredHalfSpace.Layers(layers)

    data.assign_properties()
    data.correction_incompressible()
    data.static_cone()
    data.dynamic_stiffness(omega)

    LayeredHalfSpace.write_output(layer_file, data, omega)

    return data


if __name__ == "__main__":
    import numpy as np
    wolf_stiffness("./example/input.csv", np.linspace(0, 750, 50))
