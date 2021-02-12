import math
from scipy.stats import genpareto
import matplotlib.pyplot as plt
import numpy as numpy
from polydiavlika.myglobal import *

# General distribution guidance from=Dual MAC Based Hierarchical Optical Access Network for Hyperscale Data Centers
sigma_lognormal_low=2.6
sigma_lognormal_med=1
alpha_weibull=1
c_pareto=0.5
# For on-off time modelling https://hal-enac.archives-ouvertes.fr/hal-00973913/document
def get_on_off_times(t_begin,t_end,packet_num,c_pareto,sigma):
    print(str(t_begin))
    print(str(t_end))
    mean_interval_time = (t_end - t_begin) / packet_num
    on_times_abs= genpareto.rvs(c_pareto, size=int(packet_num/2),scale=mean_interval_time)
    print('On time abs='+str(on_times_abs))
    off_times_abs=numpy.random.lognormal(mean=math.log(mean_interval_time), sigma=sigma, size=int(packet_num/2))
    print('Off time abs='+str(off_times_abs))
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
    interval_times_abs = numpy.random.lognormal(mean=math.log(mean_interval_time), sigma=sigma, size=packet_num)
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

def get_packet_size_small_big(small_size,big_size,small_prob,big_prob):
    return numpy.random.choice([big_size, small_size], size=1, replace=True, p=[big_prob, small_prob])[0]

# create packets (main)
def generate_packets_high_qos(t_begin,t_end,avg_throughput):
    packet_id=0
    csv_reader=''
    avg_packet_size=64#bytes
    avg_traffic=avg_throughput*(t_end-t_begin) #bytes
    avg_packet_num=int(avg_traffic/avg_packet_size)

    for time in get_interval_times_exponential(t_begin,t_end,avg_packet_num):
        size = avg_packet_size
        qos='high'
        packet_stats = str(packet_id) + ',' + str(time) + ',' + str(size) + ',' + str(qos) + '\n'
        csv_reader = csv_reader + packet_stats
        print('Debug: New packet= '+str(packet_stats))
        packet_id=packet_id+1
    with open(TRAFFIC_DATASETS_FOLDER+'qos_high.csv', mode='a') as file:
        #file.write('packet_id,time,size,qos\n')
        file.write(csv_reader)

def generate_packets_med_qos(t_begin,t_end,avg_throughput,sigma_lognormal):
    packet_id=0
    csv_reader=''
    avg_packet_size = 40*0.7+1500*0.3  # bytes
    avg_traffic=avg_throughput*(t_end-t_begin) #bytes
    avg_packet_num=int(avg_traffic/avg_packet_size)

    for time in get_interval_times_lognormal(t_begin, t_end, avg_packet_num, sigma_lognormal):
        size=get_packet_size_small_big(40,1500,0.7,0.3)
        qos='med'
        packet_stats = str(packet_id) + ',' + str(time) + ',' + str(size) + ',' + str(qos) + '\n'
        csv_reader = csv_reader + packet_stats
        packet_id=packet_id+1
    with open(TRAFFIC_DATASETS_FOLDER+'qos_med.csv', mode='a') as file:
        #file.write('packet_id,time,size,qos\n')
        file.write(csv_reader)

def generate_packets_low_qos(t_begin,t_end,avg_throughput,c_pareto,sigma_lognormal):
    packet_id=0
    csv_reader=''
    avg_packet_size = 40*0.6+1500*0.4  # bytes
    avg_traffic=avg_throughput*(t_end-t_begin) #bytes
    avg_packet_num=int(avg_traffic/avg_packet_size)
    print('Average packet num 1= ' +str(avg_packet_num))
    on_times=get_on_off_times(t_begin,t_end,avg_packet_num,c_pareto,sigma_lognormal)

    for on_time in on_times:
        print('Found new ON period for '+str(on_time[0])+'-'+str(on_time[1]))
        avg_traffic = avg_throughput * (on_time[1] - on_time[0])  # bytes
        avg_packet_num = max(int(avg_traffic / avg_packet_size),1)
        for time in get_interval_times_weibull(on_time[0], on_time[1], avg_packet_num, alpha_weibull):
            size = get_packet_size_small_big(40, 1500, 0.6, 0.4)
            qos = 'low'
            packet_stats=str(packet_id) + ',' + str(time) + ',' + str(size)+',' + str(qos) +'\n'
            csv_reader=csv_reader+packet_stats
            packet_id = packet_id + 1
    with open(TRAFFIC_DATASETS_FOLDER+'qos_low.csv', mode='a') as file:
        #file.write('packet_id,time,size,qos\n')
        file.write(csv_reader)

t_begin=0#sec
t_end=0.1 #sec
avg_throughput=1e8 #bytes per sec


    #generate_packets_low_qos(t_begin,t_end,avg_throughput,c_pareto,sigma_lognormal_low)

for i in range(0, 7):
    #generate_packets_med_qos(t_begin,t_end,avg_throughput,sigma_lognormal_med)
    generate_packets_high_qos(t_begin,t_end,avg_throughput)