"""put all the semi-constant parameters here, if you want to see the effect of changing a variable overrite it in the main file"""

#--- design parameters ---
pos_frontspar=0.3
pos_rearspar=0.7
thickness=1e-2


#-- fixed planform parameters ---
c_root=3.19 #m
c_tip=1.01 #m
b=22.25 #m
taper=0.316 
wing_surface = 46.6844 #m^2

n = 1.0 #loading factor

engine_spanwise_pos = 0.35 # 35% of semi wing span
engine_torsion_moment_arm = 1 #m, correct later, I have no idea just wrote something here
Thrust_max = 68000 #N, in take-off, per engine
Thrust_current = 68000 #N change corresponding to flight conditions you want to plot the internal loads to
#weight parameters
wing_weight = 1503 #kg
fuel_weight_max = 2646.28 #kg
W_engine = 830 #kg
MTOW = 20733 #kg
#--- material properties AL2024-T81 ---
E=72.4e9 #pa
G=28e9 #pa

#atmosphere parameters
RHO    = 1.225   # air density [kg/m^3]
GAMMA_AIR=1.4 #specific heat air air
R=287 #unviersal gas constnat
V_INF  = 70.0    # airspeed [m/s]
gravity = 9.81  # gravitational acceleration [m/s^2]

# --- V-n param ---
S_F=1.5  #Safety factor of 1.5 as per CS regulations

CL_MAX_L=2.7
CL_CR=0.341
CL_CLEAN=1.8

altitudes=[0,10668]

"""HEIGHT SELECTION"""
H=altitudes[0] #m   default altitude is surface


T_SURF=288.15 #K
T_CR=218.81 #K
KG_TO_LBF = 2.20462
# Convert MTOW (kg) to lbf, then clamp between 2.5 and 3.8 per CS 25.337(b)
n_raw = 2.1 + (24000 / ((MTOW * KG_TO_LBF) + 10000))
N_MAX = round(min(max(n_raw, 2.5), 3.8), 1)
N_MAX_FLAPS=2
M_C=0.77    #CRUISE MACH
V_S0=0
V_S1=0
# -----------------------------------------------------------------------
# accuracy param:
n_of_spanwise_pos = 5001