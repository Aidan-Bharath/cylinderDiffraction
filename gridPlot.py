# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 00:58:48 2015

plot the resulting wavefield.

@author: Aidan
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import auxFunc as aux
#import seaborn 

__all__ = ['WFplot']

def WFplot(r,o,cylR,griddata):
    
    
    x,y = aux.polToCart(r,o)
    levels = np.linspace(0.0015,0.018,60,endpoint=True)
    
    mpl.rc('text', usetex=True)
    mpl.rc('axes', linewidth=2)
    mpl.rc('font', weight='bold')

    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']
    
    plt.figure()    
    
    plt.contourf(x,y, np.real(griddata),levels=levels,cmap=plt.cm.jet)
    plt.title('Amplitudes')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    cbar = plt.colorbar()
    cbar.set_label('Amplitudes (m)' ,rotation=270,labelpad=18)
    plt.grid()
    plt.show()
