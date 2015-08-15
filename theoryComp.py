# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:12:29 2015

@author: aidan

This is a starccm probe waveheight comparison to theory.
"""

from __future__ import division
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import re
from starLoad import loadPickle
import auxFunc as aux

def keySub(key):
    key = re.sub('Report: ','',key)
    key = re.sub('m \(m\)','',key)
    return int(key)
    
def meshNaming(key):
    key = re.sub('ittc','',key)[-5:]
    x, y = int(key[0:2]), int(key[-2:])  
    
    return [x,y]
    
def C(k,h):
    return 1/np.cosh(2*k*h)
    
def SOrderWave(k,A,w,h,x,t,p):
    o = np.tanh(k*h)
    O = k*x-w*t+p
    
    return A*(np.cos(O)+k*A*((3-o**2)/(4*o**3))*np.cos(2*O))
    
def THOrderWave(k,A,w,h,x,t,p):
    O = k*x-w*t+p 
    S = C(k,h)
    B_31 = -3*(1+3*S+3*S**2+2*S**3)/(8*(1-S)**3)
    return SOrderWave(k,A,w,h,x,t,p) + A**3*B_31*(np.cos(O)-np.cos(3*O))

def FROrderWave(k,A,w,h,x,t,p):
    O = k*x-w*t+p
    S = C(k,h)
    coth = 1/np.tanh(k*h)

    num_42 = (6-26*S-183*S**2-204*S**3-25*S**4+25*S**5)
    den_42 = (6*(3+2*S)*(1-S)**4)
    B_42 = coth*num_42/den_42

    num_44 = (24+92*S+122*S**2+66*S**3+67*S**4+34*S**5)
    den_44 = (24*(3+2*S)*(1-S)**4)
    B_44 = coth*num_44/den_44

    return THOrderWave(k,A,w,h,x,t,p) + A**4*(B_42*np.cos(2*O)+B_44*np.cos(4*O))

def FIFOrderWave(k,A,w,h,x,t,p):
    O = k*x-w*t+p
    S = C(k,h)
    

    num_53 = 9*(132+17*S-2216*S**2-5897*S**3-6292*S**4-2687*S**5+194*S**6+467*S**7+82*S**8)
    den_53 = (128*(3+2*S)*(4+S)*(1-S)**6)
    B_53 = num_53/den_53

    num_55 = 5*(300+1579*S+3176*S**2+2949*S**3+1188*S**4+675*S**5+1326*S**6+827*S**7+130*S**8)
    den_55 = (384*(3+2*S)*(4+S)*(1-S)**6)
    B_55 = num_55/den_55

    return FROrderWave(k,A,w,h,x,t,p) + A**5*(-(B_53+B_55)*np.cos(O)+B_53*np.cos(3*O)+B_55*np.cos(5*O))


def theoryComp(data,step,k,w,A,h,p,sh,plot=True,dicSlice=None):
    keys = np.vectorize(keySub)
    endDic = {} 
    means = {}
    
    for name,df in data.iteritems():
        keylist = keys(df.keys())
        df = df.loc[step[0]:step[1]]
        idx = df.index
              
        wave = np.array([A*np.sin(k*key+w*idx-sh)+h for key in keylist])
        SOWave = np.array([SOrderWave(k,A,w,h,key,idx,p)+h for key in keylist])
        THWave = np.array([THOrderWave(k,A,w,h,key,idx,p)+h for key in keylist])
        FRWave = np.array([FROrderWave(k,A,w,h,key,idx,p)+h for key in keylist])
        FIFWave = np.array([FIFOrderWave(k,A,w,h,key,idx,p)+h for key in keylist])
        waves = [wave,SOWave,THWave,FRWave,FIFWave]
        endDic[name] = pd.DataFrame(np.sqrt(((df.values-FIFWave.T)**2))
            ,columns=df.keys()).set_index(idx)
        means[name] = [(np.sqrt(((df.values-wave.T)**2)/2*A)).mean() 
            for wave in waves]
            
   
    if plot:
        
        endDic[dicSlice].loc[:,'Report: 5m (m)':'Report: 15m (m)'].plot()
         
        plt.xlabel('Time (s)')
        plt.ylabel('Squared Difference (m)')
        plt.title('Wave Height Error')
        plt.grid()
        plt.show()
              
    return endDic,means

def plot(data,position,cut,plots,A):
    
    
    mpl.rc('text', usetex=True)
    mpl.rc('axes', linewidth=2)
    mpl.rc('font', weight='bold')
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']
  
    test2 = []
    test3 = []
    for name,dat in sorted(data.iteritems()):
                
        xy = meshNaming(name)
        if name in plots[0]:
            mean = dat[position].mean()/(2*A)
            test2.append([xy[1],mean])
        
        elif name in plots[1]:
            mean = dat[position].mean()/(2*A)
            test3.append([xy[1],mean])
        
    test2 = np.array(test2)
    test3 = np.array(test3)
    
    plt.figure()
    plt.plot(test2[:,0],test2[:,1],linewidth=2
        ,label='Resolved Region 2 Times the Wave Height')
    plt.plot(test3[:,0],test3[:,1],linewidth=2
        ,label='Resolved Region 3 Times the Wave Height')    
    plt.title('Vertical Grid Resolution')
    plt.xlabel('Vertical Cells per Wave Wave Height')
    plt.ylabel('Percent Error')
    plt.legend()
    plt.grid()
    plt.show()

def rawPlot(data):
    
    mpl.rc('text', usetex=True)
    mpl.rc('axes', linewidth=2)
    mpl.rc('font', weight='bold')
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']
    
    plt.figure()
    data.plot()
    plt.title('Wave Height Time Series')    
    plt.xlabel('Time (s)')
    plt.ylabel('Water Elevation (m)')
    plt.show()
    
def forces(data,cut,k,A,h,cylR):
    """
    We must remember to non-dimensionalize this based on the 
    StarCCM+ reference values
    """
    rvel = 1
    rarea = 1
    rho = 999.97
    g = 9.81
    C = data.loc[cut::,:]#/(0.5*rho*rvel**2*rarea)
    
    ampF = np.sqrt((C**2).max())
    ampT = forceCoef(aux.dispR(2*np.pi/k,h),A,cylR)
   
    
    return ampF,ampT
    
def forceCoef(f,A,cylR):
    Kc = aux.Kc(A,cylR)
    B = aux.B(f,cylR)
    
    Cm = 2+4/np.sqrt(np.pi*B)+(np.pi*B)**(-3./2.)
    Cd1 = (3/2)*np.pi**3*(1/Kc)*(np.pi*B)**(-1./2.)
    Cd2 = (3/2)*np.pi**2*(1/Kc)*(B)**(-1.)
    Cd3 = -(3/8)*np.pi**3*(1/Kc)*(np.pi*B)**(-3./2.)
    Cd = Cd1+Cd2+Cd3
        
    return [Cm,Cd]
    
    

if __name__ == "__main__":
    
    Dir = '/media/aidan/Seagate Expansion Drive/starCCM/tank50mpFiles/'
    data = loadPickle(Dir)
    sh = -7*0.0194532925    
    p = (np.pi/2)+sh
    step = [15,25]
    wl = 5
    k = aux.K(wl)
    h = 1
    T = aux.T(wl,h)    
    w = 2*np.pi/T
    A = 0.01
    position = 'Report: 5m (m)'
    plots = [['2mesh40-05','2mesh40-10','2mesh40-20ittc','2mesh40-30'],
             ['3mesh40-05','3mesh40-10','3mesh40-20ittc','3mesh40-30']]
    cut =[0,8]
    a = theoryComp(data,step,k,w,A,h,p,sh,plot=True,dicSlice='2mesh40-30')
    
    #plot(a,position,cut,plots,A)    
    #rawPlot(data['3mesh40-20ittc'].loc[:,'Report: 5m (m)':'Report: 15m (m)'])
    

#    wl = 4
#    cylR = 1
#    Dir = '/media/aidan/Seagate Expansion Drive/starCCM/symtank/wl'+str(wl)+'/'
#    File = 'wl'+str(wl)+' reports.p'
#    data = pd.read_pickle(Dir+File)
#    #f = forceCoef(aux.dispR(30,0.5)/(np.pi*2),0.01,1)
#    print forces(data,15,aux.K(wl),0.015,0.5,1)
    #rawPlot(data)
    