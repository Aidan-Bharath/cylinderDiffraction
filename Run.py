# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 00:35:41 2015

This is an example run Script. 

@author: Aidan
"""

import meiDiffPolar as wf
import gridGeneration as gg
import gridPlot as gp



if __name__ == "__main__":
    
    tankR = 110
    cylR = 1
    k = 5
    A = 2
    w = 4
    t = 5
    n = 10
    
    r,o = gg.grid(tankR,resolution=100)
    
    wavefield = wf.waveField(k,r,o,cylR,A,w,t,n)
       
    gp.WFplot(r,o,wavefield[2])


