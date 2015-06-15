# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 00:58:48 2015

plot the resulting wavefield.

@author: Aidan
"""

import numpy as np
import matplotlib as cm
import matplotlib.pyplot as plt
import auxFunc as aux
import seaborn 

__all__ = ['WFplot']

def WFplot(r,o,cylR,griddata):
    
    x,y = aux.polToCart(r,o)
    levels = np.linspace(0.0015,0.018,50,endpoint=True)
       
    plt.figure()    
    plt.contourf(x,y, np.real(griddata),levels=levels)
    plt.title('Analytical Solution for Amplitudes')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    cbar = plt.colorbar()
    cbar.set_label('Amplitudes' ,rotation=270,labelpad=10)
     
    plt.show()
