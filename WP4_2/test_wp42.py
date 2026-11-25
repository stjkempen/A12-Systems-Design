# test_wp42.py
#CLAUDE code that tests the ODE solver using the right parameters and data.
#ODE solver is easily adaptable to different data types, so this is a good 
# test to see if the solver works with real data.

#19 points - already interpolated from WP4_1, so no need to interpolate here.

from pathlib import Path
import sys

repo = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo))

import numpy as np
import scipy as sp
from scipy import interpolate, integrate
import matplotlib.pyplot as plt

from WP4_2.ODE_solver import solve_deflection_rk4

# ---------------- paths (relative to the repo) ----------------
file_a0 = repo / "WP4_1" / "alpha0.txt"
file_a10 = repo / "WP4_1" / "alpha10.txt"
file_airfoil = repo / "NASA SC(2)-0612 AIRFOIL.dat"

# ---------------- aircraft data (from root_interface.py / V-n diagrams.py) ----------------
c_root = 3.19          # [m]
b = 22.25              # total span [m]
taper = 0.316
half_span = b / 2
s_wing = 55.4          # [m^2]
mtow = 20331.70245     # [kg]
g0 = 9.81

# ---------------- PLACEHOLDER wing box ----------------
front_spar_xc = 0.15
rear_spar_xc = 0.60
t_spar = 0.006         # [m]
t_skin = 0.004         # [m]
shear_centre_xc = 0.5 * (front_spar_xc + rear_spar_xc)   # reader: shear centre = centroid, ~mid-box

# ---------------- load source ----------------
# False: dummy elliptic lift, no files from WP4_1 needed (use this until WP4_1 is done)
# True:  real xflr5 data from WP4_1/alpha0.txt and alpha10.txt
use_xflr5 = False
cm_dummy = -0.086      # section cm about c/4, roughly what xflr5 gives for this wing

# ---------------- PLACEHOLDER load case ----------------
# cs25.337: n_max = 2.1 + 24000 / (w + 10000), w in lb
w_lb = mtow / 0.454
n_load = min(max(2.1 + 24000 / (w_lb + 10000), 2.5), 3.8)
rho = 1.225            # sea level [kg/m^3]
v_eas = 140.0          # [m/s], placeholder speed


def chord(y):
    return c_root - c_root * (1 - taper) * y / half_span


def read_xflr5(path):
    # returns total CL and the positive-y spanwise data (y, cl, cm)
    cl_total = None
    rows = []
    reading = False
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("CL ") and cl_total is None:
                cl_total = float(line.split("=")[1])
            if "y-span" in line:
                reading = True
                continue
            if "Main Wing Cp Coefficients" in line:
                break
            if reading and line.strip():
                parts = line.split()
                if float(parts[0]) > 0:
                    rows.append([float(parts[0]), float(parts[3]), float(parts[7])])
    rows = np.array(rows)
    return cl_total, rows[:, 0], rows[:, 1], rows[:, 2]


def read_airfoil(path):
    # selig format: trailing edge -> upper surface -> leading edge -> lower surface
    data = np.loadtxt(path, skiprows=1)
    i_le = np.argmin(data[:, 0])
    upper = data[: i_le + 1][::-1]   # flip so x increases
    lower = data[i_le:]
    z_up = sp.interpolate.interp1d(upper[:, 0], upper[:, 1])
    z_lo = sp.interpolate.interp1d(lower[:, 0], lower[:, 1])
    return z_up, z_lo


def box_properties(y, z_up, z_lo, n_seg=50):
    # thin-walled trapezoidal box: 2 spar webs + 2 straight skins, no stringers
    # discretised into small segments; returns ixx about the centroid [m^4] and j [m^4]
    c = chord(y)
    xf, xr = front_spar_xc * c, rear_spar_xc * c
    zf_up, zf_lo = z_up(front_spar_xc) * c, z_lo(front_spar_xc) * c
    zr_up, zr_lo = z_up(rear_spar_xc) * c, z_lo(rear_spar_xc) * c

    # corners of the box, going round: front-bottom, front-top, rear-top, rear-bottom
    corners = [(xf, zf_lo), (xf, zf_up), (xr, zr_up), (xr, zr_lo)]
    thickness = [t_spar, t_skin, t_spar, t_skin]   # front spar, top skin, rear spar, bottom skin

    areas, zs = [], []
    ds_over_t = 0.0
    for i in range(4):
        (x1, z1), (x2, z2) = corners[i], corners[(i + 1) % 4]
        length = np.hypot(x2 - x1, z2 - z1)
        ds_over_t += length / thickness[i]
        for k in range(n_seg):
            frac = (k + 0.5) / n_seg
            areas.append(thickness[i] * length / n_seg)
            zs.append(z1 + frac * (z2 - z1))
    areas, zs = np.array(areas), np.array(zs)

    z_c = np.sum(areas * zs) / np.sum(areas)
    ixx = np.sum(areas * (zs - z_c) ** 2)

    # enclosed area (shoelace) and bredt-batho torsional constant
    xs = np.array([p[0] for p in corners])
    zc = np.array([p[1] for p in corners])
    enclosed = 0.5 * abs(np.dot(xs, np.roll(zc, -1)) - np.dot(zc, np.roll(xs, -1)))
    j = 4 * enclosed ** 2 / ds_over_t
    return ixx, j


