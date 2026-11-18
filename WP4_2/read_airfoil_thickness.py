import numpy as np
from scipy.interpolate import interp1d

def get_airfoil_thickness(target_xc):
    filepath="NASA SC(2)-0612 AIRFOIL.dat"
    #load data, skip header, handle whitespace
    
    data = np.genfromtxt(filepath, skip_header=1)
    x = data[:, 0]
    y = data[:, 1]

    #split upper and lower surface

    le_index = np.argmin(x)

    x_upper = x[:le_index+1]
    y_upper = y[:le_index+1]

    x_lower = x[le_index:]
    y_lower = y[le_index:]

    #take x strictly increasing for interpolation

    upper_sorted_idx = np.argsort(x_upper)
    x_upper = x_upper[upper_sorted_idx]
    y_upper = y_upper[upper_sorted_idx]

    lower_sorted_idx = np.argsort(x_lower)
    x_lower = x_lower[lower_sorted_idx]
    y_lower = y_lower[lower_sorted_idx]

    #interpolation functions

    f_upper = interp1d(x_upper, y_upper, kind='linear', bounds_error=False, fill_value='extrapolate')
    f_lower = interp1d(x_lower, y_lower, kind='linear', bounds_error=False, fill_value='extrapolate')

    #compute thickness at require x/c

    y_u = f_upper(target_xc)
    y_l = f_lower(target_xc)

    thickness = y_u - y_l

    return thickness