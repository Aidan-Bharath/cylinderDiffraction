# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 14:57:07 2015

@author: aidan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate as sint
import auxFunc as aux
import meiDiffPolar as ana
import phaseAvg as pa


def centShift(Dir,xs,ys):
    data = pd.read_pickle(Dir)    
    data['grid'][0,:,:] = data['grid'][0,:,:]+xs
    data['grid'][1,:,:] = data['grid'][1,:,:]+ys
    return data



def gridSlice(data,rx,ry,k,r,o,o_,a,A,h,start,tank,w=0,t=0,n=50,size=1000):
    wf = ana.waveField(k,r,o,o_,a,A,w,t,n)
        
    xint = np.linspace(rx[0],rx[1],size)
    yint = np.linspace(ry[0],ry[1],size)
    x,y = np.meshgrid(xint,yint)
    cylCut = np.argwhere(np.sqrt(x**2+y**2) <= a)
  
    
    wfGrid = sint.griddata(np.array([wf[6].flatten(),wf[7].flatten()]).T
        ,wf[0].flatten(),(x,y),method='linear',fill_value=0)
    wfGrid[cylCut[:,0],cylCut[:,1]] = np.nan
    
    ### fix this    
    pAmp = pa.surfacePhase(data,start,aux.WL(k),h,tank)
    pAGrid = sint.griddata(np.array([data['grid'][0,:,:].flatten()
        ,data['grid'][1,:,:].flatten()]).T,pAmp[1].flatten(),(x,y),method='linear'
        ,fill_value=0)
    pAGrid = pAGrid-h
    
    
    return [pAGrid,wfGrid,xint,yint,x,y]
    