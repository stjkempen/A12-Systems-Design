import numpy as np
from pathlib import Path
import scipy as sp
import matplotlib.pyplot as plt

script_folder = Path(__file__).resolve().parent


def readfile(filename):
    """Reads one xflr5 output file.
    Returns cubic interpolants Cl(y), Cd(y), Cm(y) for the half-wing (y >= 0)
    and the total wing lift coefficient CL from the file header."""
    file_path = script_folder / filename
    #list for the relevant data
    ylst = []
    Cllst = []
    Cdlst = []
    Cmlst = []
    CL = None

    with file_path.open("r", encoding="utf-8") as file:
        read = False
        for line in file:
            #skipping empty lines:
            if not line.strip():
                continue
            #total wing lift coefficient from the header
            if not read and line.split()[0] == "CL":
                CL = float(line.split("=")[1])
                continue
            # skipping to the relevant data
            if "y-span" in line:
                read = True
                continue
            if read == False:
                continue
            #break loop after useful data is extracted
            if "Main Wing Cp Coefficients" in line:
                break
            # putting all the data into lists
            lst = line.split()
            if float(lst[0]) < 0: #only consider half-wing with positive spanwise position
                continue
            ylst.append(float(lst[0]))
            Cllst.append(float(lst[3]))
            Cdlst.append(float(lst[5]))
            Cmlst.append(float(lst[7]))

    #interpolating the data
    Clf = sp.interpolate.interp1d(ylst, Cllst, kind='cubic', fill_value="extrapolate")
    Cdf = sp.interpolate.interp1d(ylst, Cdlst, kind='cubic', fill_value="extrapolate")
    Cmf = sp.interpolate.interp1d(ylst, Cmlst, kind='cubic', fill_value="extrapolate")
    return Clf, Cdf, Cmf, CL


def readxflr():
    """Returns Clf, Clf10, Cdf, Cdf10, Cmf, Cmf10, CL0, CL10
    (distributions at 0 and 10 deg angle of attack + total wing CLs)."""
    Clf, Cdf, Cmf, CL0 = readfile("alpha0.txt")          #Data for 0 deg angle of attack
    Clf10, Cdf10, Cmf10, CL10 = readfile("alpha10.txt")  #Data for 10 deg angle of attack
    return Clf, Clf10, Cdf, Cdf10, Cmf, Cmf10, CL0, CL10


def plotxflr(Clf, Cdf, Cmf, y_max):
    """Plot of the interpolated distributions, for sanity check."""
    y_plot = np.linspace(0, y_max, 500)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, f, label in zip(axes, (Clf, Cdf, Cmf), (r"$C_l$", r"$C_d$", r"$C_m$")):
        ax.plot(y_plot, f(y_plot), label="Cubic interpolation")
        ax.scatter(f.x, f.y, color="red", s=10, label="XFLR5 data")
        ax.set_xlabel("Spanwise position, y [m]")
        ax.set_ylabel(label)
        ax.grid(True)
        ax.legend()
    plt.tight_layout()
    plt.show()
