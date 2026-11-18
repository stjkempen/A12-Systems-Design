#PACKAGES
import math
import matplotlib.pyplot as plt
import numpy as np




#Constants

'''IF ALTITUDE NOT SPECIFIED IT IS SURFACE BY DEFAULT'''

S_F=1.5  #Safety factor of 1.5 as per CS regulations
G=9.81 #m/s**2
GAMMA_AIR=1.4 #specific heat air air
MTOW=20331.70245 #kg
R=287 #unviersal gas constnat
CL_MAX_L=2.7
CL_CR=0.341
CL_CLEAN=1.8

def RHO(H):
    if H==0:
        rho=1.225
    else:
        rho=0.3796
    return rho

S=55.4 #m**2 wing surface area
altitudes=[0,10668]
SIGMA=RHO(altitudes[1])/RHO(altitudes[0]) #-------conversion to EAS

"""HEIGHT SELECTION"""
H=altitudes[0] #m


T_SURF=288.15 #K
T_CR=218.81 #K
KG_TO_LBF = 2.20462
# Convert MTOW (kg) to lbf, then clamp between 2.5 and 3.8 per CS 25.337(b)
n_raw = 2.1 + (24000 / ((MTOW * KG_TO_LBF) + 10000))
N_MAX = round(min(max(n_raw, 2.5), 3.8), 1)
N_MAX_FLAPS=2
M_C=0.77
V_S0=0
V_S1=0


def M(H):
    GAMMA_AIR=1.4
    R=287
    T_SURF=288.15 #K
    T_CR=218.81
    if H==altitudes[0]:
        M=math.sqrt(GAMMA_AIR*R*T_SURF)
        return M
    else:
        M=math.sqrt(GAMMA_AIR*R*T_CR)
        return M

V_CR = 0.77*M(H) # taken as a constant 


#Masses
MPW=9302 #kg
MASS_1=10820 #kg,  OEM
MASS_2=MASS_1+MPW+(MTOW-MASS_1-MPW)  #OEM + MPW + MAX FUEL
MASS_3=MASS_1+MPW  #OEM + MPW

MASSES_LIST=[MASS_1,MASS_2,MASS_3]



MASS=MASS_1  #SELECTION OF MASS

#MTOW MASS SIMPLIFCIATIO AIRPLANE DOES NOT LAND AT MTOW


"""V_C CALCULATIONS"""
for H in altitudes:
    if H==0:
        V_CR=round(0.77*M(H)*math.sqrt(SIGMA),2)
        V_D=round(1.25*V_CR,2)
    else:
        V_CR=round(0.77*M(H)*math.sqrt(SIGMA),2)
        M_D=M_C+0.05
        V_D=round(M(H)*M_D*math.sqrt(SIGMA),2)
    
    for mass in MASSES_LIST:  
        V_S0=round(float(math.sqrt((2*mass*G)/(RHO(0)*CL_MAX_L*S))),2)
        V_S1=round(math.sqrt(((2*mass*G)/(RHO(0)*CL_CLEAN*S))),2)
        V_A=round(V_S1*math.sqrt(N_MAX),2)
        V_F=round(max(1.6*V_S1, 1.8*V_S0,),2)
        print("at altitude:", H,"For mass:", mass, "kg", "the velocities are:",
            "V_S0 =", V_S0, "V_S1 =", V_S1, "V_A =", V_A,
            "V_CR =", V_CR, "V_D =", V_D, "V_F =", V_F)









