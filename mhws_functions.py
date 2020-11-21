#!/usr/bin/python3

import netCDF4 as nc
import numpy as np
import numpy.ma as ma
import csv
from datetime import date
from marineHeatWaves import detect
import marineHeatWaves as mhw






def detect_input(file_name,local_lat,local_lon,box_size):
    '''
    Read the netCDF file and return the input vectors used for the detect funtion.

    Inputs:
    file_name   Name of the netCDF file. This should equal to the name of the site.
    local_lat   Index of the 'lat' (latitude) of the left top point of the box.
    local_lon   Index of the 'lont' (longitude) of the left top point of the box.
    box_size    The size of the square box, which equals to the square root of number of pixels in the box.

    Outputs:
    t           The time vector which is used as the input of the detect funtion. Values are from 1993-1-1 to 2019-12-31.
    temp        The sea surface temperature vector which is used as the input of the detect funtion.
    count_good  The number of good quality (quality_level >= 3) SSTs in the 'temp' list. 
    '''

    # read the nc file and create the data set
    ds = nc.Dataset(file_name+".nc")
    time=ds['time']
    ql=ds['quality_level']
    sses_bias=ds['sses_bias']
    #1981-1-1 is the start day defined in the detail of 'time' variable
    start_day=date(1981,1,1).toordinal()
    dtime = [start_day + ((tt-55200)/86400) for tt in time]

    count_good = 0 # count number of SSTs with quality level >= 3  

    #list of available times
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

    #this is the temperature array
    temp = []
    #creating time array t
    #this is the complete time series with all missing value filled
    t = []

    # 727564 is the time index for 1993-1-1 
    # 737424 is the time index for 2019-12-31
    Jan_1st_1993 = 727564
    Dec_31st_2019 = 737424
    i = Jan_1st_1993
    # dtime[255] is 1992-12-31 and dtime[256] is 1993-1-2
    j = 256
    while i <= Dec_31st_2019:
        t.append(date.fromordinal(i).toordinal())
        #if the data on a specific day is missing, fill it with 0
        if i == dtime[j]:
            j+=1
            index = dtime.index(i)
            t_temp = 0
            t_ntemp = 0
            # good temperature: sea surface temperature with quality level >= 3
            n_good_temp = 0 # number of good temperature
            sum_good_temp = 0 # sum of good temperature 
            for latitude in range(local_lat,local_lat+box_size):

                for longitude in range (local_lon,local_lon+box_size):
                    
                    if sses_bias[index,latitude,longitude] is ma.masked:
                        t_bias = 0
                    else:
                        t_bias = sses_bias[index,latitude,longitude]

                    tt = ds['sea_surface_temperature'][index,latitude,longitude].data.item(0)-t_bias
                    if tt != 0.0:
                        t_temp += tt
                        t_ntemp += 1
                    if ql[index,latitude,longitude] >= 3:
                        n_good_temp += 1
                        sum_good_temp += tt
            
            avg_temp = 0
            # if there is not good temperature in the box
            # use all the data
            if t_ntemp != 0 and n_good_temp == 0:
                avg_temp = (t_temp / t_ntemp) - 273.15 # change to degree Celsius
            # if there are good temperatures in the box
            # use good temperatures only
            elif n_good_temp > 0:
                count_good += 1
                avg_temp = (sum_good_temp / n_good_temp) - 273.15
            else:
                avg_temp = np.nan
            
            temp.append(avg_temp)
        else:
            temp.append(np.nan)    
        i+=1

    t = np.array(t)
    temp = np.array(temp)

    return t, temp, count_good

