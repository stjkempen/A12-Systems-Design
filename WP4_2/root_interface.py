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
    t = thickness*chord(y)/chord(0)

    def vertical_plate(h):                      # spars
        return t*h**3/12, h*t**3/12             # own I_x, I_y

    def inclined_plate(l, theta):               # skins
        s, co = np.sin(theta), np.cos(theta)
        return (t*l*(l**2*s**2 + t**2*co**2)/12,
                t*l*(l**2*co**2 + t**2*s**2)/12)

    l_top = np.sqrt(dx**2 + (h_r + off - h_f)**2)
    l_bot = np.sqrt(dx**2 + off**2)
    th_top = np.arctan2(h_r + off - h_f, dx)
    th_bot = np.arctan2(off, dx)

    def element(area, centroid, own):
        return {"area": area, "centroid": centroid, "I_x": own[0], "I_y": own[1]}

    return [
        element(h_f*t, np.stack([x_f, 0.5*h_f]), vertical_plate(h_f)),
        element(h_r*t, np.stack([x_r, 0.5*h_r + off]), vertical_plate(h_r)),
        element(l_top*t, np.stack([(x_f + x_r)/2, (h_f + h_r + off)/2]),
                inclined_plate(l_top, th_top)),
        element(l_bot*t, np.stack([(x_f + x_r)/2, off/2]),
                inclined_plate(l_bot, th_bot)),
    ]


def stringer(area, centroid):
    return {"area": area, "centroid": np.array(centroid, dtype=float)[:, None],
            "I_x": 0, "I_y": 0}



def skin_stringers(y, pos_frontspar, pos_rearspar, n_top,n_bottom, A_str_root, rear_offset=0):
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

    
    a = A_str_root*(1+(taper**2-1)*(2*y/b))         # same shape as y
    a=np.clip(a,a_min=100e-6,a_max=None)
    elements = []
    t_top = np.arange(1, n_top + 1) / (n_top + 1)   # interior fractions
    for ti in t_top:
        x_top = x_f + ti*(x_r - x_f)
        y_top = h_f + ti*(h_r + off - h_f)
        elements.append({"I_x" : 0,"I_y": 0,"area": a.copy(), "centroid": np.stack([x_top, y_top])})

    t_bottom = np.arange(1, n_bottom + 1) / (n_bottom + 1)   # interior fractions
    for ti in t_bottom:
        x = x_f + ti*(x_r - x_f)
        y_bot = ti*off
        elements.append({"I_x" : 0,"I_y": 0,"area": a.copy(), "centroid": np.stack([x, y_bot])})
    
    return elements


def moments_from_elements(*elements):
    total_area = sum(e["area"] for e in elements)
    centroid = sum(e["area"]*e["centroid"] for e in elements) / total_area
    Ix = Iy = 0
    for e in elements:
        d = e["centroid"] - centroid
        Ix += d[1]**2 * e["area"] + e["I_x"]    # vertical offset -> bending about horizontal axis
        Iy += d[0]**2 * e["area"] + e["I_y"]
    I_p = Ix + Iy                                 # I_p is polar moment of area
    return I_p, Ix, Iy

def torsion_constant(y, pos_frontspar, pos_rearspar, thickness, rear_offset=0):
    c = chord(y)
    x_f, x_r = pos_frontspar*c, pos_rearspar*c
    h_f = get_airfoil_thickness(pos_frontspar)*c
    h_r = get_airfoil_thickness(pos_rearspar)*c
    off = rear_offset*c
    dx = x_r - x_f

    l_top = np.sqrt(dx**2 + (h_r + off - h_f)**2)
    l_bot = np.sqrt(dx**2 + off**2)

    # enclosed area of the quadrilateral with corners
    # (x_f,0), (x_r,off), (x_r,off+h_r), (x_f,h_f)
    A_m = 0.5*dx*(h_f + h_r)

    return 4*A_m**2 / ((h_f + h_r + l_top + l_bot)/thickness)