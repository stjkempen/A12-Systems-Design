import numpy as np
from pathlib import Path
import scipy as sp
import matplotlib.pyplot as plt

script_folder = Path(__file__).resolve().parent
file_path = script_folder / "alpha0.txt"
#list for the relevant data
ylst = []
Cllst = []
Cdlst = []
Cmlst = []

def readxflr():
    with file_path.open("r", encoding="utf-8") as file:          #Data for 0 deg angle of attack
        read=False
        for line in file:
            #skipping empty lines:
            if not line.strip():
                continue
            # skipping to the relevant data
            if  "y-span" in line:
                read=True            
                continue
            if read==False:
                continue 
            #break loop after useful data is extracted
            if "Main Wing Cp Coefficients" in line:
                break
            # putting all the data into lists
            lst=line.split()
            if float(lst[0]) < 0: #only consider half-wing with positive spanwise position
                continue
            ylst.append(float(lst[0]))
            Cllst.append(float(lst[3]))
            Cdlst.append(float(lst[5]))
            Cmlst.append(float(lst[7]))
        
    print(ylst)
    print(Cllst)

    #interpolating the data
    Clf = sp.interpolate.interp1d(ylst,Cllst,kind='cubic',fill_value="extrapolate")
    Cdf = sp.interpolate.interp1d(ylst,Cdlst,kind='cubic',fill_value="extrapolate")
    Cmf = sp.interpolate.interp1d(ylst,Cmlst,kind='cubic',fill_value="extrapolate")
    """
    #plotting for sanity check
    y_plot = np.linspace(min(ylst), max(ylst), 500)
    Cl_plot = Clf(y_plot)
    Cd_plot = Cdf(y_plot)
    Cm_plot = Cmf(y_plot)
            # Create three plots
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Lift coefficient
    axes[0].scatter(ylst, Cllst, color="red", label="XFLR5 data")
    axes[0].plot(y_plot, Cl_plot, color="blue", label="Cubic interpolation")
    axes[0].set_xlabel("Spanwise position, y [m]")
    axes[0].set_ylabel(r"$C_l$")
    axes[0].set_title("Sectional lift coefficient")
    axes[0].grid(True)
    axes[0].legend()

    # Drag coefficient
    axes[1].scatter(ylst, Cdlst, color="red", label="XFLR5 data")
    axes[1].plot(y_plot, Cd_plot, color="blue", label="Cubic interpolation")
    axes[1].set_xlabel("Spanwise position, y [m]")
    axes[1].set_ylabel(r"$C_d$")
    axes[1].set_title("Sectional drag coefficient")
    axes[1].grid(True)
    axes[1].legend()

    # Pitching-moment coefficient
    axes[2].scatter(ylst, Cmlst, color="red", label="XFLR5 data")
    axes[2].plot(y_plot, Cm_plot, color="blue", label="Cubic interpolation")
    axes[2].set_xlabel("Spanwise position, y [m]")
    axes[2].set_ylabel(r"$C_m$")
    axes[2].set_title("Sectional pitching-moment coefficient")
    axes[2].grid(True)
    axes[2].legend()

    plt.tight_layout()
    plt.show() """

    #Data for 10 deg angle of attack

    script_folder = Path(__file__).resolve().parent
    file_path = script_folder / "alpha10.txt"

    with file_path.open("r", encoding="utf-8") as file2:         
        
        for line in file2:
            #skipping empty lines:
            if not line.strip():
                continue
            # skipping to the relevant data
            if  "y-span" in line:
                read=True            
                continue
            if read==False:
                continue 
            #break loop after useful data is extracted
            if "Main Wing Cp Coefficients" in line:
                break
            # putting all the data into lists
            lst=line.split()
            if float(lst[0]) < 0: #only consider half-wing with positive spanwise position
                continue
            ylst.append(float(lst[0]))
            Cllst.append(float(lst[3]))
            Cdlst.append(float(lst[5]))
            Cmlst.append(float(lst[7]))
        
    print(ylst)
    print(Cllst)

    #interpolating the data
    Clf10 = sp.interpolate.interp1d(ylst,Cllst,kind='cubic',fill_value="extrapolate")
    Cdf10 = sp.interpolate.interp1d(ylst,Cdlst,kind='cubic',fill_value="extrapolate")
    Cmf10 = sp.interpolate.interp1d(ylst,Cmlst,kind='cubic',fill_value="extrapolate")
    return Clf, Clf10, Cdf, Cdf10, Cmf, Cmf10

