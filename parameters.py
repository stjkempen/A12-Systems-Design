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

#weight parameters
wing_weight = 1503 #kg
fuel_weight_max = 2646.28 #kg
W_engine = 830 #kg
#--- material properties AL2024-T81 ---
E=72.4e9 #pa
G=28e9 #pa