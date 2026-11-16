import scipy as sp

#calculates dynamic pressure q:
def q(rho, V):
    return 0.5*rho*V*V

#calculates chord length along span (based on trapezoidal planform)
#y measured from the root (y=0) to the tip (y=b/2)
def chord(y, c_root, c_tip, b):
    return c_root - (c_root - c_tip) * (2*y/b)



#function that converts non-dimensional distributions from xlfr to dimensional based on dynamic pressure.
#returns L'(y) [N/m], D'(y) [N/m] and M'(y) [Nm/m] as functions of y
def nonDimensionalDist(cl, cd, cm, q_inf, c_root, c_tip, b):
    def L_prime(y):
        return q_inf * chord(y, c_root, c_tip, b) * cl(y)
    def D_prime(y):
        return q_inf * chord(y, c_root, c_tip, b) * cd(y)
    def M_prime(y):
        return q_inf * chord(y, c_root, c_tip, b)**2 * cm(y)
    return L_prime, D_prime, M_prime


#gets correct distributions from the CL at a certain flight condtiion. Based on n-V diagrams.
#also depends on distributions at 0, and 10 degrees.
#CL0, CL10: overall wing lift coefficients at 0 and 10 degrees (scalars from xflr)
#cl0, cl10, cm0, cm10: spanwise distributions at 0 and 10 degrees (functions of y)
def getDistFromCL(req_CL, CL0, CL10, cl0, cl10, cm0, cm10):
    #interpolation factor, same for all three distributions
    k = (req_CL - CL0) / (CL10 - CL0)
    def cl(y):
        return cl0(y) + k*(cl10(y) - cl0(y))
    def cm(y):
        return cm0(y) + k*(cm10(y) - cm0(y))
    alpha = k*10
    return cl, cm, alpha