def build_loads(y_grid):
    # lift and pitching moment per unit span, then shear, moment and torque
    q = 0.5 * rho * v_eas ** 2
    cl_req = n_load * mtow * g0 / (q * s_wing)
    c = chord(y_grid)

    if use_xflr5:
        # real xflr5 data from WP4_1 (only once that work package is ready)
        cl0_tot, y0, cl0, cm0 = read_xflr5(file_a0)
        cl10_tot, y10, cl10, cm10 = read_xflr5(file_a10)
        k = (cl_req - cl0_tot) / (cl10_tot - cl0_tot)
        cl_func = sp.interpolate.interp1d(y0, cl0 + k * (cl10 - cl0), kind="cubic", fill_value="extrapolate")
        cm_func = sp.interpolate.interp1d(y0, cm0 + k * (cm10 - cm0), kind="cubic", fill_value="extrapolate")
        lift = q * c * cl_func(y_grid)             # [N/m]
        pitch = q * c ** 2 * cm_func(y_grid)       # [N m/m], about c/4
    else:
        # DUMMY loads, no files needed: elliptic lift scaled so the half wing carries n*W/2
        shape = np.sqrt(np.clip(1 - (y_grid / half_span) ** 2, 0, None))
        shape_area = sp.integrate.trapezoid(shape, y_grid)
        lift = n_load * mtow * g0 / 2 * shape / shape_area     # [N/m]
        pitch = q * c ** 2 * cm_dummy                          # [N m/m], constant cm about c/4

    # torque about the shear centre: lift acts at c/4, ahead of the shear centre -> nose-up
    arm = (shear_centre_xc - 0.25) * c
    torque_dist = lift * arm + pitch               # [N m/m]

    # integrate from the tip inwards (reader appendix c): s(tip) = 0, m(tip) = 0, t(tip) = 0
    def from_tip(f):
        return -sp.integrate.cumulative_trapezoid(f[::-1], y_grid[::-1], initial=0)[::-1]

    shear = from_tip(lift)            # s(y)  = int_y^L w dy
    moment = -from_tip(shear)         # -m(y) = int_y^L s dy  -> upward lift gives negative m
    torque = from_tip(torque_dist)    # t(y)  = int_y^L (q d + t) dy

    return {"cl_req": cl_req, "lift": lift, "shear": shear, "moment": moment, "torque": torque}


def run(n_points):
    y = np.linspace(0.0, half_span, n_points)
    loads = build_loads(y)
    z_up, z_lo = read_airfoil(file_airfoil)
    props = np.array([box_properties(yi, z_up, z_lo) for yi in y])
    result = solve_deflection_rk4(y, loads["moment"], loads["torque"], props[:, 0], props[:, 1])
    return y, loads, props, result


if __name__ == "__main__":
    y, loads, props, res = run(201)

    print("load case: n = %.2f, V = %.0f m/s, rho = %.3f -> CL required = %.2f"
          % (n_load, v_eas, rho, loads["cl_req"]))
    print("half-wing lift = %.0f N   (should be n*W/2 = %.0f N)"
          % (loads["shear"][0], n_load * mtow * g0 / 2))
    print("root: M = %.0f N m, T = %.0f N m, Ixx = %.2e m^4, J = %.2e m^4"
          % (loads["moment"][0], loads["torque"][0], props[0, 0], props[0, 1]))
    print("tip deflection = %.3f m   (limit 0.15 b = %.3f m)  -> %s"
          % (res["v_tip"], 0.15 * b, "OK" if res["v_tip"] <= 0.15 * b else "FAIL"))
    print("tip twist      = %.2f deg (limit +/-10 deg)        -> %s"
          % (np.degrees(res["phi_tip"]), "OK" if abs(np.degrees(res["phi_tip"])) <= 10 else "FAIL"))

    # grid convergence: tip values should not move when the grid is refined
    for n in [51, 101, 201, 401]:
        _, _, _, r = run(n)
        print("points = %3d   v_tip = %.6f m   phi_tip = %.6f deg" % (n, r["v_tip"], np.degrees(r["phi_tip"])))

    fig, ax = plt.subplots(2, 2, figsize=(11, 7))
    ax[0, 0].plot(y, loads["moment"] / 1e3); ax[0, 0].set_ylabel("M [kN m]")
    ax[0, 1].plot(y, loads["torque"] / 1e3); ax[0, 1].set_ylabel("T [kN m]")
    ax[1, 0].plot(res["y"], res["v"]); ax[1, 0].set_ylabel("v [m]")
    ax[1, 1].plot(res["y"], np.degrees(res["phi"])); ax[1, 1].set_ylabel("phi [deg]")
    for a in ax.flat:
        a.set_xlabel("y [m]")
        a.grid(True)
    plt.tight_layout()
    plt.show()