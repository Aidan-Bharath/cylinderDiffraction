# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 00:58:48 2015

plot the resulting wavefield.

@author: Aidan
"""

import numpy as np
import matplotlib.pyplot as plt

__all__ = ['WFplot']

def WFplot(r,o,griddata):
    

    griddata[np.isnan(griddata)] = 0
    griddata[griddata>10],griddata[griddata<-10] = 0,0
   
    
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    ax.contourf(np.rad2deg(o),r, np.real(griddata))
    plt.show()
