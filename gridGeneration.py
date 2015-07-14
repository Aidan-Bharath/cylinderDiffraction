# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 00:18:59 2015

This script is ment to generate the radial domain used to calculate scattering
Fields around a single cylinder.

@author: Aidan
"""

import numpy as np
import auxFunc as aux

__all__ = ['grid']


def grid(r,cylR,resolution = 350):
    """
    Thsi just generates the meshgrid of points needed for Calculations
    """
    
    r = np.linspace(cylR,r,resolution)
    o = np.linspace(0,2*np.pi,resolution)
    rMatrix,oMatrix = np.meshgrid(r,o)

    return rMatrix,oMatrix
    
def multigrid(r,resolution = 250):
    """
    Thsi just generates the meshgrid of points needed for Calculations
    """
    
    r = np.linspace(0,r,resolution)
    o = np.linspace(0,2*np.pi,resolution)
    rMatrix,oMatrix = np.meshgrid(r,o)
    x,y = aux.polToCart(rMatrix,oMatrix)

    return [rMatrix,oMatrix,x,y]
    
    
