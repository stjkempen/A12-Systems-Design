""""python file with main calculations"""
import numpy as np
import matplotlib.pyplot as plt

from WP4_2.ODE_solver import solve_deflection_rk4
from WP4_2.root_interface import trap_elements, skin_stringers,moments_from_elements, torsion_constant
from WP4_2.read_airfoil_thickness import get_airfoil_thickness
from parameters import *
y=np.linspace(0,b/2,1001)
t=thickness

trap=trap_elements(y,pos_frontspar=pos_frontspar, pos_rearspar=pos_rearspar,thickness=t)
string=skin_stringers(y,pos_frontspar=pos_frontspar,pos_rearspar=pos_rearspar,n_top=5,n_bottom=4,A_str_root=450e-6)
elements=trap+string
_,Ix, Iy=moments_from_elements(*elements)
J_t=torsion_constant(y,pos_frontspar=pos_frontspar,pos_rearspar=pos_rearspar,thickness=thickness)

plt.plot(y,J_t)
plt.plot(y,Ix)
plt.plot(y,Iy)

plt.show()

#--- clipping of area ---
plt.plot(y,string[0]["area"])
plt.show()