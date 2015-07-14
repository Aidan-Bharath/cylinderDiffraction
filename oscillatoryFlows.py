# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:47:17 2015

@author: aidan
"""
import numpy as np
import matplotlib.pyplot as plt
import auxFunc as aux
import seaborn

def centValue(f):
    pass
    


def kcBPlot(f,B,r1):
    Kc = [aux.Kc(aux.A(f),r) for r in r1]
    B = [aux.B(f,r) for r in r1 ]
    plt.figure()
    for i in xrange(len(r1)):
        amp = aux.A_Kc(Kc[i],r1[i])
        plt.plot(B[i],Kc[i],label='Separation for '+str(r1[i])+' m')
    plt.legend()
    plt.grid(True)
    plt.xlabel('B (Frequency Parameter)')
    plt.ylabel('Kc (Amplitude Parameter)')    
    plt.title('2D Flow Separation for Various Radius Cylinders \n'
        +'Frequency Range '+str(f.min())+' < f < '+str(f.max())+' \n'
        +'Max Amplitude shown = '+str(amp.max())+' m')
    plt.show()
    

if __name__ == "__main__":
    
    r = [0.08,0.16]
    f = np.linspace(0.1,1.2,100)
    B = aux.B(f,r[0])
    
    print aux.A_Kc(1,r[0])
    
    
    kcBPlot(f,B,r)
    