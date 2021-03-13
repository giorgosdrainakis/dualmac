import math
import random
from polydiavlika import myglobal
from polydiavlika.channel import *

class Nodes:
    def __init__(self):
        self.db=[]
        self.mode=None # competition, polling
        self.channels=Channels()
        self.control_channel=None
        self.last_lucky_WAA=0
        self.A_matrix_WAA=[]

    def add_new_packets_to_buffers(self,current_time):
        for node in self.db:
            node.add_new_packets_to_buffers(current_time)

    def transmit_CD(self,current_time):
        self.transmit_CA(current_time)

    def transmit_CA(self, current_time):
        self.decrement()
        #detected_free_channel_ids = self.channels.get_detected_free_channel_ids(current_time)
        detected_free_channels = self.channels.get_detected_free_channels(current_time)
        actual_free_channels=self.channels.get_free_channels(current_time) # todo works for 1 channel
        #print('Detected='+str(len(detected_free_channels)))
        #print('Free=' + str(len(actual_free_channels)))
        if self.mode == 'competition':
            for node in self.db:
                aa=node.transmit(current_time, detected_free_channels)
                #print(str(aa) + ',' + str(node.id))
            #print('----')
        elif self.mode == 'polling':
            for node in self.db:
                if node.flag_B == 'send':
                    aa=node.transmit(current_time, actual_free_channels)
                    #print((str(node.C_load) + ',' + str(node.C_idle) + ',' + str(node.C_send) + ','+str(aa)+ ','+str(node.id)))
                    if node.current_packet is None or node.C_send==0:
                        node.flag_B = 'stop'
                    else:
                        node.C_idle = myglobal.T_idle
            #print('----')
        else:
            print('Error - cannot find rack mode')

    def calculate_process_table_WAA(self,current_time):
        pass

    def calculate_buffer_image_WAA(self,current_time):
        total_control_message=[]
        for node in self.db:
            msg=get_message_WAA()

    def transmit_WAA(self, current_time):
        if self.check_new_cycle_WAA(current_time):
            self.calculate_process_table_WAA(current_time)
        for node in self.db:
            node.transmit_WAA(current_time, detected_free_channels)
            node.transmit_control() # ensomatomeno me to panw todo

    def check_transmission_WAA(self,current_time):
        # check conflicts due to instanteous transmission
        # check arrivals
        for node in self.db:
            node.check_arrival_WAA(current_time)

    def check_transmission_CA(self,current_time):
        # check conflicts due to instanteous transmission
        last_collided_channel_ids=[]
        for node in self.db:
            for other_node in self.db:
                if other_node.id!=node.id and \
                        node.current_channel_id is not None and \
                        other_node.current_channel_id is not None and \
                        other_node.current_channel_id==node.current_channel_id :
                            last_collided_channel_ids.append(node.current_channel_id)
                            node.current_packet_does_collide=True
        last_collided_channel_ids=set(last_collided_channel_ids)
        # check arrivals
        for node in self.db:
            node.check_arrival_CA(current_time)

        for channel in self.channels.db:
            found=False
            for node in self.db:
                if node.current_channel_id==channel.id:
                    found=True
                    channel.detect_tx_in=min(channel.detect_tx_in,node.current_packet.time_trx_in+channel.propagation_time)
                    channel.detect_tx_out=max(channel.detect_tx_out,node.current_packet.time_trx_out+channel.propagation_time)
                    channel.tx_in = min(channel.tx_in,node.current_packet.time_trx_in)
                    channel.tx_out = max(channel.tx_out,node.current_packet.time_trx_out)
            if not found and channel.id in last_collided_channel_ids:
                channel.detect_tx_in = -1
                channel.detect_tx_out = current_time + channel.propagation_time
                channel.tx_in = -1
                channel.tx_out = current_time

        # counters and protocol checks
        if self.mode=='polling':
            for node in self.db:
                if node.C_load == 0 or node.C_idle == 0:
                    self.switch_to_competition(node.id)
                    break
        elif self.mode=='competition':
            for node in self.db:
                if node.C_collision>=myglobal.N_collision:
                    self.switch_to_polling(node.id)
                    break
        else:
            print('Error - cannot find rack mode in protocol check')

    def check_transmission_CD(self,current_time):
        # check conflicts due to instanteous transmission
        last_collided_channel_ids=[]
        for node in self.db:
            for other_node in self.db:
                if other_node.id!=node.id and \
                        node.current_channel_id is not None and \
                        other_node.current_channel_id is not None and \
                        other_node.current_channel_id==node.current_channel_id :
                            last_collided_channel_ids.append(node.current_channel_id)
                            node.current_packet_does_collide=True
        last_collided_channel_ids=set(last_collided_channel_ids)
        # check arrivals
        for node in self.db:
            node.check_arrival_CD(current_time)

        for channel in self.channels.db:
            found=False
            for node in self.db:
                if node.current_channel_id==channel.id:
                    found=True
                    channel.detect_tx_in=min(channel.detect_tx_in,node.current_packet.time_trx_in+channel.propagation_time)
                    channel.detect_tx_out=max(channel.detect_tx_out,node.current_packet.time_trx_out+channel.propagation_time)
                    channel.tx_in = min(channel.tx_in,node.current_packet.time_trx_in)
                    channel.tx_out = max(channel.tx_out,node.current_packet.time_trx_out)
            if not found and channel.id in last_collided_channel_ids:
                channel.detect_tx_in = -1
                channel.detect_tx_out = current_time + channel.propagation_time
                channel.tx_in = -1
                channel.tx_out = current_time

        # counters and protocol checks
        if self.mode=='polling':
            for node in self.db:
                if node.C_load == 0 or node.C_idle == 0:
                    self.switch_to_competition(node.id)
                    break
        elif self.mode=='competition':
            for node in self.db:
                if node.C_collision>=myglobal.N_collision:
                    self.switch_to_polling(node.id)
                    break
        else:
            print('Error - cannot find rack mode in protocol check')

    def have_buffers_packets(self):
        for node in self.db:
            if node.have_buffers_packets():
                return True

    def add_new(self,node):
        self.db.append(node)

    def get_node_from_id(self,id):
        for node in self.db:
            if node.id==id:
                return node

    def decrement(self):
        #back_times=[]
        for node in self.db:
            node.waiting=max(0,node.waiting-myglobal.timestep)
            node.C_idle=max(0,node.C_idle-myglobal.timestep)
            node.C_load = max(0, node.C_load - myglobal.timestep)
            node.C_send = max(0, node.C_send - myglobal.timestep)
            if node.flag_A=='competition':
                node.backoff_time = max(0, node.backoff_time - myglobal.timestep)
            #back_times.append(node.backoff_time)
        #print(str(back_times))

    def switch_to_competition(self,node_id):
        print('switching to compete')
        self.mode='competition'
        for node in self.db:
            node.flag_A = 'competition'
            node.flag_B = 'stop'
            node.waiting=myglobal.WAITING

    def switch_to_polling(self,node_id):
        print('switching to polling')
        self.mode='polling'
        for node in self.db:
            node.waiting=myglobal.WAITING
            node.flag_A = 'polling'
            if node.id==node_id:
                node.C_collision = 0
                node.backoff_time = 0
                node.flag_B = 'send'
                node.C_send=myglobal.T_send
                node.C_load=myglobal.T_load
            else:
                node.flag_B = 'stop'
                node.C_send=math.inf
                node.C_load=math.inf
                node.C_idle = math.inf
        #print(str(print_has_buffer_list))

    def get_next_packet(self,current_time):
        for node in self.db:
            candidate=node.get_next_packet(current_time)
            if candidate is not None:
                return candidate
        return None

    def process_buffers(self,current_time):
        for node in self.db:
            node.process_buffers(current_time)

