# WolfStiffness

## Background

This package computes the dynamic soil spring stiffness and dashpot damping,
for an infinite elastic isotropic layered system. 

The computation is based on the semi-analytical cone model presented by 
[Wolf and Deeks (2004)](https://www.elsevier.com/books/foundation-vibration-analysis/wolf/978-0-7506-6164-5). This model assumes that the load is applied to a disk at the

The model is based on one-dimensional wave propagation surface, 
which induces stresses on an area that increases with depth; the
displacements are constant at the cross-section of the cone.
Discontinuities can be modelled by assuming at the interface between 
two layers that one cone leads to the creation of two new cones: reflected and
refracted. This allows the modelling of multi-layered soils.

In this model the dynamic stiffness, Kdyn and damping, D, follow the 
definition proposed in Wolf and Deeks (2004):

<img src="https://render.githubusercontent.com/render/math?math=K_{dyn}=\Re \left(S\right)">
<img src="https://render.githubusercontent.com/render/math?math=D=\frac{\Im \left(S \right)}{\omega}">

where S is the dynamic stiffness matrix (complex frequency response function)
and ω the angular frequency.

## How to use it
The package reads an input CSV file that has the following format:
 
| Layer      | G      | nu    | rho    | damping  | thickness  | radius  | direction |
| ---------- | ------ | ----- | ------ | -------- | ---------- | ------- |---------- | 
| Force      | -      | -     | -      | -        | -          | 1       | V         |
| Layer 1    | 1000   | 0.25  | 2000   | 0.05     | 1          | -       | -         |
| Layer 2    | 2000   | 0.3   | 1500   | 0.05     | 5          | -       | -         |
| Halfspace  | 2500   | 0.20  | 2500   | 0.025    | inf        | -       | -         |

where:
* _Layer_ is the layer name
* _G_ is the dynamic shear modulus (Pa)
* _nu_ is the Poisson ratio 
* _rho_ is the material density (kg/m<sup>3</sup>)
* _damping_ is the material damping
* _thickness_ is layer thickness (m)
* _radius_ is loading radius (m)
* _direction_ is loading direction (can be either _V_ or _H_)
 
The first row of the file needs to be the information about the loading.
The last layer needs to have _inf_ thickness.

### To run the code in python

Install the package using:
```bash
pip install git+https://bitbucket.org/DeltaresGEO/wolfstiff.git
```

To run the code, please follow:

```python
import numpy as np
from WolfStiffness.wolfStiffness import WolfStiffness

# define omegas
omega = np.linspace(0, 5, 150)

# runs stiffness
wolf = WolfStiffness(omega, output_folder="./example")
wolf.read_csv("./example/input_H.csv")
wolf.compute()
wolf.write()
```
In this example the dynamic stiffness is computed for angular frequencies between 0 and 5 rad/s.
The results are saved in a json file in the _output_folder_.

An example of a calculation is [here](./example.py).
