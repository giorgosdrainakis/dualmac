import datetime
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
from polydiavlika.nodeDUAL import *
from polydiavlika.traffic import *
from polydiavlika.buffer import *
from polydiavlika.channel import *

def main():
    # params
    BITRATE = 1e10
    myglobal.TOLERANCE = 1e-10
    myglobal.N_collision=16
    myglobal.T_send=1e-4
    myglobal.T_load=4e-5
    myglobal.T_idle=2.56e-8
    myglobal.timestep = 8e-10
    T_BEGIN = 0
    T_END = 0.08
    # constants
    TOTAL_NODES = 8
    channel_id_list = [1]
    HIGH_BUFFER_SIZE = 300 * 64
    MED_BUFFER_SIZE = int(300 * (64 * 0.7 + 1500 * 0.3))
    LOW_BUFFER_SIZE = int(300 * (64 * 0.6 + 1500 * 0.4))
    duration = T_END - T_BEGIN
    log_interval = duration / 1000

    # init node and channel list
    first_time = True
    nodes=Nodes()
    channels=Channels()

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
        channels.add_new(new_channel)

    # run simulation
    CURRENT_TIME=T_BEGIN
    print('start 0/1000=' + str(datetime.datetime.now()))
    while CURRENT_TIME<=T_END:
        # check if packets were born and add to buffers
        nodes.process_new_packets(CURRENT_TIME)
        # check if buffers can forward waiting packets to channels todo
        detected_free_channel_ids=channels.get_detected_free_channel_ids(CURRENT_TIME)
        actual_free_channel_ids=channels.get_free_channel_ids(CURRENT_TIME)
        channel_packet_tuple=nodes.get_potential_packets(CURRENT_TIME,detected_free_channel_ids,actual_free_channel_ids)

        if channel_packet_tuple is not None:
            for element in channel_packet_tuple:
                print('Transmitting packet=' + str(element[1].packet_id) + ' from channel id=' + str(element[0]))
                element[1].time_buffer_out = CURRENT_TIME
                element[1].time_trx_in = CURRENT_TIME
                channels.transmit(element[1],element[0])

        # check if channels arrive at receivers todo
        arrived_packets=channels.get_arrived_packets(CURRENT_TIME)
        for packet in arrived_packets:
            packet.time_trx_out=CURRENT_TIME
            nodes.fill_receivers(arrived_packets)

        CURRENT_TIME=CURRENT_TIME+myglobal.timestep

        if first_time and CURRENT_TIME > log_interval:
            print('completeness 1/1000='+str(datetime.datetime.now()))
            first_time=False

    # print buffer etc. content
    for node in nodes.db:
        print(str(node.id))
        print(len(node.receiver))
        print(len(node.dropped))
        print('---------')
    print('completeness 1000/1000=' + str(datetime.datetime.now()))


main()