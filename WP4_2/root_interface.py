"""
houses root interface where user can put in shape of wing box -- assumed trapezoid

h_frontspar
h_rearspar

before identifying centroid, the coordinate system is set to left bottem corner trapezoid

"""
import numpy as np

from parameters import c_root, b, taper
from WP4_2.read_airfoil_thickness import get_airfoil_thickness
#--- parameters ---

# --- planform geometry ---
def chord(y):
    c=c_root-c_root*(1-taper)*y/(b/2)
    return c


def trap_elements(y, pos_frontspar, pos_rearspar, thickness, rear_offset=0):
    c = chord(y)
    x_f, x_r = pos_frontspar*c, pos_rearspar*c
    h_f = get_airfoil_thickness(pos_frontspar)*c
    h_r = get_airfoil_thickness(pos_rearspar)*c
    off = rear_offset*c
    dx = x_r - x_f

    frontspar = {"area": h_f*thickness, "centroid": np.stack([x_f, 0.5*h_f])}
    rearspar  = {"area": h_r*thickness, "centroid": np.stack([x_r, 0.5*h_r + off])}
    topspar   = {"area": np.sqrt(dx**2 + (h_r + off - h_f)**2)*thickness,
                 "centroid": np.stack([(x_f + x_r)/2, (h_f + h_r + off)/2])}
    bottomspar = {"area": np.sqrt(dx**2 + off**2)*thickness,
                  "centroid": np.stack([(x_f + x_r)/2, off/2])}
    return [frontspar, rearspar, topspar, bottomspar]


def stringer(area, centroid):
    return {"area": area, "centroid": np.array(centroid, dtype=float)[:, None]}

def skin_stringers(y, pos_frontspar, pos_rearspar, n_top,n_bottom, area, rear_offset=0):
    """Equally spaced stringers on the top and bottom skins (n_per_side each).
    `area` is the area of each stringer; the spar positions and rear_offset
    are the same as in trap_elements (fractions of chord)."""
    if n_top < 1 and n_bottom < 1:
        return []

    c = chord(y)
    x_f, x_r = pos_frontspar*c, pos_rearspar*c
    h_f = get_airfoil_thickness(pos_frontspar)*c
    h_r = get_airfoil_thickness(pos_rearspar)*c
    off = rear_offset*c

    
    a = np.full(np.shape(x_f), area, dtype=float)         # same shape as y

    elements = []
    t_top = np.arange(1, n_top + 1) / (n_top + 1)   # interior fractions
    for ti in t_top:
        x = x_f + ti*(x_r - x_f)
        y_top = h_f + ti*(h_r + off - h_f)
        elements.append({"area": a.copy(), "centroid": np.stack([x, y_top])})

    t_bottom = np.arange(1, n_bottom + 1) / (n_bottom + 1)   # interior fractions
    for ti in t_bottom:
        x = x_f + ti*(x_r - x_f)
        y_bot = ti*off
        elements.append({"area": a.copy(), "centroid": np.stack([x, y_bot])})
    
    return elements


def moments_from_elements(*elements):
    total_area = sum(e["area"] for e in elements)
    centroid = sum(e["area"]*e["centroid"] for e in elements) / total_area
    J = Ix = Iy = 0
    for e in elements:
        d = e["centroid"] - centroid          # new variable, no mutation
        Ix += d[1]**2 * e["area"]             # about the horizontal axis
        Iy += d[0]**2 * e["area"]
        J  += np.sum(d**2, axis=0) * e["area"]
    return J, Ix, Iy