import math
from scipy.stats import genpareto
import matplotlib.pyplot as plt
import numpy as numpy
from polydiavlika.myglobal import *

# General distribution guidance from=Dual MAC Based Hierarchical Optical Access Network for Hyperscale Data Centers

# For on-off time modelling https://hal-enac.archives-ouvertes.fr/hal-00973913/document
def get_on_off_times(t_begin,t_end,packet_num,c_pareto,sigma):
    mean_interval_time = (t_end - t_begin) / packet_num
    on_times_abs= genpareto.rvs(c_pareto, size=packet_num)
    off_times_abs=numpy.random.lognormal(mean=math.log10(mean_interval_time), sigma=sigma, size=packet_num)
    on_period=[]
    on_periods=[]
    counter=0
    current_time=t_begin
    while current_time<=t_end:
        # off phase
        current_time=current_time+off_times_abs[counter]
        new_on_start=current_time
        # on phase
        current_time=current_time+on_times_abs[counter]
        new_off_start=current_time
        if current_time<=t_end:
            on_periods.append([new_on_start,new_off_start])
        counter=counter+1
    return on_periods

def get_interval_times_exponential(t_begin,t_end,packet_num):
    mean_interval_time=(t_end-t_begin)/packet_num
    interval_times_abs = numpy.random.exponential(scale=mean_interval_time, size=packet_num)
    interval_times_actual=[]
    new_sample_time=t_begin
    for abs_time in interval_times_abs:
        new_sample_time=new_sample_time+abs_time
        if new_sample_time>t_end:
            break
        else:
            interval_times_actual.append(new_sample_time)
    return interval_times_actual

def get_interval_times_lognormal(t_begin,t_end,packet_num,sigma):
    mean_interval_time=(t_end-t_begin)/packet_num
    interval_times_abs = numpy.random.lognormal(mean=math.log10(mean_interval_time), sigma=sigma, size=packet_num)
    interval_times_actual=[]
    new_sample_time=t_begin
    for abs_time in interval_times_abs:
        new_sample_time=new_sample_time+abs_time
        if new_sample_time>t_end:
            break
        else:
            interval_times_actual.append(new_sample_time)
    return interval_times_actual

def get_interval_times_weibull(t_begin,t_end,packet_num,alpha):
    mean_interval_time=(t_end-t_begin)/packet_num
    interval_times_abs = mean_interval_time*numpy.random.weibull(a=alpha,size=packet_num)

    print(str(interval_times_abs))
    interval_times_actual=[]
    new_sample_time=t_begin
    for abs_time in interval_times_abs:
        new_sample_time=new_sample_time+abs_time
        if new_sample_time>t_end:
            break
        else:
            interval_times_actual.append(new_sample_time)
    return interval_times_actual

def get_packet_size_constant():
    return 64

def get_packet_size_small_big(small_size,big_size,small_prob,big_prob):
    return numpy.random.choice([big_size, small_size], size=1, replace=True, p=[big_prob, small_prob])[0]

# settings
#t_gran=1 #sec
t_begin=0
t_end=3600*2
packet_num=100
size=64 #bytes
big_packet_size=1024
small_packet_size=8
big_packet_prob=0.4
small_packet_prob=0.6
sigma_lognormal=3
alpha_weibull=1
c_pareto=3
limitless=True
csv_reader=''
# create packets (main)
if limitless:
    packet_id=0
    qos='med'
    #for time in get_interval_times_exponential(t_begin,t_end,packet_num):
    for time in get_interval_times_lognormal(t_begin,t_end,packet_num,sigma_lognormal):
    #for time in get_interval_times_weibull(t_begin,t_end,packet_num,alpha_weibull):
        size=get_packet_size_small_big(small_packet_size,big_packet_size,0.7,0.3)
        toPrint = str(packet_id) + ',' + str(time) + ',' + str(size) + ',' + str(qos) + '\n'
        print(toPrint)
        csv_reader = csv_reader + toPrint
        packet_id=packet_id+1
    print(str(csv_reader))
    with open(TRAFFIC_DATASETS_FOLDER+'qos_med.csv', mode='a') as file:
        file.write('packet_id,time,size,qos\n')
        file.write(csv_reader)
else:
    packet_id=0
    qos='low'
    list_of_lists=get_on_off_times(t_begin,t_end,packet_num,c_pareto,sigma_lognormal)
    for on_time in list_of_lists:
        print('Found new ON period for '+str(on_time[0])+'-'+str(on_time[1]))
        for time in get_interval_times_lognormal(on_time[0],on_time[1],packet_num,sigma_lognormal):
            size = get_packet_size_small_big(small_packet_size, big_packet_size, small_packet_prob, big_packet_prob)
            toPrint=str(packet_id) + ',' + str(time) + ',' + str(size)+',' + str(qos) +'\n'
            print(toPrint)
            csv_reader=csv_reader+toPrint
            packet_id = packet_id + 1
    print(str(csv_reader))
    with open(TRAFFIC_DATASETS_FOLDER+'qos_low.csv', mode='a') as file:
        file.write('packet_id,time,size,qos\n')
        file.write(csv_reader)
