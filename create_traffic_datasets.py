import datetime
import math
import random
from polydiavlika import myglobal
from scipy.stats import genpareto
import matplotlib.pyplot as plt
import numpy as numpy
from scipy.stats import weibull_min

def get_variable_packet_size(small_size,big_size,small_prob):
    myrand=random.random()
    if (myrand<=small_prob):
        ret=small_size
    else:
        ret=big_size
    return ret

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
    interval_times_abs = numpy.random.lognormal(mean=math.log2(mean_interval_time), sigma=sigma, size=packet_num)
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
    #interval_times_abs = mean_interval_time*numpy.random.weibull(a=alpha,size=packet_num)
    interval_times_abs = weibull_min.rvs(alpha, loc=0, scale=mean_interval_time, size=packet_num)
    interval_times_actual=[]
    new_sample_time=t_begin
    for abs_time in interval_times_abs:
        new_sample_time=new_sample_time+abs_time
        if new_sample_time>t_end:
            break
        else:
            interval_times_actual.append(new_sample_time)
    return interval_times_actual

def get_on_off_times(t_begin,t_end,packet_num,c_pareto,sigma):
    mean_interval_time=(t_end-t_begin)/packet_num
    #on_times_abs=gprnd(c_pareto,mean_interval_time,0,1,packet_num) todo
    on_times_abs = genpareto.rvs(c_pareto,scale=mean_interval_time, size=packet_num)
    #off_times_abs=lognrnd(log(mean_interval_time),sigma,1,packet_num) todo
    off_times_abs = numpy.random.lognormal(mean=math.log(mean_interval_time,2), sigma=sigma, size=packet_num)
    on_periods=[]
    counter=1
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

def generate_packets_low_qos(packet_id,t_begin,t_end,avg_throughput,source_id,destination_ids,c_pareto,sigma_lognormal,alpha):
    csv_reader=''
    first_packet_id=packet_id
    avg_packet_size=64*0.6+1500*0.4 #bytes
    avg_traffic=avg_throughput*(t_end-t_begin) #bytes
    avg_packet_num=round(avg_traffic/avg_packet_size)
    on_times=get_on_off_times(t_begin,t_end,avg_packet_num,c_pareto,sigma_lognormal)
    total_len=len(on_times)
    for on_time in on_times:
        avg_traffic=avg_throughput*(on_time[1]-on_time[0])
        avg_packet_num = max(round(avg_traffic / avg_packet_size),1)
        interval_times=get_interval_times_weibull(on_time[0],on_time[1],avg_packet_num,alpha)
        for inttime in interval_times:
            new_time=inttime
            packet_size = get_variable_packet_size(64, 1500, 0.6)
            qos = 'low'
            destination_id=random.sample(destination_ids,1)[0]
            csv_reader=csv_reader+str(packet_id)+','+str(new_time)+','\
                       +str(packet_size)+','+str(qos)+','+str(source_id)+','+str(destination_id)+'\n'
            packet_id = packet_id + 1
            print('low='+str((packet_id-first_packet_id)/total_len))
    return csv_reader,packet_id

def generate_packets_med_qos(packet_id,t_begin,t_end,avg_throughput,source_id,destination_ids,sigma_lognormal):
    csv_reader=''
    first_packet_id=packet_id
    avg_packet_size=64*0.7+1500*0.3#bytes
    avg_traffic=avg_throughput*(t_end-t_begin) #bytes
    avg_packet_num=round(avg_traffic/avg_packet_size)
    interval_times=get_interval_times_lognormal(t_begin,t_end,avg_packet_num,sigma_lognormal)
    total_len=len(interval_times)
    for inttime in interval_times:
        packet_size=get_variable_packet_size(64,1500,0.7)
        qos='med'
        new_time=inttime
        destination_id = random.sample(destination_ids, 1)[0]
        csv_reader = csv_reader + str(packet_id) + ',' + str(new_time) + ',' \
                     + str(packet_size) + ',' + str(qos) + ',' + str(source_id) + ',' + str(destination_id) + '\n'
        packet_id = packet_id + 1
        print('med='+str((packet_id-first_packet_id)/total_len))
    return csv_reader,packet_id

def generate_packets_high_qos(packet_id,t_begin,t_end,avg_throughput,source_id,destination_ids):
    csv_reader=''
    packet_id=packet_id
    first_packet_id=packet_id
    avg_packet_size=64#bytes
    avg_traffic=avg_throughput*(t_end-t_begin)#bytes
    avg_packet_num=round(avg_traffic/avg_packet_size)
    interval_times=get_interval_times_exponential(t_begin,t_end,avg_packet_num)
    total_len=len(interval_times)
    for inttime in interval_times:
        packet_size=avg_packet_size
        qos='high'
        new_time=inttime
        destination_id = random.sample(destination_ids, 1)[0]
        csv_reader = csv_reader + str(packet_id) + ',' + str(new_time) + ',' \
                     + str(packet_size) + ',' + str(qos) + ',' + str(source_id) + ',' + str(destination_id) + '\n'
        packet_id=packet_id+1
        print('high='+str((packet_id-first_packet_id)/total_len))
    return csv_reader,packet_id

