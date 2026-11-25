import scipy as sp
import numpy as np
from math import cos, sin, radians
import matplotlib.pyplot as plt
from WP4_1.readin_data import readxflr
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

import parameters
from parameters import RHO, V_INF, c_root, c_tip, b, g, n_of_spanwise_pos

w_engine = parameters.W_engine
y = np.linspace(0, parameters.b / 2 , n_of_spanwise_pos)

ystep = y[1] - y[0]
n=parameters.n  

torque_engine=parameters.Thrust_current*parameters.engine_torsion_moment_arm

#calculates dynamic pressure q:
def q(rho, V):
    return 0.5*rho*V*V

#calculates chord length along span (based on trapezoidal planform)
#y measured from the root (y=0) to the tip (y=b/2)
def chord(y, c_root, c_tip, b):
    return c_root - (c_root - c_tip) * (2*y/b)


#calculates the density per unit span of the wing
#the output is a single number that describes the density at a spanwise location
#assumes that weight distribution is proportional to the chord length
def density_unit_length(y,S,Wwingtotal,Wfueltotal):
    constant=(Wwingtotal+Wfueltotal)/S
    return constant*chord(y, parameters.c_root , parameters.c_tip , parameters.b)


#weight per unit span [N/m] of wing structure + fuel (positive value, acts downward)
#parameters.wing_weight and parameters.fuel_weight_max are masses in kg, so multiply by g
def weightDist(y, fuel_fraction):
    a = g * density_unit_length(y, parameters.wing_surface, parameters.wing_weight,
                                   fuel_fraction * parameters.fuel_weight_max)
    return a


#gets correct distributions from the CL at a certain flight condtiion. Based on n-V diagrams.
#also depends on distributions at 0, and 10 degrees.
#CL0, CL10: overall wing lift coefficients at 0 and 10 degrees (scalars from xflr)
#cl0, cl10, cm0, cm10: spanwise distributions at 0 and 10 degrees (functions of y)
def getDistFromCL(req_CL, CL0, CL10, cl0, cl10, cm0, cm10):
    #interpolation factor, same for all three distributions
    k = (req_CL - CL0) / (CL10 - CL0)
    def cl(y):
        return cl0(y) + k*(cl10(y) - cl0(y))
    def cm(y):
        return cm0(y) + k*(cm10(y) - cm0(y))
    alpha = k*10
    return cl, cm, alpha

#find the required CL from the load factor n
def getReqCL(mass, n, rho, v_inf, S):
    CL = (n*2*mass*g)/(rho*v_inf*v_inf*S)
    return CL


#function that converts non-dimensional distributions from xlfr to dimensional based on dynamic pressure.
#returns L'(y) [N/m], D'(y) [N/m] and M'(y) [Nm/m] as functions of y
def nonDimensionalDist(cl, cd, cm, q_inf, c_root, c_tip, b):
    def L_prime(y):
        return q_inf * chord(y, c_root, c_tip, b) * cl(y)
    def D_prime(y):
        return q_inf * chord(y, c_root, c_tip, b) * cd(y)
    def M_prime(y):
        return q_inf * chord(y, c_root, c_tip, b)**2 * cm(y)
    return L_prime, D_prime, M_prime

#converts lift and drag forces to forces normal to the wing box depending on alpha
def convertToNormalForce(alpha, L_prime, D_prime):
    def normalDist(y):
        return cos(radians(alpha))*L_prime(y)+sin(radians(alpha))*D_prime(y)
    return normalDist

#integrates a distribution from the tip inwards: F(y) = integral from y to b/2 of f(s) ds
def integrateFromTip(y, f_vals):
    return -sp.integrate.cumulative_trapezoid(f_vals[::-1], y[::-1], initial=0)[::-1]

#calculates and plots the loads along the half span for a required CL
#includes aerodynamic loads and the wing structure + fuel weight (no engine weight yet)
#n: load factor applied to the weight, fuel_fraction: fraction of max fuel on board
def plotLoads(rho=RHO, V=V_INF, c_root=c_root, c_tip=c_tip, b=b, n_point=n_of_spanwise_pos,
              n=1.0, fuel_fraction=1.0, aircraft_mass=parameters.MTOW):
    Clf, Clf10, Cdf, Cdf10, Cmf, Cmf10, CL0, CL10 = readxflr()

    #distributions at the required CL
    req_CL= getReqCL(aircraft_mass, n, rho, V, parameters.wing_surface)
    cl, cm, alpha = getDistFromCL(req_CL, CL0, CL10, Clf, Clf10, Cmf, Cmf10)
    k = (req_CL - CL0) / (CL10 - CL0)   #same interpolation factor for cd
    def cd(y):
        return Cdf(y) + k*(Cdf10(y) - Cdf(y))

    #dimensional distributions
    q_inf = q(rho, V)
    L_prime, D_prime, M_prime = nonDimensionalDist(cl, cd, cm, q_inf, c_root, c_tip, b)
    N_prime = convertToNormalForce(alpha, L_prime, D_prime)

    #evaluate along the half span
    y = np.linspace(0, b/2, n_point)
    L_vals = L_prime(y)
    N_aero = N_prime(y)
    #structure + fuel weight, component normal to the wing box (weight acts downward)
    W_vals = n * cos(radians(alpha)) * weightDist(y, fuel_fraction)
    N_vals = N_aero - W_vals
    M_vals = M_prime(y)

    
    #adding point loads to the force distributions
    engine_index = parameters.engine_spanwise_pos * n_of_spanwise_pos
    N_vals[int(engine_index)] -= w_engine * 9.81 * n / ystep
    M_vals[int(engine_index)] += torque_engine /ystep

    #internal loads (positive up / nose up), integrated from the free tip to the root
    shear   = integrateFromTip(y, N_vals)      # S(y) [N]
    bending = integrateFromTip(y, shear)       # M_b(y) [Nm]
    torque  = integrateFromTip(y, M_vals)      # T(y) [Nm] (from aerodynamic moment only)



    print(f"Required CL = {req_CL}, alpha = {alpha:.2f} deg, q = {q_inf:.1f} Pa")
    print(f"Half-wing lift  = {np.trapezoid(L_vals, y):.1f} N")
    print(f"Half-wing weight (struct+fuel) = {np.trapezoid(weightDist(y, fuel_fraction), y):.1f} N")
    print(f"Root shear      = {shear[0]:.1f} N")
    print(f"Root bending    = {bending[0]:.1f} Nm")
    print(f"Root torque     = {torque[0]:.1f} Nm")

    #plotting
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    plots = [
        (L_vals,  "Lift per unit span L' [N/m]",       "Lift distribution"),
        (N_vals,  "Normal force per unit span [N/m]",  "Net normal force (aero - weight)"),
        (M_vals,  "Moment per unit span M' [Nm/m]",    "Pitching moment distribution"),
        (shear,   "Shear force S [N]",                 "Shear force diagram"),
        (bending, "Bending moment M [Nm]",             "Bending moment diagram"),
        (torque,  "Torque T [Nm]",                     "Torque diagram"),
    ]
    for ax, (vals, ylabel, title) in zip(axes.flat, plots):
        ax.plot(y, vals)
        ax.set_xlabel("Spanwise position, y [m]")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True)
    fig.suptitle(f"Wing loads at CL = {req_CL} (alpha = {alpha:.2f} deg, V = {V} m/s)")
    plt.tight_layout()
    plt.show()

    return y, shear, bending, torque


if __name__ == "__main__":
    plotLoads(1.0)



