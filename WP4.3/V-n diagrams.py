#PACKAGES
import math
import numpy as np
import matplotlib as mplt




#Constants
S_F=1.5  #Safety factor of 1.5 as per CS regulations
G=9.81 #m/s**2
GAMMA_AIR=1.4 #specific heat air air
MTOW=20331.70245*G #N
OEW=10658*G #N
CL_MAX_L=2.7
CL_CRUISE=0.341
CL_CLEAN=1.8
RHO=1.225 #kg/m**3
S=55.4 #m**2 wing surface area

#MTOW MASS SIMPLIFCIATIO AIRPLANE DOES NOT LAND AT MTOW
V_S0=math.sqrt((2*MTOW)/(RHO*CL_MAX_L*S))
V_S1=math.sqrt((2*MTOW)/(RHO*CL_CLEAN*S))




