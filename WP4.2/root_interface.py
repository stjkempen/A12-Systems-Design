"""
houses root interface where user can put in shape of wing box -- assumed trapezoid

h_frontspar
h_rearspar

before identifying centroid, the coordinate system is set to left bottem corner trapezoid

"""
import numpy as np
from math import sqrt


def trap_elements(h_frontspar,h_rearspar, pos_frontspar,pos_rearspar,thickness,rear_offset = 0):
    # --- define side contributions ---
    frontspar={"area" : h_frontspar*thickness,"centroid" : np.array([pos_frontspar,0.5*h_frontspar])}
    rearspar={"area" : h_rearspar*thickness,"centroid" : np.array([pos_rearspar,0.5*h_rearspar+rear_offset])}

    topspar={"area":sqrt((pos_rearspar-pos_frontspar)**2+((h_frontspar-h_rearspar)/2+rear_offset)**2), 
             "centroid": np.array([(pos_rearspar-pos_frontspar)/2,(h_frontspar+h_rearspar+rear_offset)/2])}
    
    bottemspar={"area":sqrt((pos_rearspar-pos_frontspar)**2+((h_frontspar-h_rearspar)/2-rear_offset)**2), 
             "centroid": np.array([(pos_rearspar-pos_frontspar)/2,(rear_offset)/2])}
    
    elements=[frontspar,rearspar,topspar,bottemspar]
    return elements

def stringer(area: float, centroid: list):
    stringer={"area": area, "centroid" : centroid}
    return stringer


def J_from_elements(*elements):
    total_area=sum(elem["area"] for elem in elements)
    centroid=np.array([elem["area"]**2*elem["centroid"] for elem in elements])/total_area**2




# -> J(z)

