# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 00:35:41 2015

This is an example run Script. 

@author: Aidan
"""

import meiDiffPolar as wf
import gridGeneration as gg
import gridPlot as gp
import auxFunc as aux




if __name__ == "__main__":
    
    tankR = 20
    cylR = 1
    wl = 4
    k = aux.K(wl)
    A = 0.01
    w = 4
    t = 5
    n = 50
    o_ = 0
    
    ### Watch Resolution
    r,o = gg.grid(tankR,cylR,resolution=250)
     
    wavefield = wf.waveField(k,r,o,o_,cylR,A,w,t,n)
     
  
    gp.WFplot(r,o,cylR,wavefield[0])
    
    print aux.f(wl,0.5)
    