def detect_input_one_pixel(file_name,lat,lon):

    '''
    This function is used to detect marine heatwaves in one pixel.

    Inputs:
    file_name   Name of the netCDF file
    lat         Latitude index of the pixel.
    lon         Longitude index of the pixel.

    Outputs:
    t           The time vector used as input of the detect function.
    temp        The sea surface temperature vector used as input of the detect function.
    '''

    ds = nc.Dataset(file_name+".nc")
    time=ds['time']
    sses_bias=ds['sses_bias']

    #1981-1-1
    start_day=date(1981,1,1).toordinal()
    dtime = [start_day + ((tt-55200)/86400) for tt in time]

    temp = []
    t = []
    Jan_1st_1993 = 727564
    Dec_31st_2019 = 737424
    i = Jan_1st_1993
    # dtime[255] is 1992-12-31 and dtime[256] is 1993-1-2
    j = 256

    while i <= Dec_31st_2019:
        t.append(date.fromordinal(i).toordinal())
        #if the data on a specific day is missing, fill it with 0
        if i == dtime[j]:
            j+=1
            index = dtime.index(i)
            # use SST - sses_bias to get the de-biased SST
            if sses_bias[index,lat,lon] is ma.masked:
                t_bias = 0
            else:
                t_bias = sses_bias[index,lat,lon]
                        
            tt = ds['sea_surface_temperature'][index,lat,lon].data.item(0) - t_bias
            if tt != 0.0:
                tt = tt - 273.15
            else:
                tt = np.nan
            
            temp.append(tt)
        else:
            temp.append(np.nan)    
        i+=1

    t = np.array(t)
    temp = np.array(temp)

    return t,temp

def sst_counter(temp):
    '''
    Function used to count number of temperatures we have in a box.

    Input: 
    temp        The sea surface temperature vector in a box.

    Output:
    counter     Number of sea surface temperatures in 'temp' list.
    '''
    counter = 0
    for te in temp:
        if np.isnan(te) == False:
            counter+=1

    return counter       


def write_mhw_analyse_csv(mhws,file_name,location_type="onshore"):

    '''
    This function will create a csv file that contains some characteristics of marine heatwaves.

    Inputs:
    mhws        This is the output of detect funtion. 
                It contains all the characteristics of marine heatwaves in the box from 1993 to 2019.
    file_name   This is the name of the netCDF file.
    
    Options:
    location_type   This should be "onshore" or "offshore". It represents the location of the box.
                    The default value if "onshore".
    '''

    category = mhws['category']

    # change the intensity category into the corresponding intensity levels
    #1=strong, 2=moderate, 3=severe, 4=extreme
    intensity_level = []
    for ca in category:
        if ca == 'Strong':
            intensity_level.append(1)
        elif ca == 'Moderate':
            intensity_level.append(2)
        elif ca == 'Severe':
            intensity_level.append(3)
        elif ca == 'Extreme':
            intensity_level.append(4)
        else:
            intensity_level.append('ERROR')

    # variables(characteristics of Marine Heatwaves) in the csv file       
    start = [date.fromordinal(int(st)) for st in mhws['time_start']] # date format
    end = [date.fromordinal(int(st)) for st in mhws['time_end']]
    duration = mhws['duration']
    peak_time = [date.fromordinal(int(st)) for st in mhws['time_peak']]
    int_max = mhws['intensity_max']
    int_cum = mhws['intensity_cumulative']
    int_mean = mhws['intensity_mean']

    f = file_name+"_"+location_type
    with open(f+'_analys.csv','w',newline = '') as a_file:
        writer = csv.writer(a_file)
        writer.writerow(["index_number","time_start","time_end","duration","peak_time","max_intensity","mean_intensity","cumulative_intensity","intensity_level","intensity_category"])
        i = 0
        while i < len(start):
            writer.writerow([i+1,start[i],end[i],duration[i],peak_time[i],int_max[i],int_mean[i],int_cum[i],intensity_level[i],category[i]])
            i += 1


    mhwBlock = mhw.blockAverage(t, mhws)
    mhwBlock_3y = mhw.blockAverage(t, mhws,blockLength=3)
    mhwBlock_9y = mhw.blockAverage(t, mhws,blockLength=9)

