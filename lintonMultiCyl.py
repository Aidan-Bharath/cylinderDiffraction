# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 06:45:39 2015

@author: Aidan

This Code is ment to solve for the scattering pattern of an arbitrary number 
of cylinders with arbitrary radius save that r < R (cylinders do not touch each 
other).

"""
from __future__ import division
import numpy as np
import scipy.special as spec
import gridGeneration as gg
import auxFunc as aux

def sumM(m):
    return np.arange(-m,m+1)

def Z(a,k,n):
    ka = k*a
    return (spec.jvp(n,ka,n=1)/spec.h1vp(n,ka,n=1))
    
def H(k,r,n):
    kr = k*r
    return spec.hankel1(n,kr)
    
def I(x,y,B,k):
    """
    I for all k
    
    """
    expon = k*(x*np.cos(B)+y*np.sin(B))
    return complex(expon,expon)
    
def solExp(m,B):
    return complex(np.cos((np.pi/2)-B),np.sin((np.pi/2)-B))**m


def radConv(cart):
    return np.array([aux.cartToPol(cyl[0],cyl[1]) for cyl in cart])



if __name__ == "__main__":
    
    Iv = np.vectorize(I)

    """
    need:
    k = incident wave number
    a_j = radius of jth cylinder
    x,y & r,o = polar and cylindrical coordinates
    B = incident angle of incident wave from +x
    
    """

    k,m = 10,sumM(5) # summing indicies
        
    rmax = 100
    wl = 4
    K = aux.K(wl)
    B = 0
    
    grid = gg.multigrid(rmax)
    cylR = [0.5,0.2]
    cylCart = np.array([[1,1],[2,-1]])
    cylRad = radConv(cylCart)
    print (-Iv(cylCart[0,:],cylCart[1,:],B,K)*solExp(m,B)[:,None]).flatten().shape