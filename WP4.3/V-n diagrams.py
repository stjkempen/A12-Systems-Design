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
CL_CRUISE=0.341
CL_CLEAN=1.8
RHO=1.225 #kg/m**3
S=55.4 #m**2 wing surface area
V_CR = 261.8 # taken as a constant
CRUISE=10668 #m
SURFACE=0
H=CRUISE #m
T=288.15 #K

MPW=9302 #kg
M_1=10820 #kg,  OEM
M_2=M_1+MPW+(MTOW-M_1-MPW)  #OEM + MPW + MAX FUEL
M_3=M_1+MPW  #OEM + MPW

#MTOW MASS SIMPLIFCIATIO AIRPLANE DOES NOT LAND AT MTOW
V_S0=math.sqrt((2*MTOW)/(RHO*CL_MAX_L*S))
V_S1=math.sqrt((2*MTOW)/(RHO*CL_CLEAN*S))
M=math.sqrt(GAMMA_AIR*R*T)
M_C=(V_CR/M)
V_D=1.25*V_CR
M_D=(V_D/M)
V_A=V_S1*math.sqrt( )

while H==CRUISE:








