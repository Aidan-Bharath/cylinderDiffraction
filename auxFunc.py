# -*- coding: utf-8 -*-
"""
Created on Tue May  5 16:55:57 2015

@author: aidan
"""
from __future__ import division
import numpy as np

__all__ = ['T','K']


def T(wl,h):
    return wl/np.sqrt(9.81*K(wl)*np.tanh(K(wl)*h))
    
def K(wl):
    return 2*np.pi/wl
    
    
    

    
    