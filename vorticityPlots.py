# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 12:27:28 2015

@author: aidan
 - Surface vorticity field plots and anaylsis

"""
from __future__ import division
import numpy as np
import pandas as pd
import scipy.interpolate as sint
import matplotlib.pyplot as plt
import matplotlib as mpl

def rmCyl(x,y,cylP,r):
    return np.argwhere((np.sqrt((x-cylP[0])**2+(y-cylP[1])**2)<r))

def loadSingle(File,cylP,r):
    
    size = 1100

    direct = ['x','y','z']    
    data = pd.read_csv(File)
    points = np.array([data['X (m)'].values,data['Y (m)'].values]).T
    x,y = np.linspace(10,35,size), np.linspace(0,10,size)
    xi,yi = np.meshgrid(x,y)
    idx = rmCyl(xi,yi,cylP,r)
    
    
    vort = {}
    for i,j in enumerate(direct):
        
        temp = sint.griddata(points,data.loc[:,data.keys()[i]],(xi,yi),
            method='linear', fill_value=0)
        for k in xrange(len(idx[:,0])):
            temp[int(idx[k,0]), int(idx[k,1])] = np.nan
        vort[j] = temp
        
    return [vort,xi,yi]
    
def Plot(data):
    mpl.rc('text', usetex=True)
    mpl.rc('axes', linewidth=2)
    mpl.rc('font', weight='bold')
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']
   
    levels = np.linspace(-0.15,0.2,100,endpoint=True)

    pltdata = data[0]['y']
    pltdata[pltdata>=levels.max()] = levels.max()
    pltdata[pltdata<=levels.min()] = levels.min()
    
    plt.figure()    
    plt.contourf(data[1],data[2],pltdata,cmap=plt.cm.RdBu)#,levels=levels)
    plt.title('CFD Surface Vorticity Z-Component')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')    
    cbar = plt.colorbar()
    cbar.set_label('Vorticity (s^{-1})' ,rotation=270,labelpad=15)
    plt.show()

def loadDict(File,time,cylP,r):

        
    if type(File) is type({}):
        data = File
    else:
        data = pd.read_pickle(File)
   
    xi,yi = data['grid'][0,:,:],data['grid'][1,:,:]
    idx = rmCyl(xi,yi,cylP,r)
        
    direct = ['x','y','z']
    vort = {}
    for i,j in enumerate(direct):
       
        temp = data[time][data[time].keys()[i]]
        for k in xrange(len(idx[:,0])):
            temp[int(idx[k,0]), int(idx[k,1])] = np.nan
        vort[j] = temp
        
    return [vort,xi,yi]
    


if __name__ == "__main__":
    
    Dir = '/media/aidan/Seagate Expansion Drive/starCCM/channelData/amp10cm/t2/'
    File = 'surfData.p'
    cylP = [30,1.75]
    r = 0.1575
    
    #data = loadSingle(Dir,cylP,r)
    #d = pd.read_pickle(Dir+File)
    data = loadDict(d,39.5,cylP,r)
        
    
    Plot(data)






