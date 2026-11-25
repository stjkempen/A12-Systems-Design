#PACKAGES
import math
import matplotlib.pyplot as plt
import numpy as np


from parameters import *


#Constants

'''IF ALTITUDE NOT SPECIFIED IT IS SURFACE BY DEFAULT'''



def rho(H):
    if H==0:
        rho=1.225
    else:
        rho=0.3796
    return rho
SIGMA=rho(altitudes[1])/rho(altitudes[0]) #-------conversion to EAS



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
MPW=9302 #kg,     MAXIMUM PAYLOAD 
MASS_1=10820 #kg,  OEM
MASS_2=MASS_1+MPW+(MTOW-MASS_1-MPW)  #OEM + MPW + MAX FUEL
MASS_3=MASS_1+MPW  #OEM + MPW

MASSES_LIST = sorted([MASS_1, MASS_2, MASS_3])




#MTOW MASS SIMPLIFCIATIO AIRPLANE DOES NOT LAND AT MTOW


"""V_C CALCULATIONS"""
CL_MAX_NEG = -1.0   
N_NEG = -1.0        

fig, axes = plt.subplots(len(altitudes), len(MASSES_LIST), figsize=(16, 9),
                         sharex=True, sharey=True)

for i, H in enumerate(altitudes):

    """mass-independent velocities"""

    if H==0:
        V_CR=round(0.77*M(H)*math.sqrt(SIGMA),2)
        V_D=round(1.25*V_CR,2)
    else:
        V_CR=round(0.77*M(H)*math.sqrt(SIGMA),2)
        M_D=M_C+0.05
        V_D=round(M(H)*M_D*math.sqrt(SIGMA),2)

    """Mass-dependent velocities"""
    
    for j, mass in enumerate(MASSES_LIST):  
        V_S0=round(float(math.sqrt((2*mass*gravity)/(rho(0)*CL_MAX_L*wing_surface))),2)
        V_S1=round(math.sqrt(((2*mass*gravity)/(rho(0)*CL_CLEAN*wing_surface))),2)
        V_A=round(V_S1*math.sqrt(N_MAX),2)
        V_F=round(max(1.6*V_S1, 1.8*V_S0,),2)


                # ---------- V-n diagram ----------
        k = 0.5*rho(0)*wing_surface/(mass*gravity)                 
        V_neg = math.sqrt(abs(N_NEG)/(k*abs(CL_MAX_NEG)))
        V_Af = V_S0*math.sqrt(N_MAX_FLAPS)

        # envelope, clean
        v_pos = np.linspace(0, V_A, 100)
        n_pos = k*CL_CLEAN*v_pos**2
        v_ng = np.linspace(0, V_neg, 100)
        n_ng = -k*abs(CL_MAX_NEG)*v_ng**2
        clean_v = np.concatenate([v_pos, [V_D, V_D, V_CR], v_ng[::-1]])
        clean_n = np.concatenate([n_pos, [N_MAX, 0, N_NEG], n_ng[::-1]])

        # flaps-extended envelope
        v_f = np.linspace(0, V_Af, 100)
        n_f = k*CL_MAX_L*v_f**2
        flap_v = np.concatenate([v_f, [V_F, V_F]])
        flap_n = np.concatenate([n_f, [N_MAX_FLAPS, 0]])


        """plotting V-N diagrams"""


        ax = axes[i, j]
        ax.plot(clean_v, clean_n, "b-", lw=2, label="Clean")
        ax.plot(flap_v, flap_n, "r--", lw=1.5, label="Flaps extended")

        # vertical reference lines (no text, the point labels carry the names)
        for v, col in [(V_A, "gray"), (V_CR, "gray"), (V_D, "gray"), (V_F, "red")]:
            ax.axvline(v, color=col, ls=":", lw=0.8)
        ax.text(V_F, N_MAX_FLAPS + 0.1, "$V_F$", ha="left", color="red", fontsize=8)

        # the 4 critical points: (speed, n, name, text offset in points, alignment)
        crit = [
            (V_A,   N_MAX, "$V_A$",     (-4,   6), "right", "bottom"),   # min speed, max +n
            (V_D,   N_MAX, "$V_D$",     (-4,   6), "right", "bottom"),   # max speed, max +n
            (V_neg, N_NEG, "$V_{neg}$", ( 0,  -6), "center", "top"),     # min speed, max -n
            (V_CR,  N_NEG, "$V_C$",     ( 0,  -6), "center", "top"),     # max speed, max -n
        ]
        for v, n, name, off, ha, va in crit:
            ax.plot(v, n, "ko", ms=5, zorder=5)
            ax.annotate(f"{name} = {v:.0f} m/s\n$n$ = {n:.2f}",
                        xy=(v, n), xytext=off, textcoords="offset points",
                        ha=ha, va=va, fontsize=7.5)

        ax.axhline(0, color="k", lw=0.5)
        ax.set_title(f"m = {mass:.0f} kg, h = {H} m", fontsize=10)
        ax.set_xlabel("$V_{EAS}$ [m/s]", fontsize=9)
        ax.set_ylabel("$n$ [-]", fontsize=9)
        ax.set_ylim(N_NEG - 0.9, N_MAX + 0.9)

        # show tick values on every panel (sharex/sharey hides them by default)
        ax.tick_params(labelbottom=True, labelleft=True, labelsize=8)
        ax.locator_params(axis="x", nbins=6)
        ax.locator_params(axis="y", nbins=7)
        ax.grid(alpha=0.3)
        if i == 0 and j == 0:
            ax.legend(loc="lower right", fontsize=8)



fig.tight_layout()
fig.savefig("vn_diagrams.png", dpi=200)
plt.show()