def export_traffic_dataset(nodes,t_begin,t_end,avg_throughput,qos,hasHeader):
    sigma_lognormal_low = 2.6
    sigma_lognormal_med = 1
    alpha_weibull = 0.8
    c_pareto = 0.5
    csv_content = ''
    nodes_dict = list(range(1, nodes+1))

    # For every source node
    for source_id in range(1,nodes+1):
        print('Node '+str(source_id))
        if nodes==1:
            dest_ids=[0,0]
        else:
            dest_ids=[x for x in nodes_dict if x != source_id]
            # If only two nodes, force each to send to the other
            if len(dest_ids)==1:
                dest_ids=[dest_ids,dest_ids]

        # Generate low qos traffic
        if qos=='all' or qos=='low':
            low_packets=generate_packets_low_qos(t_begin,t_end,avg_throughput,source_id,dest_ids,c_pareto,sigma_lognormal_low,alpha_weibull)
            if low_packets is None:
                print('Warning: No low packets generated - check distribution params')
            else:
                csv_content = csv_content+low_packets


        # Generate medium qos traffic
        if qos=='all' or qos=='med':
            med_packets=generate_packets_med_qos(t_begin,t_end,avg_throughput,source_id,dest_ids,sigma_lognormal_med)
            if med_packets is None:
                print('Warning: No med packets generated - check distribution params')
            else:
                csv_content = csv_content+med_packets

        # Generate high qos traffic
        if qos=='all' or qos=='high':
            high_packets=generate_packets_high_qos(t_begin,t_end,avg_throughput,source_id,dest_ids)
            if high_packets is None:
                print('Warning: No high packets generated - check distribution params')
            else:
                csv_content = csv_content+high_packets

    csv_names='packet_id,time,packet_size,packet_qos,source_id,destination_id\n'
    if hasHeader:
        output_table= csv_names+csv_content
    else:
        output_table=csv_content

    mytime = str(datetime.datetime.now())
    mytime = mytime.replace('-', '_')
    mytime = mytime.replace(' ', '_')
    mytime = mytime.replace(':', '_')
    mytime = mytime.replace('.', '_')

    with open(Global._ROOT + Global._LOGS_FOLDER + 'traffic_dataset_packets_'+mytime + ".txt", mode='a') as file:
        file.write(output_table + '\n')

def export_traffic_dataset_single(nodeid,nodeslist,t_begin,t_end,avg_throughput,qos,hasHeader):
    packet_id=0
    sigma_lognormal_low = 1
    sigma_lognormal_med = 1
    alpha_weibull = 0.1
    c_pareto = 0.8
    csv_content = ''

    # For every source node
    dest_ids=nodeslist

    # Generate low qos traffic
    if qos=='all' or qos=='low':
        low_packets,packet_id=generate_packets_low_qos(packet_id,t_begin,t_end,avg_throughput,nodeid,dest_ids,c_pareto,sigma_lognormal_low,alpha_weibull)
        if low_packets is None:
            print('Warning: No low packets generated - check distribution params')
        else:
            csv_content = csv_content+low_packets

    # Generate medium qos traffic
    if qos=='all' or qos=='med':
        med_packets,packet_id=generate_packets_med_qos(packet_id,t_begin,t_end,avg_throughput,nodeid,dest_ids,sigma_lognormal_med)
        if med_packets is None:
            print('Warning: No med packets generated - check distribution params')
        else:
            csv_content = csv_content+med_packets

    # Generate high qos traffic
    if qos=='all' or qos=='high':
        high_packets,packet_id=generate_packets_high_qos(packet_id,t_begin,t_end,avg_throughput,nodeid,dest_ids)
        if high_packets is None:
            print('Warning: No high packets generated - check distribution params')
        else:
            csv_content = csv_content+high_packets

    csv_names='packet_id,time,packet_size,packet_qos,source_id,destination_id\n'
    if hasHeader:
        output_table= csv_names+csv_content
    else:
        output_table=csv_content

    mytime = str(datetime.datetime.now())
    mytime = mytime.replace('-', '_')
    mytime = mytime.replace(' ', '_')
    mytime = mytime.replace(':', '_')
    mytime = mytime.replace('.', '_')

    with open(myglobal.ROOT + myglobal.TRAFFIC_DATASETS_FOLDER+ mytime + ".csv", mode='a') as file:
        file.write(output_table + '\n')

t_begin=0 #sec (float)
t_end=0.8 #sec (float)
avg_throughput=1.25e9/3 #bytes! per sec (int) or 3.125
node_id_list=[1] # (int)
maxnodeslist = [1, 2, 3, 4, 5, 6, 7, 8]
avg_throughput=avg_throughput/len(maxnodeslist)
qos='all'# {'low','med','high','all'} (string)

# traffic dset is created by default in same dir as 'traffic_dataset.csv'
for nodeid in node_id_list:
    nodeslist=[item for item in maxnodeslist if item not in node_id_list]
    hasHeader=True
    export_traffic_dataset_single(nodeid,nodeslist,t_begin,t_end,avg_throughput,qos,hasHeader)



