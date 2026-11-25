import numpy as np
import matplotlib.pyplot as plt

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from parameters import G, E, b


def rk4_fixed(f_grid, s0, y_grid):
    n = len(y_grid) - 1

    if n % 2 != 0:
        raise ValueError("number of grid intervals must be even (odd number of points)")
    #avoids interpolation - exact values for all the points

    h = y_grid[2] - y_grid[0] #step size
    s = np.array(s0, dtype=float)

    y_out = [y_grid[0]]
    s_out = [s.copy()]

    for k in range (0, n, 2):
        k1 = f_grid(k,s)
        k2 = f_grid(k + 1, s + h / 2 * k1)
        k3 = f_grid(k + 1, s + h / 2 * k2)
        k4 = f_grid(k + 2, s + h * k3)
        s = s + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

        y_out.append(y_grid[k + 2])
        s_out.append(s.copy())

    return np.array(y_out), np.array(s_out)


def solve_deflection_rk4(y_grid, m_grid, t_grid, ixx_grid, j_grid):
    # inputs: all arrays on the same uniform grid from root (y = 0) to tip (y = b/2)
    #   y_grid    spanwise stations [m], odd number of points
    #   m_grid    bending moment [N m]
    #   t_grid    torque [N m]
    #   ixx_grid  second moment of area [m^4]
    #   j_grid    torsional constant [m^4]
    #   e, g      young's and shear modulus [Pa]
    # returns dict with arrays on the step points + tip values
    e=E
    g=G

    y_grid = np.asarray(y_grid, dtype=float)
    dy = np.diff(y_grid)
    if not np.allclose(dy, dy[0]):
        raise ValueError("y_grid must be uniform")

    # pre-compute the two forcing terms on the grid (they depend on y only)
    curvature = -np.asarray(m_grid) / (e * np.asarray(ixx_grid))
    twist_rate = np.asarray(t_grid) / (g * np.asarray(j_grid))

    def f_grid(k, s):
        # s = [v, dv/dy, phi]
        return np.array([s[1], curvature[k], twist_rate[k]])

    y_out, s_out = rk4_fixed(f_grid, [0.0, 0.0, 0.0], y_grid)

    return {
        "y": y_out,
        "v": s_out[:, 0],
        "dvdy": s_out[:, 1],
        "phi": s_out[:, 2],
        "v_tip": s_out[-1, 0],
        "phi_tip": s_out[-1, 2],
    }

def verify():
    # 1) uniform load + constant torque, constant ixx and j (hand calculation)
    # 2) grid convergence: tip values must not change when the grid is refined
    length = 15.0
    w = 10000.0
    t0 = 5000.0
    ixx_val = 1e-3
    j_val = 2e-3

    v_exact = w * length ** 4 / (8 * E * ixx_val)
    phi_exact = t0 * length / (G * j_val)

    for n_points in [11, 21, 41, 81]:
        y = np.linspace(0.0, length, n_points)
        result = solve_deflection_rk4(
            y,
            m_grid=-w * (length - y) ** 2 / 2,
            t_grid=np.full_like(y, t0),
            ixx_grid=np.full_like(y, ixx_val),
            j_grid=np.full_like(y, j_val),
        )
        print("points = %3d   v_tip error = %.2e   phi_tip error = %.2e"
              % (n_points,
                 abs(result["v_tip"] - v_exact) / v_exact,
                 abs(result["phi_tip"] - phi_exact) / phi_exact))

def deflection(y,M, T,Ix,J):
    res = solve_deflection_rk4(y_grid=y, m_grid=M, t_grid=T, ixx_grid=Ix, j_grid=J)

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



if __name__ == "__main__":
    verify()




