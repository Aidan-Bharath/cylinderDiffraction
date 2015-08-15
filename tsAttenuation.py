# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:13:27 2015

@author: aidan

To look specifically at timeseries attenuation with timestep setting.
"""

from __future__ import division
import pandas as pd
from os import path,chdir
import numpy as np
import re
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
import auxFunc as aux

def vectFloat(x):
    return float(x)

def loadSets(parDir):

    curDir = path.abspath('./')
    chdir(parDir)
    files = glob.glob('*')
    dic = {}    
    for paths in files:
        dataPath = path.join(parDir,paths)
        chdir(dataPath)
        dic[str(paths)] = pd.read_pickle(str(paths)+' reports.p')
        
    chdir(curDir)
    return dic
    
def minMax(dic,slices):
    mpl.rc('text', usetex=True)
    mpl.rc('axes', linewidth=2)
    mpl.rc('font', weight='bold')
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']

    df = {}
    for name,data in sorted(dic.iteritems()):
        sdata = data.loc[slices[0]:slices[1]].sort(axis=1)
        df[re.sub('ts','',name)] = (sdata.max()-sdata.min())/2
    df = pd.DataFrame(df)          
    
    df.plot(colormap='jet',label="0.{}".format(df.index))
    plt.title('Amplitudes Along the Direction of the Propagating Wave')
    plt.legend(title='Time Step',loc=3)
    plt.xlabel('Measurement Position From Inlet')
    plt.ylabel('Amplitude (m)')
    plt.grid()
    plt.show()
    
def courantComp(dic,slices,wl,A,h,x=0,y=0,z=0):
    Float = np.vectorize(vectFloat)
    
    mpl.rc('text', usetex=True)
    mpl.rc('axes', linewidth=2)
    mpl.rc('font', weight='bold')
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']

    df = {}
    for name,data in sorted(dic.iteritems()):
        sdata = data.loc[slices[0]:slices[1]].sort(axis=1)
        df[re.sub('ts','',name)] = (A-((sdata.max()-sdata.min())/2))/A
    df = pd.DataFrame(df)          
    t = Float('0.'+df.columns.values)
    Cfl = aux.courant(wl,t,A,h,x=x,y=y,z=z)
    print Cfl
    
    plt.figure()
    for name,rep in df.iterrows():
        plt.plot(Cfl,rep,label=name)
    plt.title(r'Wave Height Difference Over Various C_{FL} Numbers')
    plt.legend(title='Position',loc=4)
    plt.xlabel(r'C_{FL} Number')
    plt.ylabel(r'Normalized Difference')
    plt.grid()
    plt.show()
    
    
def pError(dic,slices,A):
    mpl.rc('text', usetex=True)
    mpl.rc('axes', linewidth=2)
    mpl.rc('font', weight='bold')
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']

    df = {}
    for name,data in sorted(dic.iteritems()):
        sdata = data.loc[slices[0]:slices[1]].sort(axis=1)
        df[re.sub('ts','',name)] = 100-((sdata.max()-sdata.min())/2)/A
    df = pd.DataFrame(df)          
    
    df.plot(colormap='jet',label="0.{}".format(df.index))
    plt.title('Amplitudes Along the Direction of the Propagating Wave')
    plt.legend(title='Time Step',loc=2)
    plt.xlabel('Measurement Position From Inlet')
    plt.ylabel('Amplitude (m)')
    plt.grid()
    plt.show()


if __name__ == "__main__":
    
    parDir = '/media/aidan/Seagate Expansion Drive/starCCM/cocTank/'
    dic = loadSets(parDir)
    wl = 5
    A = 0.01
    h = 0.5
    slices = [25,31]
    courantComp(dic,slices,wl,A,h,x=40,y=0,z=20)    
    #minMax(dic,slices)
    #pError(dic,slices,0.01)