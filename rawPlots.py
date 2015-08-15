# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:10:46 2015

@author: aidan
"""

from __future__ import division
from os import path,chdir
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import auxFunc as aux
import phaseAvg as pa
import gridGeneration as gg
import ampCompare as ac



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

def rmCyl(grid,cylP,r):
    gx = grid[0,:,:]
    gy = grid[1,:,:]
    idx = np.argwhere((np.sqrt((gx-cylP[0])**2+(gy-cylP[1])**2)<r))
        #(np.sqrt(gx**2+gy**2)>=cylP[0]-r))
    
    return idx                      
                      
def pAmpPlot(data,st,wl,h,A,tank):
    mpl.rc('text', usetex=True)
    mpl.rc('axes', linewidth=2)
    mpl.rc('font', weight='bold')
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']
   
    grid = data['grid']
    pAmp = pa.surfacePhase(data,st,wl,h,tank)
    idx = rmCyl(grid,[20,0],1)
    for i in xrange(len(idx[:,0])):
        pAmp[1][int(idx[i,0]), int(idx[i,1])] = np.nan
    levels = np.linspace(0,1.8,100,endpoint=True)
    
   
    plt.figure()    
    #plt.contour(grid[0,1:,1:],grid[1,1:,1:],pAmp[1][1:,1:],colors='k'
    #    ,linewidth=0.1)
    plt.contourf(grid[0,1:,1:],grid[1,1:,1:],(pAmp[1][1:,1:]-h)/A
        ,levels=levels,cmap=plt.cm.jet)
    plt.title('CFD Phase Averaged Amplitudes')
    plt.xlabel('X (m)')
    plt.xlim(0,40)
    plt.ylabel('Y (m)')
    plt.ylim(0,15)
    cbar = plt.colorbar()
    cbar.set_label('Relative Amplitudes' ,rotation=270,labelpad=10)
    plt.show()
    
def pAmpVPlot(data,st,wl,h,A,tank):
    mpl.rc('text', usetex=True)
    mpl.rc('axes', linewidth=2)
    mpl.rc('font', weight='bold')
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']
   
    grid = data['grid']
    pAmp = pa.surfacePhase(data,st,wl,h,tank)
    pAmpM = pAmp[0].mean(axis=2)/pAmp[1].max()
    idx = rmCyl(grid,[20,0],1)
#    levels = np.linspace(0,70,100,endpoint=True)
#    pAmp[1][pAmp[1]>=levels.max()] = levels.max()
    for i in xrange(len(idx[:,0])):
        pAmp[1][int(idx[i,0]), int(idx[i,1])] = np.nan
   
    
   
    plt.figure()    
    #plt.contour(grid[0,1:,1:],grid[1,1:,1:],pAmp[1][1:,1:],colors='k'
    #    ,linewidth=0.1)
    plt.contourf(grid[0,1:,1:],grid[1,1:,1:],pAmp[1][1:,1:]
        ,levels=levels,cmap=plt.cm.jet)
    plt.title('CFD Phase Averaged Vorticity Magintudes')
    plt.xlabel('X (m)')
    plt.xlim(0,40)
    plt.ylabel('Y (m)')
    plt.ylim(0,15)
    cbar = plt.colorbar()
    cbar.set_label(r'Vorticity Magnitude ((s^{-1})' ,rotation=270,labelpad=10)
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

def tsSurface(dic,pos,place):
    
    
    idx = np.abs(dic['grid'][0,0,:]-place[0]).argmin()
    idy = np.abs(dic['grid'][1,:,0]-place[1]).argmin()
       
    keys = sorted(dic.keys())
    plotArray = np.zeros([(len(dic.keys())-1),2])
    
    for i in xrange(plotArray.shape[0]):
        plotArray[i,0] = keys[i]
        plotArray[i,1] = dic[keys[i]][pos][idx,idy]
        
    plt.figure()
    plt.plot(plotArray[:,0],plotArray[:,1])
    plt.show()
        
    return 
    
def CflPlot(wl,A,t,x,z,h):
    
    mpl.rc('text', usetex=True)
    mpl.rc('axes', linewidth=2)
    mpl.rc('font', weight='bold')
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']
       
    levels = np.linspace(0,0.06,100,endpoint=True)
    w = aux.dispR(wl,h)
    x = np.linspace(x[0],x[1],100)
    z = np.linspace(z[0],z[1],100)
    x, z = np.meshgrid(x,z)
    
    cfl = (w*t/2)*(k*x*A/np.pi+z)
    
   
    
    plt.figure()    
    plt.contour(x,z,cfl,colors='k',linewidth=0.1)
    plt.contourf(x,z,cfl,levels=levels,cmap=plt.cm.jet)
    plt.title('C_{FL} Numbers')
    plt.xlabel('X Cells')
    
    plt.ylabel('Z Cells')
    
    cbar = plt.colorbar()
    cbar.set_label('C_{FL} Number' ,rotation=270,labelpad=10)
    plt.show()
   
       
if __name__ == "__main__":
#    
    Dir = '/media/aidan/Seagate Expansion Drive/starCCM/symtank/wl6/'
    files = 'surfData.p'
    dic = pd.read_pickle(Dir+files)
    print 'done load'
    
   
    #time = sorted(dic.keys())[-100]
    #pos = 'Position[Z] (m)'
    #b = tsSurface(dic,pos,[15,1])
    #rawPlot(dic,time,pos)
    #data = ac.centShift(Dir,-20,-20)    
    
   
    rx = [-15,15]
    ry = [-10,10]
    wl = 6
    k = aux.K(wl)
    tankR = 20
    cylR = 1
    r,o = gg.grid(tankR,cylR,resolution=250)
    o_ = 0    
    A = 0.01    
    start = 20
    h = 0.5
    tank = [19,29]    
    pAmpVPlot(dic,start,wl,h,A,tank)
    #CflPlot(wl,A,0.001,[10,70],[5,40],h)   
    #gData = ac.gridSlice(data,rx,ry,k,r,o,o_,cylR,A,h,start,tank)
    
    #RMSPlot(gData[0],gData[1],gData[2],gData[3])