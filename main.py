""""python file with main calculations"""
import numpy as np
import matplotlib.pyplot as plt

from WP4_2.ODE_solver import solve_deflection_rk4
from WP4_2.root_interface import trap_elements, stringer,moments_from_elements, chord
from WP4_2.read_airfoil_thickness import get_airfoil_thickness
from parameters import *
y=np.linspace(0,b/2,201)
t=1e-3

elements=trap_elements(y,pos_frontspar=pos_frontspar, pos_rearspar=pos_rearspar,thickness=t)


J,Ix,Iy=moments_from_elements(*elements)




def deflection(M, T, E=72.4e9, G=28.0e9):
    res = solve_deflection_rk4(y, m_grid=M, t_grid=T, ixx_grid=Ix, j_grid=J, e=E, g=G)

    v_limit =  0.15*b
    phi_limit = 10 
    v_ok = res["v_tip"] <= v_limit
    phi_ok = res["phi_tip"] <= phi_limit

    print("tip deflection:", round(res["v_tip"], 3), "m, limit:", round(v_limit, 3), "m, OK:", v_ok)
    print("tip twist:", round(np.degrees(res["phi_tip"]), 2), "deg, limit:", phi_limit, "deg, OK:", phi_ok)

    return res

def plot_deflection(res):
    plt.figure()
    plt.plot(res["y"], res["v"])
    plt.xlabel("y [m]")
    plt.ylabel("v [m]")
    plt.title("Bending Deflection")
    plt.grid(True)

    plt.figure()
    plt.plot(res["y"], np.degrees(res["phi"]))
    plt.xlabel("y [m]")
    plt.ylabel("phi [deg]")
    plt.title("Twist")
    plt.grid(True)

    plt.tight_layout()
    plt.show()



plt.plot(y,J)
plt.plot(y,Ix)
plt.plot(y,Iy)

plt.show()