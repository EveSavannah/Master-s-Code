from itertools import izip_longest, imap
from struct import unpack, calcsize
import numpy as np
import matplotlib.pyplot as plt
import time
from mpl_toolkits import mplot3d
import matplotlib.patches as mpatches

params_pattern = '=IBdddd' # (num_samples, sample_bytes, v_off, v_scale, h_off, h_scale, [samples]) ...
struct_size = calcsize(params_pattern)
print struct_size

#with open("/unix/creamtea/scopeStuff/test2.ch3.traces","rb") as f:
with open("1_Mar_950_Trig_ch3_both_6.0mV.ch4.traces","rb") as f, open("1_Mar_950_Trig_ch4ind_6mV.ch4.traces","rb") as f2:
    areaList = []
    areaList2 = []
   
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
        # area=np.trapz(voltList,timeList)
        area1=np.trapz(voltList[:650],timeList[:650])
        area=np.trapz(voltList[650:1300],timeList[650:1300])
#        area=np.trapz(voltList,timeList)
        areaList.append(area-area1)  #area-area1

        header2 = f2.read(struct_size)
        if not header2: break 
        sHeader2 = unpack(params_pattern,header2)
        numSamples2=sHeader2[0]
        bytesPerSample2=sHeader2[1]
        v_off2=sHeader2[2]
        v_scale2=sHeader2[3]
        h_off2=sHeader2[4]
        h_scale2=sHeader2[5]
        dt2=np.dtype('>i1')

        
        dataList2=np.fromfile(f2,dt2,numSamples2)
        sampList2=np.arange(numSamples2)
        voltList2=np.multiply(dataList2,v_scale2)
        timeList2=np.multiply(sampList2,h_scale2)        
        timeList2+=h_off2
        area7=np.trapz(voltList2[:650],timeList2[:650])
        area4=np.trapz(voltList2[650:1300],timeList2[650:1300])
        area2=np.trapz(voltList2,timeList2)
        areaList2.append(area4-area7)  #area-area1
    


#    print areaList
    # areaMean=np.mean(areaList)
    # areaStd=np.std(areaList)
    # print areaMean,areaStd
    # print (areaMean/areaStd)*(areaMean/areaStd)

    # the histogram of the data
    n, bins, patches = plt.hist(areaList, 50, normed=0, facecolor='b', alpha=0.6,label='Both Channels')
    n2, bins2, patches2 = plt.hist(areaList2, 50, normed=0, facecolor='r', alpha=0.8,label='Channel 4')

     # colors = ('b','b','b')
     # area = np.pi*3
    # print len(areaList),len(areaList2)
     # for value,value2  in zip(areaList,areaList2):
         # print value,value2
    

#plt.scatter(areaList,areaList2,c=colors)#,s=area,c=colors,alpha=0.5)
#plt.ylim(-0.5e-9,2e-9)
#plt.xlim(-0.5e-9,2e-9)
    plt.title('Histogram of Charge at 6mV with just channel 4 tiggering and both ')
    plt.xlabel('Total Charge/C')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.show()


