# -*- coding: utf-8 -*-
"""
Created on Sat Apr 04 03:17:15 2015

@author: Aidan
"""
from __future__ import division
import numpy as np
import re
import matplotlib.pyplot as plt

__all__ = ['Wave','rmP','dicSeriesPlot','dicDFSlice','T','K']

def _k(l):
    return (2*np.pi)/l[0]

def _omega(l):
    return (2*np.pi)/l[2]

def _O(l):
    return _k(l)*l[3]-_omega(l)*l[4]

def Wave(l):
    return l[1]*np.cos(_O(l))+l[5]
    
def rmP(name):
    return re.sub('.p','',name)
    
def dicSeriesPlot(dic,leg=True):
    for i,j in dic.iteritems():
        plot = j.plot(label=i)
    if leg:
        plt.legend()
            
    return plot
    
def dicDFSlice(dic,time):
    for name,data in dic.iteritems():
        dic[name] = data.loc[:time,:]
        
    return dic
    
def pVel(wl,h):
    return np.sqrt(9.81*K(wl)*np.tanh(K(wl)*h))
    
def T(wl,h):
    return (2*np.pi)/pVel(wl,h)
    
def K(wl):
    return 2*np.pi/wl

def WL(k):
    return 2*np.pi/k
    
def cg(wl,h):
    th = np.tanh(K(wl)*h)
    return (wl/(2*T(wl,h)))*(1+K(wl)*h*((1-th**2)/th))
    
def cp(wl,h):
    return np.sqrt((9.81/K(wl))*np.tanh(K(wl)*h))
    
def polToCart(r,o):
    return r*np.cos(o),r*np.sin(o)

def cartToPol(x,y):
    ## Watch this returns negative values below x axis
    return [np.sqrt(x**2+y**2),np.arctan(y/x)]
    
def f(wl,h):
    return 1/T(wl,h)
    
def f_B(B,R,h):
    """
    Runs off of the shallow water approx for wavelength
    """
    v = 1.002*10**(-3)
    rho = 999.97
    f = (B*v)/(4*R**2*rho)
    return np.sqrt(9.81*h)/f
    
def A_Kc(Kc,R):
    return (Kc*R)/np.pi
    
def d(f):
    v = 1.002*10**(-3)
    rho = 999.97
    return np.sqrt((v)/(np.pi*f*rho))
    
def A(f):
    return 7*d(f)    
    
def Kc(A,R):
    return np.pi*(A/R)

def B(f,R):
    return (4/np.pi)*(R/d(f))**2
    
    

if __name__ == "__main__":
    
    print f_B(60,1,0.5)
    print A_Kc(0.05,1)