from itertools import izip_longest, imap
from struct import unpack, calcsize
import numpy as np
import matplotlib.pyplot as plt
import time

params_pattern = '=IBdddd' # (num_samples, sample_bytes, v_off, v_scale, h_off, h_scale, [samples]) ...
struct_size = calcsize(params_pattern)
print struct_size

#with open("/unix/creamtea/scopeStuff/test2.ch3.traces","rb") as f:
with open("scopeStuff/1_Mar_950_Trig_ch4_both_2.0mV.ch4.traces","rb") as f:
    areaList = []
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
        timeList=np.multiply(sampList,h_scale)        
        timeList+=h_off
        area1=np.trapz(voltList[:650],timeList[:650])
        area=np.trapz(voltList[650:1300],timeList[650:1300])
        print area,area1,len(voltList)
        areaList.append(area)

        plt.clf()
        print np.mean(voltList)
        plt.plot(timeList,voltList)
        plt.xlabel('Time')
        plt.ylabel('Voltage')
        plt.pause(0.01)



        
