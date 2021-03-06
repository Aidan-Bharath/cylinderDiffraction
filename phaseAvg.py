# -*- coding: utf-8 -*-
"""
Created on Fri May 15 13:19:59 2015

@author: aidan
"""
from __future__ import division
import numpy as np
import pandas as pd
import auxFunc as aux


def seriesPhase(File,start,wl,d,nphases):
    T = aux.T(wl,d)
    nphases = np.linspace(0,nphases,nphases)
    stops = np.array(start+(T*nphases))
    
    data = pd.read_pickle(File).loc[start:stops[-1],:]
    pAvg = {}    
    for idx,key in data.iteritems():
        phases = [key.loc[stops[i]:stops[i+1]].values for i in xrange(len(stops)-1)]        
        means = pd.DataFrame([phase for phase in phases]).mean().T    
        pAvg[idx] = means
        
    return pd.DataFrame(pAvg)


def reflectCalc(Dict,wl,d,wallDist,start,T):
    ### phase or group velocity    
    '''
    This is set to have at least two periods at the farthest point
    from the radiating source
    '''
    
    #cg = aux.cg(wl,d)
    cp = aux.cp(wl,d)
    inlet = wallDist[0]
    refl = wallDist[1]
    maxDist = inlet - 4*cp
    stop = (inlet + 4*refl-maxDist)/cp
    stop = start+T*np.floor((stop-start)/T)
    print stop
    
    ### temporary due to files    
    

    return maxDist,stop
        

def surfacePhase(data,start,wl,d,wallDist):
    """
    This is geared only for surface elevation.... Damn
    """

    T = aux.T(wl,d)    
    sets = 1
    
    mag,stop = reflectCalc(data,wl,d,wallDist,start,T) 
    
    numT = int(np.floor((stop-start)/T))
    ranges = [[start+T*(i),start+T*(i+1)] for i in xrange(numT)]
    
    phased = {}
    for i in xrange(len(ranges)):
        phased[i] = {key:data for key,data in data.iteritems() if key <= ranges[i][1] and key >= ranges[i][0]}    
  
    pAvg = np.zeros(phased.values()[0].values()[0].values()[0].shape)
    
      
    for times in xrange(len(phased.values()[0].keys())):
        build = np.zeros(phased.values()[0].values()[0].values()[0].shape)
        
        for keys,data in phased.iteritems():
                       
            try:
                build = np.dstack((build,data[sorted(data.keys())[times]].values()[sets]))
            except IndexError:
                pass
     
        build = np.mean(np.delete(build,[0,0,0],axis=2),axis=2)
        
        pAvg = np.dstack((pAvg,build))
   
    pAvg = np.delete(pAvg,[0,0,0],axis=2)
    pAmp = pAvg.max(axis=2)
        
    
    return [pAvg,pAmp,mag]

def surfPhase(data,x,y,wl,A,h):
    ### Test Set up
    x = np.linspace(0,39,100)
    #y = np.linspace(0,39,100)
    #x,y = np.meshgrid(x,y)
    k = aux.K(wl)
    T = aux.T(wl,h)
    t = np.linspace(0,T,100)    
    wave = A*np.sin(k*x+(2*np.pi/T)*t)
    print wave
    
    
    
    
    return wave
    
    
    
if __name__ == "__main__":
    
    Dir = '/media/aidan/Seagate Expansion Drive/starCCM/channelData/amp10cm/t2/'
    File = 'surfData.p'
    
    #data = seriesPhase(Dir+File,3,4,0.5,5)
    data = surfacePhase(Dir,File,10,4,1.5,[19,29])
    #wave = surfPhase(2,1,1,4,0.01,0.5)
    