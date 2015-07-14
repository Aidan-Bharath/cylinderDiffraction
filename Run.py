# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 12:42:46 2015

@author: aidan

A run file for the Diffraction patterns around a single cylinder

"""

import gridGeneration as gg
import meiDiffPolar as md
import gridPlot as gp
import auxFunc as aux


if __name__ == "__main__":
    
    wl = 10
    k = aux.K(wl)
    r = 25
    o_ = 0
    cylR = 2
    A = 0.01
    w = 0
    t = 0
    n = 15
    
    r, o = gg.grid(r,cylR)
    diff = md.waveField(k,r,o,o_,cylR,A,w,t,n)
    gp.WFplot(r,o,cylR,diff[0])

