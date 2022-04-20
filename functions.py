# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 09:48:29 2021

@author: CalinCalbureanu
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import xlrd
import statistics as st
import math
import fathon
from fathon import fathonUtils as fu
import pywt


  
def plotPupilsize(x,y):
    plt.plot(x,y)
    plt.xlabel("Video Time")
    plt.ylabel("Pupil size")
    plt.title('Pupil size')
    plt.show()

def ploteasyhard(x,y,a,b):
    figure, axis = plt.subplots(2)
    axis[0].scatter(x,y, s = 0.1)
    axis[0].set_title("Easy scenario")
    axis[0].set_ylabel("Pupil size")
    
    axis[1].scatter(a,b, s = 0.1)
    axis[1].set_title("Hard scenario")
    axis[1].set_ylabel("Pupil size")
    axis[1].set_xlabel("Timestamp")
    return figure


def modmax(d): 
    # compute signal modulus 
    m = [0.0]*len(d) 
    for i in range(len(d)): 
        m[i] = math.fabs(d[i])
    # if value is larger than both neighbours, and strictly # larger than either, then it is a local maximum 
    t = [0.0]*len(d) 
    for i in range(len(d)): 
        ll = m[i-1] if i >= 1 else m[i] 
        oo = m[i] 
        rr = m[i+1] if i < len(d)-2 else m[i] 
        if (ll <= oo and oo >= rr) and (ll < oo or oo > rr): 
            # compute magnitude 
            t[i] = math.sqrt(d[i]**2) 
        else: 
            t[i] = 0.0 
            
    return t

# Outputs a number between 1 ... 10
def ipa(d, times):
    # obtain 2-level DWT of pupil diameter signal d
    try:
        (cA2, cD2, cD1) = pywt.wavedec(d, "sym16", "per", level = 2)
    except ValueError:
        return
    
    # get signal duration (in seconds)
    tt = times[-1] - times[0]
    

    #normalize by 1/2^j, j = 2 for 2-level DWT
    cA2[:] = [x / math.sqrt(4.0) for x in cA2]
    cD1[:] = [x / math.sqrt(2.0) for x in cD1]
    cD2[:] = [x / math.sqrt(4.0) for x in cD2]

    # detect modulus maxima
    cD2m = modmax(cD2)
    
    # threshold using univeral threshold lambda = sigma * sqrt(2logn)
    # where sigma is the standard deviation of the noise
    lambduniv = np.std(cD2m) * math.sqrt(2.0 * np.log2(len(cD2)))
    cD2t = pywt.threshold(cD2m, lambduniv, mode = "hard")

    # compute IPA
    ctr = 0
    for i in range (len(cD2t)) :
        if math.fabs(cD2t[i]) > 0:
            ctr += 1
    
    IPA = float(ctr)/tt
    
    return IPA
    
