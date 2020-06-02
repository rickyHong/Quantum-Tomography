import scipy as sp
from numpy.core.defchararray import add
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import sys


"""
    makeRhoImages(p,plt_given,customColor)
    Desc: Creates matlab plots of the density matrix.

    Parameters
    ----------
    p : ndarray with shape = (n,2^numQubits,2^numQubits)
        The density matrix you want to create plots of.
    plt_given : matplotlib.pyplot
        Input pyplot for which the figures will be saved on to.
    customColor : boolean
        Specify if you want our custom colorMap. Default is true
    """
def makeRhoImages(p,plt_given,customColor = True):
    # Set up
    numQubits = int(np.log2(p.shape[0]))
    xpos = np.zeros_like(p.flatten(),dtype=float)
    ypos = np.zeros_like(p.flatten(),dtype=float)
    for i in range(0,2**numQubits):
        xpos[i*2**numQubits:(1+i)*2**numQubits] = .5+i
    for i in range(0,2**numQubits):
        ypos[i::2**numQubits] = .5+i
    zpos = np.zeros_like(p.flatten(),dtype=float)
    # width of cols
    dx = .9*np.ones_like(xpos)
    dy = .9*np.ones_like(ypos)
    # custom color map
    n_bin = 100
    if(customColor):
        from matplotlib.colors import LinearSegmentedColormap
        cmap_name = 'my_list'
        colors = [(1 / 255.0, 221 / 255.0, 137 / 255.0),
                  (32 / 255.0, 151 / 255.0, 138 / 255.0),
                  (53 / 255.0, 106 / 255.0, 138 / 255.0),
                  (86 / 255.0, 33 / 255.0, 139 / 255.0),
                  (131 / 255.0, 75 / 255.0, 114 / 255.0),
                  (173 / 255.0, 114 / 255.0, 90 / 255.0),
                  (253 / 255.0, 187 / 255.0, 45 / 255.0)]
        colorMap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
    else:
        colorMap = plt.cm.jet
    norm = mpl.colors.Normalize(vmin=-1, vmax=1)

    tickBase = ["H","V"]
    tick = [""]
    for x in range(numQubits):
        newTick = np.zeros(len(tick)*2,dtype="O")
        for i in range(len(tick)):
            for j in range(len(tickBase)):
                newTick[len(tick)*i +j] = tick[i] + tickBase[j]
        tick = newTick
    xTicks = ["|"+x+">" for x in tick]
    yTicks = ["|"+x+">" for x in tick]


    # Real Graph
    fig = plt_given.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    dz = p.flatten().astype(float)
    img = ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colorMap((dz + 1) / 2),edgecolor="black",alpha=.8)



    ax1.axes.set_xticklabels(xTicks)
    ax1.axes.set_yticklabels(yTicks)
    ax1.axes.set_xticks(range(1,2**numQubits+1))
    ax1.axes.set_yticks(range(1,2**numQubits+1))
    ax1.axes.set_zticks(np.arange(-1, 1.1, .2))
    ax1.axes.set_zlim3d(-1, 1)
    plt_given.title("Rho Real")
    fig.subplots_adjust(bottom=0.2)
    ax1 = fig.add_axes([0.2, 0.10, 0.7, 0.065])
    cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=colorMap,
                                    norm=norm,
                                    orientation='horizontal')

    # Imaginary graph
    fig = plt_given.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    dz = p.flatten().imag.astype(float)
    ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colorMap((dz + 1) / 2),edgecolor="black",alpha=.8)

    ax1.axes.set_xticklabels(xTicks)
    ax1.axes.set_yticklabels(yTicks)
    ax1.axes.set_xticks(range(1, 2 ** numQubits + 1))
    ax1.axes.set_yticks(range(1, 2 ** numQubits + 1))
    ax1.axes.set_zticks(np.arange(-1, 1.1, .2))
    ax1.axes.set_zlim3d(-1, 1)
    plt_given.title("Rho Imaginary")

    fig.subplots_adjust(bottom=0.2)
    ax1 = fig.add_axes([0.2, 0.10, 0.7, 0.065])
    cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=colorMap,
                                    norm=norm,
                                    orientation='horizontal')


"""
    printLastOutput(tomo,bounds)
    Desc: Prints the properties of the last tomography to the console. Properties are defined in tomography conf settings.
          Using bounds will not change the conf settings. The calculated properties are determined by self.err_functions.

    Parameters
    ----------
    tomo : Tomography() Object
        This is the main tomography object. It will get the data from it's last tomography and print it.
    bounds : boolean
        Set this to true if you want error bounds on your estimated property values. Default is False.
        These are determined with monte carlo simulation and the states are saved under self.mont_carl_states
    """
def printLastOutput(tomo,bounds = -1):
    p = tomo.last_rho
    print("State: ")
    print(p)
    properties = tomo.getProperties(p, bounds)
    for prop in properties:
        if(len(prop) >3):
            print(prop[0] + " : " + str(prop[1]) + " +/- " + str(prop[2]))
        else:
            print(prop[0] + " : " + str(prop[1]))

"""
    saveRhoImages(p,pathToDirectory,customColor)
    Desc: Creates and saves matlab plots of the density matrix.

    Parameters
    ----------
    p : ndarray with shape = (n,2^numQubits,2^numQubits)
        The density matrix you want to create plots of.
    pathToDirectory : string
        Path to where you want your images to be saved.
    customColor : boolean
        Specify if you want our custom colorMap. Default is true.
    """
