""""python file with main calculations"""
import numpy as np
import matplotlib.pyplot as plt

from WP4_2.root_interface import trap_elements, stringer,moments_from_elements
from parameters import *
y=np.linspace(0,b,100)
t=1e-3



elements=trap_elements(y,pos_frontspar=pos_frontspar, pos_rearspar=pos_rearspar,thickness=t)


J,Ix,Iy=moments_from_elements(*elements)

plt.plot(y,J)
plt.plot(y,Ix)
plt.plot(y,Iy)

plt.show()