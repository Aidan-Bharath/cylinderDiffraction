# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 00:58:48 2015

plot the resulting wavefield.

@author: Aidan
"""

import numpy as np
import matplotlib.pyplot as plt
import auxFunc as aux

__all__ = ['WFplot']

def WFplot(r,o,cylR,griddata):
    
    x,y = aux.polToCart(r,o)
    cut = np.argwhere([np.sqrt(x**2+y**2) <= cylR])
    print x.shape,y.shape    
    print cut.shape
    
    fig = plt.figure()    
    plt.contourf(x,y, np.real(griddata))
    plt.colorbar()
    #plt.show()
