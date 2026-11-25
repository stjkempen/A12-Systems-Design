""""python file with main calculations"""
import numpy as np
import matplotlib.pyplot as plt

from WP4_1.loading_calc import plotLoads
from WP4_2.root_interface import trap_elements, skin_stringers,moments_from_elements, torsion_constant
from WP4_2.ODE_solver import deflection, plot_deflection
from parameters import *

# --- section related to WP4.1 ---
y, shear, bending, torque = plotLoads()

# --- section related to WP4.2 ---

# - defening the geometry of the wing cross-section -
t=thickness

trap=trap_elements(y,pos_frontspar=pos_frontspar, pos_rearspar=pos_rearspar,thickness=t)
string=skin_stringers(y,pos_frontspar=pos_frontspar,pos_rearspar=pos_rearspar,n_top=5,n_bottom=4,A_str_root=450e-6)
elements=trap+string
_,Ix, Iy=moments_from_elements(*elements)
J_t=torsion_constant(y,pos_frontspar=pos_frontspar,pos_rearspar=pos_rearspar,thickness=thickness)

# - ODE solver -
results=deflection(y, bending,torque,Ix,J_t)
plot_deflection(results)


# --- plotting of results ---


"""plt.plot(y,J_t)
plt.plot(y,Ix)
plt.plot(y,Iy)

plt.show()

#--- clipping of area ---
plt.plot(y,string[0]["area"])
plt.show()"""