from itertools import izip_longest, imap
from struct import unpack, calcsize
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import random
from math import sqrt
import scipy.optimize as optimize

params_pattern = '=IBdddd' # (num_samples, sample_bytes, v_off, v_scale, h_off, h_scale, [samples]) ...
struct_size = calcsize(params_pattern)
print struct_size
C =0
z = 1
#with open("/unix/creamtea/scopeStuff/test2.ch3.traces","rb") as f:
#with open("/unix/creamtea/scopeStuff/test950V_5V_5p0ns_100mvDiv.ch3.traces","rb") as f:
with open("2_Mar_950_Trig_5_ch4ch310mV.ch4.traces","rb") as f:
    areaList = []
    totalareag = []
    peak =[]
    time =[]

    areaList2 = []
    totalareag2 = []
    peak2 =[]
    time2 =[]
    while True:
        header = f.read(struct_size)
        if not header: break
        sHeader = unpack(params_pattern,header)
        numSamples=sHeader[0]
        bytesPerSample=sHeader[1]
        v_off=sHeader[2]
        v_scale=sHeader[3]
        h_off=sHeader[4]
        h_scale=sHeader[5]
        dt=np.dtype('>i1')
    
        
        dataList=np.fromfile(f,dt,numSamples)
        sampList=np.arange(numSamples)
        voltList=np.multiply(dataList,v_scale)
        voltList=voltList
        
        shift =+np.mean(voltList[:300])
        
        voltList = (voltList - shift)
        timeList=np.multiply(sampList,h_scale)
        timeList+=h_off
        
        x = timeList
        y = voltList*0.02
        plt.plot(x, y,'b')
        area=np.trapz(x,y)
        areaList.append(area)
        countAbove=0
        firstAbove=0
        indices = []
        totalcharge=0
        for ind,volt in enumerate(y):
            if volt >0.00005:
                if countAbove == 0:
                    firstAbove=ind
                countAbove+=1
            else:
                if countAbove > 10:
                    indices.append((firstAbove,ind))
                countAbove=0

    # add b to a number an array as total charge add popt[1] to array as time o
        def gauss_function(x, a, x0, sigma):
            return a*np.exp(-(x-x0)**2/(2*sigma**2))

        for start,stop in indices:
            start = start-20
            stop = stop +20
        
            if stop <5002:
                mean = 0.5*(x[start]+x[stop])
                sigma = 1E-10
                popt, pcov = optimize.curve_fit(gauss_function, x[start:stop], y[start:stop], p0 = [1, mean, sigma],maxfev=1000000)
                plt.plot(x[start:stop], gauss_function(x[start:stop], *popt), label='Guassian Fit',color="red")
                #print popt
                A = (popt[:1]*(popt[2:3]))/0.3989
                    #print A
                if A < 0:
                    A =0
                if A>0.000000001:
                    A=0
                totalcharge = totalcharge + A
                time.append(popt[1:2])
                peak.append(A)
                popt[1:2]
    
        totalareag.append(totalcharge)

            #while z<1001:
            #[z] = totalcharge
#z = z+1


#print totalareag

k=np.count_nonzero(totalareag)
print 'non zero',k
l = sum(totalareag)
h = l/k
print h
m=np.count_nonzero(peak)
print m
avgpeak = np.mean(peak)
print avgpeak
#print (area-areaguass)
# plot data
avgtotal=np.mean(totalareag)
print 'mean',avgtotal
print 'std', np.std(totalareag)



   


mean= np.mean(areaList)
print 'trap'
print - mean


        