def saveRhoImages(p,pathToDirectory,customColor = True):
    # Set up
    numQubits = int(np.log2(p.shape[0]))
    xpos = np.zeros_like(p.flatten(), dtype=float)
    ypos = np.zeros_like(p.flatten(), dtype=float)
    for i in range(0, 2 ** numQubits):
        xpos[i * 2 ** numQubits:(1 + i) * 2 ** numQubits] = .5 + i
    for i in range(0, 2 ** numQubits):
        ypos[i::2 ** numQubits] = .5 + i
    zpos = np.zeros_like(p.flatten(), dtype=float)
    # width of cols
    dx = .9 * np.ones_like(xpos)
    dy = .9 * np.ones_like(ypos)
    # custom color map
    n_bin = 100
    if (customColor):
        from matplotlib.colors import LinearSegmentedColormap
        cmap_name = 'my_list'
        colors = [(1 / 255.0, 221 / 255.0, 137 / 255.0),
                  (32 / 255.0, 151 / 255.0, 138 / 255.0),
                  (53 / 255.0, 106 / 255.0, 138 / 255.0),
                  (86 / 255.0, 33 / 255.0, 139 / 255.0),
                  (131 / 255.0, 75 / 255.0, 114 / 255.0),
                  (173 / 255.0, 114 / 255.0, 90 / 255.0),
                  (253 / 255.0, 187 / 255.0, 45 / 255.0)]
        colorMap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
    else:
        colorMap = plt.cm.jet
    norm = mpl.colors.Normalize(vmin=-1, vmax=1)

    tickBase = ["H", "V"]
    tick = [""]
    for x in range(numQubits):
        newTick = np.zeros(len(tick) * 2, dtype="O")
        for i in range(len(tick)):
            for j in range(len(tickBase)):
                newTick[len(tick) * i + j] = tick[i] + tickBase[j]
        tick = newTick
    xTicks = ["|" + x + ">" for x in tick]
    yTicks = ["|" + x + ">" for x in tick]

    # Real Graph
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    dz = p.flatten().astype(float)
    img = ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colorMap((dz + 1) / 2),edgecolor="black",alpha=.8)

    ax1.axes.set_xticklabels(xTicks)
    ax1.axes.set_yticklabels(yTicks)
    ax1.axes.set_xticks(range(1, 2 ** numQubits + 1))
    ax1.axes.set_yticks(range(1, 2 ** numQubits + 1))
    ax1.axes.set_zticks(np.arange(-1, 1.1, .2))
    ax1.axes.set_zlim3d(-1, 1)
    plt.title("Rho Real")
    fig.subplots_adjust(bottom=0.2)
    ax1 = fig.add_axes([0.2, 0.10, 0.7, 0.065])
    cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=colorMap,
                                    norm=norm,
                                    orientation='horizontal')
    plt.savefig(pathToDirectory + "/rhobarReal.png",bbox_inches = 'tight', pad_inches = 0)

    # Imaginary graph
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    dz = p.flatten().imag.astype(float)
    ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colorMap((dz + 1) / 2),edgecolor="black",alpha=.8)

    ax1.axes.set_xticklabels(xTicks)
    ax1.axes.set_yticklabels(yTicks)
    ax1.axes.set_xticks(range(1, 2 ** numQubits + 1))
    ax1.axes.set_yticks(range(1, 2 ** numQubits + 1))
    ax1.axes.set_zticks(np.arange(-1, 1.1, .2))
    ax1.axes.set_zlim3d(-1, 1)
    plt.title("Rho Imaginary")
    fig.subplots_adjust(bottom=0.2)
    ax1 = fig.add_axes([0.2, 0.10, 0.7, 0.065])
    cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=colorMap,
                                    norm=norm,
                                    orientation='horizontal')
    plt.savefig(pathToDirectory + "/rhobarImag.png",bbox_inches = 'tight', pad_inches = 0)


"""
    matrixToHTML(M)
    Desc: Creates an HTML table based on the given matrix.

    Parameters
    ----------
    M : ndarray
        Matrix you would like to display on your html page.
    printEigenVals : boolean
        Specify if you want eigen values to be calculated and displayed at the bottom of the table.
    Returns
    -------
    res : string
        HTML code of the created table.
    """

def matrixToHTML(M,printEigenVals = False):
    s = np.shape(M)
    res = '<table style=\"border: 1px solid black;border-collapse: collapse;font-size: 15px; table-layout:fixed;width:100%;margin-top: 25px;\">'
    for i in range(s[0]):
        res = res+' <tr>'
        for j in range(s[1]):
            res = res + '<td style = "border: 1px solid black;">' + str(np.real(M[i,j])) + "<div style=\"color:rebeccapurple;font-weight: bold;display:inline;\">+</div><BR>"+ str(np.imag(M[i,j]))
            res = res + '<div style=\"color:rebeccapurple;font-weight: bold;display:inline;\">j</div></td>'
        res = res +'</tr>'
    res = res+'</table>'
    if(printEigenVals):
        d, v = np.linalg.eig(M)
        eigenVals = "<h5>Eigen Values: "
        for x in range(0,len(d)):
            eigenVals = eigenVals+str(round(d[x].real, 5))
            if(abs(d[x].imag)>.00001):
                eigenVals = eigenVals+"< div style =\"color:rebeccapurple;font-weight: bold;display:inline;\">+</div>"
                eigenVals = eigenVals+str(round(d[x].imag, 5))
                eigenVals = eigenVals+"<div style=\"color:rebeccapurple;font-weight: bold;display:inline;\">j</div>"
            eigenVals = eigenVals+" , "
        eigenVals = str(eigenVals)[0:len(str(eigenVals))-2]
        eigenVals = eigenVals+"</h5>"
        res = res+eigenVals
    return res