class Node:
    def __init__(self,id,traffic):
        self.id=id
        self.traffic=traffic
        self.buffer_low=None
        self.buffer_med=None
        self.buffer_high=None
        self.received=[]
        self.dropped=[]
        self.destroyed=[]
        self.flag_A=None # competition, polling
        self.flag_B = None # send, stop
        self.C_send=math.inf
        self.C_idle=math.inf
        self.C_collision=0
        self.C_load=math.inf
        self.backoff_time=0
        self.current_packet=None
        self.current_channel_id=None
        self.current_packet_does_collide=False #
        self.waiting=0
        self.packets_WAA=[]

    def print_buff(self):
        mystr='-'+str(self.buffer_low.get_current_size())+'-'+str(self.buffer_med.get_current_size())+'-'+str(self.buffer_high.get_current_size())
        return mystr
    def have_buffers_packets(self):
        if self.buffer_low.has_packets() or self.buffer_med.has_packets() or self.buffer_high.has_packets():
            return True

    def get_message_WAA(self):
        for counter in range(0,myglobal.WAA_capacity_64):
            newline=self.buffer_high.encode_packet_WAA(counter)

        for counter in range(0,myglobal.WAA_capacity_64):
            newline=self.buffer_med.encode_packet_WAA(counter)

        for counter in range(0,myglobal.WAA_capacity_64):
            newline=self.buffer_low.encode_packet_WAA(counter)


    def transmit(self,current_time,detected_free_channels):
        if self.waiting>0:
            return -11
        if detected_free_channels is None:
            return -1
        if len(detected_free_channels)==0:
            return -2
        if self.is_transmitting(current_time):
            return -3
        if self.backoff_time>0:
            return -4
        mychannel = random.choice(detected_free_channels)
        if self.current_packet is None:
            pack=self.get_next_packet(current_time)
            if pack is None:
                return -5
            pack.time_buffer_out=current_time
            pack.time_trx_in=current_time
            pack.time_trx_out=current_time+mychannel.get_total_time_to_tx(pack.packet_size)
            self.current_packet=pack
            self.current_channel_id=mychannel.id
            self.current_packet_does_collide = False
            print('Transmitting packet id=' + str(self.current_packet.packet_id) + ' from node=' + str(self.id))
        else:
            self.current_packet.time_trx_in=current_time
            self.current_packet.time_trx_out = current_time + mychannel.get_total_time_to_tx(self.current_packet.packet_size)
            self.current_channel_id = mychannel.id
            self.current_packet_does_collide=False
            print('REtransmitting packet id=' + str(self.current_packet.packet_id) + ' from node=' + str(self.id))

    def check_arrival_CD(self,current_time):
        if self.current_packet is not None:
            has_packet_arrived=self.current_packet.time_trx_in<self.current_packet.time_trx_out and self.current_packet.time_trx_out<=current_time
            if has_packet_arrived:
                if self.current_packet_does_collide:
                    self.C_collision = self.C_collision + 1
                    #print(str(self.C_collision))
                    #self.backoff_time = max(int(random.uniform(0, (2 ** self.C_collision) - 1)),1) * myglobal.timestep
                    self.backoff_time=max(random.randint(0, (2 ** self.C_collision) - 1),1)* myglobal.timeslot
                    self.current_packet.time_trx_out=-1
                    self.current_packet.time_trx_in = -1
                    print('Collision of packet at arrival =' + str(self.current_packet.packet_id) +' from node='+str(self.id) )
                else:
                    self.C_collision=0
                    self.current_packet.time_trx_out=current_time
                    self.current_packet.mode=self.flag_A
                    self.received.append(self.current_packet)
                    print('Received packet=' + str(self.current_packet.packet_id) + ' from node=' + str(self.current_packet.source_id))
                    self.current_packet = None

                self.current_channel_id=None
                self.current_packet_does_collide=False

    def check_arrival_CA(self,current_time):
        if self.current_packet is not None:
            has_packet_arrived=self.current_packet.time_trx_in<self.current_packet.time_trx_out and self.current_packet.time_trx_out<=current_time
            if has_packet_arrived:
                if self.current_packet_does_collide:
                    self.C_collision = self.C_collision + 1
                    #print(str(self.C_collision))
                    #self.backoff_time = max(int(random.uniform(0, (2 ** self.C_collision) - 1)),1) * myglobal.timestep
                    self.backoff_time=max(random.randint(0, (2 ** self.C_collision) - 1),1)* myglobal.timeslot
                    self.current_packet.time_trx_out=-1
                    self.current_packet.time_trx_in = -1
                    print('Collision of packet at arrival =' + str(self.current_packet.packet_id) +' from node='+str(self.id) )
                else:
                    self.C_collision=0
                    self.current_packet.time_trx_out=current_time
                    self.current_packet.mode=self.flag_A
                    self.received.append(self.current_packet)
                    print('Received packet=' + str(self.current_packet.packet_id) + ' from node=' + str(self.current_packet.source_id))
                    self.current_packet = None

                self.current_channel_id=None
                self.current_packet_does_collide=False
            else: #packet has not arrived
                if self.current_packet_does_collide:
                    self.C_collision = self.C_collision + 1
                    #print(str(self.C_collision))
                    #self.backoff_time = max(int(random.uniform(0, (2 ** self.C_collision) - 1)),1) * myglobal.timestep
                    self.backoff_time=max(random.randint(0, (2 ** self.C_collision) - 1),1)* myglobal.timeslot
                    self.current_packet.time_trx_out=-1
                    self.current_packet.time_trx_in = -1
                    self.current_channel_id = None
                    self.current_packet_does_collide = False
                    print('Collision of packet at TRXing =' + str(self.current_packet.packet_id) +' from node='+str(self.id) +' ,added backoff='+str(self.backoff_time))
                else:
                    pass
                    #print('TRXing/Waiting packet=' + str(self.current_packet.packet_id) + ' from node=' + str(self.current_packet.source_id))

    def check_arrival_WAA(self,current_time):
        for pack in self.packets_WAA:
            has_packet_arrived=pack.time_trx_in<pack.time_trx_out and pack.time_trx_out<=current_time
            if has_packet_arrived:
                pack.time_trx_out=current_time
                self.received.append(pack)
                self.packets_WAA.remove(pack)
                print('Received packet=' + str(pack.packet_id) + ' from node=' + str(pack.source_id))
            else: #packet has not arrived
                pass

    def add_new_packets_to_buffers(self,current_time):
        new_packets=self.traffic.get_new_packets(current_time)
        for packet in new_packets:
            is_in_buffer=False
            if packet.packet_qos=='low':
                is_in_buffer=self.buffer_low.add(packet,current_time)
                #('Added packet=' + str(packet.packet_id) + ' in low buffer node=' + str(self.id))
            elif packet.packet_qos=='med':
                is_in_buffer=self.buffer_med.add(packet,current_time)
                #print('Added packet=' + str(packet.packet_id) + ' in  med buffer node=' + str(self.id))
            elif packet.packet_qos=='high':
                is_in_buffer=self.buffer_high.add(packet,current_time)
                #print('Added packet=' + str(packet.packet_id) + ' in high buffer node=' + str(self.id))
            if not is_in_buffer:
                print('Dropped packet='+str(packet.packet_id)+' in node='+str(self.id))
                packet.mode=self.flag_A
                self.dropped.append(packet)

    def is_transmitting(self,current_time):
        if self.current_packet is not None:
            if current_time<self.current_packet.time_trx_out+myglobal.PROPAGATION_TIME and self.current_packet.time_trx_in<self.current_packet.time_trx_out :
                return True
        return False

    def get_next_packet(self,current_time):
        if self.backoff_time==0:
            if self.buffer_high.has_packets():
                return self.buffer_high.get_next_packet()
            elif self.buffer_med.has_packets():
                if self.buffer_low.has_packets():
                    lucky=random.uniform(0, 1)
                    if lucky<0.3:
                        self.buffer_low.get_next_packet()
                    else:
                        self.buffer_med.get_next_packet()
                else:
                    return self.buffer_med.get_next_packet()
            elif self.buffer_low.has_packets():
                return self.buffer_low.get_next_packet()
            else:
                return None
        else:
            return None








