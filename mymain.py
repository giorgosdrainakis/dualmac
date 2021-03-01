import datetime
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as numpy
from polydiavlika.myglobal import *
import csv
import math
from scipy.stats import genpareto
import matplotlib.pyplot as plt
import numpy as numpy
import random
import numpy as np
import statistics
import csv
import matplotlib
from matplotlib.ticker import MaxNLocator
from polydiavlika.node import *
from polydiavlika.traffic import *
from polydiavlika.buffer import *
from polydiavlika.channel import *

def main():
    # params
    MODE='DUAL' # or WAA
    if MODE=='DUAL':
        BITRATE = 5e9
        channel_id_list = [1]  # one data channel
    else:
        BITRATE=10e9
        channel_id_list = [2] # 2 data channel
        control_channel_id = 5000 # 1 control channel
    T_BEGIN = 0
    T_END = 0.008
    # constants
    TOTAL_NODES =  8
    HIGH_BUFFER_SIZE = 1e6
    MED_BUFFER_SIZE = 1e6
    LOW_BUFFER_SIZE = 1e6
    duration = T_END - T_BEGIN
    log_interval = duration / 1000 # for debugging

    # init node and channel list
    first_time = True # for debugging
    nodes=Nodes()

    # create nodes and channels
    for id in range(1,TOTAL_NODES+1):
        new_traffic=Traffic_per_packet('test'+str(id)+'.csv')
        new_node=Node(id,new_traffic)
        new_node.buffer_low=Buffer(LOW_BUFFER_SIZE)
        new_node.buffer_med=Buffer(MED_BUFFER_SIZE)
        new_node.buffer_high=Buffer(HIGH_BUFFER_SIZE)
        new_node.flag_A='competition'
        new_node.flag_B=None
        nodes.add_new(new_node)
    nodes.mode='competition'

    for id in channel_id_list:
        new_channel=Channel(id,BITRATE)
        nodes.channels.add_new(new_channel)

    if MODE=='WAA':
        control_channel=Channel(control_channel_id,BITRATE)
        nodes.control_channel=control_channel

    # run simulation
    CURRENT_TIME=T_BEGIN
    print('start 0/1000=' + str(datetime.datetime.now()))
    while CURRENT_TIME<=T_END or nodes.have_buffers_packets():
        nodes.add_new_packets_to_buffers(CURRENT_TIME)
        if MODE == 'DUAL':  # collision avoidance CA
            nodes.check_transmission_CA(CURRENT_TIME)
            nodes.transmit_CA(CURRENT_TIME)
        else: # new protocol
            nodes.check_transmission_WAA(CURRENT_TIME)
            nodes.transmit_WAA(CURRENT_TIME)
        CURRENT_TIME=CURRENT_TIME+myglobal.timestep
        # debugging
        if first_time and CURRENT_TIME > log_interval:
            print('completeness 1/1000='+str(datetime.datetime.now()))
            first_time=False
    print('FINISH!')
    # print buffer etc. content
    mytime = str(datetime.datetime.now())
    mytime = mytime.replace('-', '_')
    mytime = mytime.replace(' ', '_')
    mytime = mytime.replace(':', '_')
    mytime = mytime.replace('.', '_')

    filenames=[]
    for node in nodes.db:
        output_table = 'packet_id,time,packet_size,packet_qos,source_id,destination_id,' \
                       'time_buffer_in,time_buffer_out,time_trx_in,time_trx_out,mode\n'
        print('id='+str(node.id))
        print('rx='+str(len(node.received)))
        print('ovflow='+str(len(node.dropped)))
        print('desotryed='+str(len(node.destroyed)))
        print('---------')
        for packet in node.received:
            output_table=output_table+packet.show()+'\n'
        for packet in node.dropped:
            output_table=output_table+packet.show()+'\n'
        for packet in node.destroyed:
            output_table=output_table+packet.show()+'\n'

        print('Writing node +...'+str(node.id))
        nodename=myglobal.ROOT + 'log'+ mytime +  str(node.id) +".csv"
        with open(nodename, mode='a') as file:
            file.write(output_table)
            filenames.append(nodename)

    combined_csv = pd.concat([pd.read_csv(f) for f in filenames])
    combined_name=myglobal.ROOT+'combined'+str(mytime)+'.csv'
    combined_csv.to_csv(combined_name, index=False)

    print('Sorting...')
    with open(combined_name, 'r', newline='') as f_input:
        csv_input = csv.DictReader(f_input)
        data = sorted(csv_input, key=lambda row: (float(row['time']), float(row['packet_id'])))

    print('Rewriting...')
    with open(combined_name, 'w', newline='') as f_output:
        csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
        csv_output.writeheader()
        csv_output.writerows(data)

    print('completeness 1000/1000=' + str(datetime.datetime.now()))
main()