#PACKAGES
import math
import matplotlib.pyplot as plt
import numpy as np




#Constants
S_F=1.5  #Safety factor of 1.5 as per CS regulations
G=9.81 #m/s**2
GAMMA_AIR=1.4 #specific heat air air
MTOW=20331.70245 #kg
R=287 #unviersal gas constnat
CL_MAX_L=2.7
CL_CR=0.341
CL_CLEAN=1.8
RHO=1.225 #kg/m**3
S=55.4 #m**2 wing surface area
V_CR = 261.8 # taken as a constant
CRUISE=10668 #m
SURFACE=0
H=CRUISE #m
T_SURF=288.15 #K
T_CR=218.81 #K

def M(H):
    GAMMA_AIR=1.4
    R=287
    T_SURF=288.15 #K
    T_CR=218.81
    if H==CRUISE:
        M=math.sqrt(GAMMA_AIR*R*T_CR)
        return M
    else:
        M=math.sqrt(GAMMA_AIR*R*T_SURF)
        return M





#Masses
MPW=9302 #kg
M_1=10820 #kg,  OEM
M_2=M_1+MPW+(MTOW-M_1-MPW)  #OEM + MPW + MAX FUEL
M_3=M_1+MPW  #OEM + MPW

MASS=M_1  #SELECTION OF MASS


#MTOW MASS SIMPLIFCIATIO AIRPLANE DOES NOT LAND AT MTOW
V_S0=math.sqrt((2*MTOW)/(RHO*CL_MAX_L*S))
V_S1=math.sqrt((2*MTOW)/(RHO*CL_CLEAN*S))
M_CR=(V_CR/M(H))
V_A=V_S1*math.sqrt( )
V_F=min(1.6*V_S1)

while H==CRUISE:
    M_D=M_CR+(0.05*M(H))
    if MASS==M_1:
        
    elif MASS==M_2:
        
    else:
        break

while H==SURFACE:
    V_D=1.25*V_CR
    M_D=(V_D/M(H))
    if MASS==M_1:
         
    elif MASS==M_2:
        bla bla bla 
    else:
        break