def write_mhwBlock_csv(t,mhws,block_length,file_name,location_type="onshore"):

    '''
    This function creates a csv file that contains the characteristics of all marine heatwave in a time block.

    Inputs:
    t               The time vector.
    mhws            This is the output of detect funtion. 
                    It contains all the characteristics of marine heatwaves in the box from 1993 to 2019.
    block_length    The length of time blocks in year.
    file_name       The name of the netCDF file.

    Options:
    location_type   This should be "onshore" or "offshore". It represents the location of the box.
                    The default value is "onshore"
    '''

    mhwBlock = mhw.blockAverage(t, mhws,blockLength=block_length)
    # mhwBlock
    start_year = mhwBlock['years_start'] #          Start year blocks (inclusive)
    end_year = mhwBlock['years_end'] #              End year of blocks (inclusive)
    centre_year = mhwBlock['years_centre'] #        Decimal year at centre of blocks
    frequency = mhwBlock['count']#                  Total MHW count in each block
    duration = mhwBlock['duration']#                Average MHW duration in each block [days]
    max_intensity = mhwBlock['intensity_max']#      Average MHW "maximum (peak) intensity" in each block [deg. C]
    max_max_intensity = mhwBlock['intensity_max_max']#  Maximum MHW "maximum (peak) intensity" in each block [deg. C]
    mean_intensity = mhwBlock['intensity_mean']       #Average MHW "mean intensity" in each block [deg. C]
    intensity_var = mhwBlock['intensity_var']        #Average MHW "intensity variability" in each block [deg. C]
    cumulative_intensity = mhwBlock['intensity_cumulative'] #Average MHW "cumulative intensity" in each block [deg. C x days]
    rate_onset = mhwBlock['rate_onset']           #Average MHW onset rate in each block [deg. C / days]
    rate_decline = mhwBlock['rate_decline']         #Average MHW decline rate in each block [deg. C / days]
    mhw_days = mhwBlock['total_days']           #Total number of MHW days in each block [days]
    total_cumu_int = mhwBlock['total_icum']          # Total cumulative intensity over all MHWs in each block [deg. C x days]

    f = "average_"+block_length+"_year_"+file_name+"_"+location_type
    with open(f+'_analys.csv','w',newline = '') as a_file:
        writer = csv.writer(a_file)
        writer.writerow(["index_number","start_year","end_year","centre_year","frequency","duration","max_intensity","max_max_intensity","mean_intensity","intensity_variablity","cumulative_intensity","rate_onset","rate_decline","mhw_days","total_cumulative_intensity"])
        i = 0
        while i < len(start_year):
            writer.writerow([i+1,start_year[i],end_year[i],centre_year[i],frequency[i],duration[i],max_intensity[i],max_max_intensity[i],mean_intensity[i],intensity_var[i],cumulative_intensity[i],rate_onset[i],rate_decline[i],mhw_days[i],total_cumu_int[i]])
            i += 1
            
def number_of_sst_map(file_name):
    '''
    This function counts and prints the number of ssts at each 10 pixels in the file.
    This funtion is used to choose box.

    Input:
    file_name   The name of the netCDF file
    '''
    ds = nc.Dataset(file_name+".nc")
    lat = ds['lat'] 
    lon = ds['lon'] 
    sst = ds['sea_surface_temperature']
    ql = ds['quality_level']

    n_lat = lat.size
    n_lon = lon.size

    # 256 is the index of 1993-1-2 (since 1993-1-1 is missing) in the 'time' variable in data set
    # 9985 is the index of 2019-12-31 in the 'time' variable in data set
    print("Latitude | Longitude | Number of SSTs | Number of good SSTs")
    for la in range(0,n_lat,10):
        for lo in range(0,n_lon,10):
            x = sst[256:9985,la,lo]
            y = x[~x.mask]
            n_good = 0
            for tt in range(256,9986):
                if ql[tt,la,lo] >= 4:
                    n_good += 1
                    
            print(la,lo,y.size,n_good)

