import datetime
import math
from scipy.stats import genpareto
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



TOTAL_NODES=8
T_BEGIN=0
T_END=0.1
duration=T_END-T_BEGIN

log_interval=duration/1000
BITRATE=1e10
timestep=1/BITRATE
def main():
    # init node and channel list
    first_time = True
    nodes=Nodes()
    channels=Channels()
    print('start 0/1000=' + str(datetime.datetime.now()))
    # create nodes and channels
    for id in range(1,TOTAL_NODES+1):
        new_traffic=Traffic_per_packet('test'+str(id)+'.csv')
        new_node=Node(id,new_traffic)
        new_node.buffer_low=Buffer(1600)
        new_node.buffer_med=Buffer(1600)
        new_node.buffer_high=Buffer(1600)
        nodes.add_new(new_node)

    for id in range(1,2):
        new_channel=Channel(id,1e10)
        channels.add_new(new_channel)
    # run simulation
    CURRENT_TIME=T_BEGIN
    while CURRENT_TIME<=T_END:
        # check if packets were born and add to buffers
        nodes.process_new_packets(CURRENT_TIME)
        # check if buffers can forward waiting packets to channels todo
        free_channel_list=channels.get_free_channel_ids(CURRENT_TIME)
        for channel_id in free_channel_list:
            next_packet=nodes.get_next_packet(CURRENT_TIME)
            if next_packet is not None:
                print('Transmitting packet=' + str(next_packet.packet_id) + 'from channel id=' + str(channel_id))
                next_packet.time_buffer_out = CURRENT_TIME
                next_packet.time_trx_in = CURRENT_TIME
                channels.transmit(next_packet,channel_id)

        # check if channels arrive at receivers todo
        arrived_packets=channels.get_arrived_packets(CURRENT_TIME)
        for packet in arrived_packets:
            packet.time_trx_out=CURRENT_TIME
            nodes.fill_receivers(arrived_packets)

        CURRENT_TIME=CURRENT_TIME+timestep

        if first_time and CURRENT_TIME > log_interval:
            print('completeness 1/1000='+str(datetime.datetime.now()))
            first_time=False

    # print buffer etc. content
    for node in nodes.db:
        print(str(node.id))
        print(str(node.receiver))
        print(str(node.dropped))
        print('---------')


main()