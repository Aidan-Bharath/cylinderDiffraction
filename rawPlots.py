# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:10:46 2015

@author: aidan
"""

import numpy as np
import pandas as pd
import matplotlib as cm
import matplotlib.pyplot as plt
import auxFunc as aux
import phaseAvg as pa
import gridGeneration as gg
import ampCompare as ac
import seaborn 


def rawPlot(dic,time,data):
    
    levels = np.linspace(0.485,0.515,100,endpoint=True)
    
    plt.figure()    
    plt.contourf(dic['grid'][0,1:,1:],dic['grid'][1,1:,1:],dic[time][data][1:,1:]
        ,levels=levels)
    plt.title('CFD Waveheights at '+str(time)+' s')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')    
    cbar = plt.colorbar()
    cbar.set_label('Total Water Depth (m)' ,rotation=270,labelpad=10)
    plt.show()

def pAmpPlot(data,st,wl,h,tank):

    grid = data['grid']
    pAmp = pa.surfacePhase(data,st,wl,h,tank)
    levels = np.linspace(0.5,0.51,100,endpoint=True)
    
    plt.figure()    
    #plt.contour(grid[0,1:,1:],grid[1,1:,1:],pAmp[1][1:,1:],colors='k'
    #    ,linewidth=0.1)
    plt.contourf(grid[0,1:,1:],grid[1,1:,1:],pAmp[1][1:,1:]
        ,levels=levels)
    plt.title('CFD Phase Averaged Amplitudes (m)')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    cbar = plt.colorbar()
    cbar.set_label('Amplitudes' ,rotation=270,labelpad=10)
    plt.show()
    
def RMSPlot(pA,wF,x,y):
        
    sd = wF-pA
    print sd[~np.isnan(sd)].min(),sd[~np.isnan(sd)].max()
    
    levels = np.linspace(sd[~np.isnan(sd)].min(),sd[~np.isnan(sd)].max()
        ,50,endpoint=True)
    wflevels = np.linspace(wF[~np.isnan(wF)].min(),wF[~np.isnan(wF)].max()
        ,15,endpoint=True)
        
    rms = np.sqrt(np.mean(~np.isnan(sd)))
    print rms
    
    plt.figure()
    cf = plt.contourf(x,y,sd,levels=levels)
    cfc = plt.colorbar(cf)
    cfc.set_label('Difference (m)' ,rotation=270,labelpad=10)
    cs = plt.contour(x,y,wF,cmap=plt.cm.jet,levels=wflevels,linewidths=1)
    plt.clabel(cs,fontsize=12,inline=1)
        
    plt.title('Analytical and CFD Amplitude Difference',fontsize=20)
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    
    plt.show()    
        
    
if __name__ == "__main__":
    
    Dir = '/home/aidan/starCCM/data/RInviscid/surfData.p'
    dic = pd.read_pickle(Dir)
   
    time = 22.5  
    pos = 'Position[Z] (m)'
    
    data = ac.centShift(Dir,-20,-20)    
    
   
    rx = [-15,15]
    ry = [-10,10]
    wl = 4
    k = aux.K(wl)
    tankR = 20
    cylR = 1
    r,o = gg.grid(tankR,cylR,resolution=250)
    o_ = 0    
    A = 0.01    
    start = 14
    wl = 4
    h = 0.5
    tank = [19,19]    
    pAmpPlot(dic,start,wl,h,tank)
        
    #gData = ac.gridSlice(data,rx,ry,k,r,o,o_,cylR,A,h,start,tank)
    
    #RMSPlot(gData[0],gData[1],gData[2],gData[3])