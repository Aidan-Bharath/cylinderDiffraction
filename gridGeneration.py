# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 00:18:59 2015

This script is ment to generate the radial domain used to calculate scattering
Fields around a single cylinder.

@author: Aidan
"""

import numpy as np

__all__ = ['grid']


def grid(r,resolution = 100):
    """
    Thsi just generates the meshgrid of points needed for Calculations
    """
    
    r = np.linspace(0,r,resolution)
    o = np.linspace(0,2*np.pi,resolution)
    rMatrix,oMatrix = np.meshgrid(r,o)

    return rMatrix,oMatrix
    
    
