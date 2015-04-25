# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 22:42:56 2015

Code reproduces the wave scattering pattern around vertical cylinders
which will be used for validation of CFD results.

This constitutes the 2D solution of scattering around a single cylinder, 
following Mei.

@author: Aidan
"""
from __future__ import division
import numpy as np
import scipy.special as spec

__all__ = ['waveField']


def eps(n):
    """
    Set the epsilon coef based on nth summign term
    """
    
    if n is 0:
        return 0
    else:
        return 2
        
        
def im(n):
    """
    calculate the imaginary coef
    """
    
    if n % 2 is 0:
        return -1
    else:
        return 1


def Bescoef(k,r,a,n):
    """
    The calculates the Bessel and Hankel function coef for the 
    incident and scattered wave solution.
    
    spec.jv(v,z) - Bessel Func of the first kind of order v
    spec.jvp(v,z) - first derivative of BF of the first kinda of order v
    spec.h1vp(v,z) - first derivative of Hankel Func of order v
    spec.hankel1(v,z) - Hankel func of the first kind of order v
    
    """
    
    kr , ka = k*r , k*a  
    coef = spec.jv(n,kr)-(spec.jvp(n,ka,n=1)/spec.h1vp(n,ka,n=1))*spec.hankel1(n,kr)
    
    return coef
    
    
def waveField(k,r,o,a,A,w,t,n):
    """
    Calculates the sum of both incident and scattering wave amplitudes for
    a given geometry and position in polar coord r.
    
    k - Wavenumber
    r - radius from center
    o - angle
    a - radius of cylinder
    A - incident wave amplitude
    w - angular frequency of incident wave
    t - time
    n - number of terms to include in the summation.
    
    """
    wave = [eps(i)*im(i)*Bescoef(k,r,a,i)*np.cos(i*o) for i in xrange(n)] 
    wave = np.sum(np.array(wave),axis=0)
    
    ki = A*wave
    ks = A*(complex(np.cos(w*t),np.sin(w*t)))*wave
    
    return (ki,ks,ki+ks)
    
    

if __name__ == "__main__":
    
    print waveField(4,2,3,1,2,2.5,4,10)