def count_gap(temp,start_date=date(1993,1,1),end_date=date(2019,12,31)):

    '''
    This function is used to show information about gaps in a time interval.

    Inputs: 
    temp        The full temperature vector, which is one of outputs of 'detect_input' function.
    start_date  The date of start of the time interval. 
                It should be in the date format and its value should be between 1993-1-1 and 2019-12-31.  
                e.g. "date(2000,1,1)" The default value is 1993,1,1
    end_date    The date of start of the time interval. 
                It should be in the date format and its value should be between 1993-1-1 and 2019-12-31, and it should be a date after the 'start_date'.  
                e.g. "date(2000,1,1)" The default value is 2019,12,31

    '''
    # generate the time list and date list
    t = np.arange(date(1993,1,1).toordinal(),date(2019,12,31).toordinal()+1)
    dates = [date.fromordinal(tt.astype(int)) for tt in t]

    start_index = dates.index(start_date)
    end_index = dates.index(end_date)

    # print the length of gaps
    gap_length = 0 # length of each gap
    n_missing = 0 # number of missing days
    n_gaps = 0 # number of gaps
    max_length = 0 # length of the largest gap
    n_small_gaps = 0 # number of gaps with length <= 2
    n_medium_gaps = 0 # number of gaps with length > 2 and <= 4
    n_large_gaps = 0 # number of gaps with length >= 5
    for i in range(start_index,end_index+1):
        if np.isnan(temp[i]) == True:
            gap_length+=1
        else:
            if gap_length != 0:
                if gap_length > max_length:
                    max_length = gap_length
                    
                if gap_length <= 2:
                    n_small_gaps+=1
                elif gap_length > 2 and gap_length <= 4:
                    n_medium_gaps+=1
                else:
                    n_large_gaps+=1
                    
                n_gaps += 1
                n_missing += gap_length
                #print(gap_length)
            gap_length = 0

    print("Thera are",n_missing,"days missing.")
    print("There are",n_gaps,"gaps.")
    print("The largest gap is",max_length,"days")
    print("There are",n_small_gaps,"with length 1 or 2 days.")
    print("There are",n_medium_gaps,"with length 3 or 4 days.")
    print("There are",n_large_gaps,"with length >= 5 days.")

'''
# the onshore box in Port Hacking Site
t1,temp1,n_good_ssts1 = detect_input("Port_Hacking",1,132,5)
n_ssts1 = sst_counter(temp1)
mhws1,clim1 = detect(t1,temp1, maxPadLength=4)
write_mhw_analyse_csv(mhws1,"Port_Hacking")
write_mhwBlock_csv(t1,mhws1,1,"Port_Hacking")
write_mhwBlock_csv(t1,mhws1,3,"Port_Hacking")
write_mhwBlock_csv(t1,mhws1,9,"Port_Hacking")


# the offshore box in Port Hacking Site
t2,temp2,n_good_ssts2 = detect_input("Port_Hacking",201,195,5)
n_ssts2 = sst_counter(temp2)
mhws2,clim2 = detect(t2,temp2, maxPadLength=4)
write_mhw_analyse_csv(mhws2,"Port_Hacking",location_type="offshore")
write_mhwBlock_csv(t2,mhws2,1,"Port_Hacking",location_type="offshore")
write_mhwBlock_csv(t2,mhws2,3,"Port_Hacking",location_type="offshore")
write_mhwBlock_csv(t2,mhws2,9,"Port_Hacking",location_type="offshore")

# the onshore box in Rottnest Island Site
t3,temp3,n_good_ssts3 = detect_input("Rottnest_Island",90,125,5)
n_ssts3 = sst_counter(temp3)
mhws3,clim3 = detect(t3,temp3, maxPadLength=4)
write_mhw_analyse_csv(mhws3,"Rottnest_Island")
write_mhwBlock_csv(t3,mhws3,1,"Rottnest_Island")
write_mhwBlock_csv(t3,mhws3,3,"Rottnest_Island")
write_mhwBlock_csv(t3,mhws3,9,"Rottnest_Island")

# the offshore box in Rottnest Island Site            
t4,temp4,n_good_ssts4 = detect_input("Rottnest_Island",0,25,5)
n_ssts4 = sst_counter(temp4)
mhws4,clim4 = detect(t4,temp4, maxPadLength=4)
write_mhw_analyse_csv(mhws4,"Rottnest_Island",location_type="offshore")
write_mhwBlock_csv(t4,mhws4,1,"Rottnest_Island",location_type="offshore")
write_mhwBlock_csv(t4,mhws4,3,"Rottnest_Island",location_type="offshore")
write_mhwBlock_csv(t4,mhws4,9,"Rottnest_Island",location_type="offshore")
'''