# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 13:15:19 2015

@author: aidan
"""
#import pyximport; pyximport.install()

import meiCythonCyl2 as mcc
import time
import gridGeneration as gg



tankR = 50.0
cylR = 1.0
res = 10000

t0 = time.time()
gg.grid(tankR,cylR,resolution=res)
t1 = time.time()

print t1-t0

t0 = time.time()
mcc.singleCyl(tankR,cylR,res=res)
t1 = time.time()

print t1-t0
