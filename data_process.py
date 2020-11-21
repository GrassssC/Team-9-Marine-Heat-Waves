#!/usr/bin/python3

import netCDF4 as nc
import numpy as np
from datetime import date
from datetime import datetime 
import numpy.ma as ma
from marineHeatWaves import detect
import csv
f = 'Port_Hacking_site'
fn = f+'.nc'
ds = nc.Dataset(fn)
time=ds['time']
ql=ds['quality_level']
sses_bias=ds['sses_bias']
#1981-1-1
start_day=date(1981,1,1).toordinal()
dtime = [start_day + ((tt-55200)/86400) for tt in time]


#list of availablke times
#this is the processed raw data where missing time is not filled.
dates = [date.fromordinal(tt.astype(int)) for tt in dtime]


#for refference only, we arbitarrily take 1 point:
la = ds['lat']
lat = []
for i in la:
    lat.append(i.data.item(0))
lo = ds['lon']
lon = []
for i in lo:
    lon.append(i.data.item(0))


#this is the tempreture array
temp = []
temp_sd = []
diff_arr = []
#creating time array t
#this is the comnplete timne series with all missing value filled
t = []
j = 0
start=dtime[0]
i = start
end = dtime[9987]
while i < end:
    t.append(date.fromordinal((i).astype(int)))
    #if the data on a specific day is misisng, fill it wilth 0
    if i == dtime[j]:
        print(i)
        j+=1
        index = dtime.index(i)
        t_list = [] 
        t_good_list = []
        n_good_temp = 0 # number of good temperature
        sum_good_temp = 0 # sum of good temperature 
        for latitude in range(3,4):
            for longitude in range (133,134):
                            # use SST - sses_bias to get the de-biased SST
                if sses_bias[index,latitude,longitude] is ma.masked:
                    t_bias = 0
                else:
                    t_bias = sses_bias[index,latitude,longitude]
                tt = ds['sea_surface_temperature'][index,latitude,longitude].data.item(0) - t_bias
                if tt != 0.0:
                    t_list.append(tt)
                if ql[index,latitude,longitude] >= 3:
                    n_good_temp += 1
                    t_good_list.append(tt)
        avg_temp = 0
        t_ntemp = len(t_list)
        if t_ntemp != 0 and n_good_temp == 0:
            avg_temp = (np.sum(t_list) / t_ntemp) - 273.16
            sd = np.std(t_list)
            diff = max(t_list) - min(t_list)
        elif n_good_temp > 0:
            avg_temp = (np.sum(t_good_list) / n_good_temp)- 273.16
            sd = np.std(t_good_list)
            diff = max(t_good_list) - min(t_good_list)
        else:
            avg_temp = np.nan
            sd = np.nan
            diff = np.nan
        temp.append(avg_temp)
        temp_sd.append(sd)
        diff_arr.append(diff)
    else:
        temp.append(np.nan)    
        temp_sd.append(np.nan)
        diff_arr.append(np.nan)
    i+=1


with open(f+'_time_aganst_temp_and_sd_onshore_1.csv','w',newline = '') as a_file:
    writer = csv.writer(a_file) 
    writer.writerow(["index","time","temp","temp_sd","difference"])
    i = 0
    while i < len(temp_sd):
        if (not np.isnan(temp[i])) and (i > 285) :
            writer.writerow([i+1,t[i],temp[i],temp_sd[i],diff_arr[i]])
        i += 1

t =  [st.toordinal() for st in t]
t = np.array(t)
temp = np.array(temp)
mhws = detect(t,temp,climatologyPeriod=[1992,2020], maxPadLength=4)


start = [date.fromordinal(int(st)) for st in mhws[0]['time_start']]
end = [date.fromordinal(int(st)) for st in mhws[0]['time_end']]
duration = mhws[0]['duration']
peak_time = [date.fromordinal(int(st)) for st in mhws[0]['time_peak']]
int_max = mhws[0]['intensity_max']
int_cum = mhws[0]['intensity_cumulative']
int_mean = mhws[0]['intensity_mean']

with open(f+'_analys_onshore_1.csv','w',newline = '') as a_file:
    writer = csv.writer(a_file)
    
    writer.writerow(["index_number","time_start","time_end","duration","peak_time","max_intensity","mean_intensity","cumulative_intensity"])
    i = 0
    while i < len(start):
        if start[i] > date(1992,12,31):
            writer.writerow([i+1,start[i],end[i],duration[i],peak_time[i],int_max[i],int_mean[i],int_cum[i]])
        i += 1
