import math
import random
from polydiavlika import myglobal

class Nodes:
    def __init__(self):
        self.db=[]
        self.mode=None # competition, polling

    def fill_receivers(self,arrived_packets):
        for packet in arrived_packets:
            for node in self.db:
                if node.id==packet.destination_id:
                    node.receiver.append(packet)
                    print('Received packet=' + str(packet.packet_id) + ' from node=' + str(packet.source_id))

    def add_new(self,node):
        self.db.append(node)

    def get_node_from_id(self,id):
        for node in self.db:
            if node.id==id:
                return node

    def decrement(self):
        for node in self.db:
            node.C_idle=max(0,node.C_idle-myglobal.timestep)
            node.C_load = max(0, node.C_load - myglobal.timestep)
            node.C_send = max(0, node.C_send - myglobal.timestep)
            node.backoff_time = max(0, node.backoff_time - myglobal.timestep)

    def get_potential_packets(self,current_time,detected_free_channel_ids,actual_free_channel_ids):
        self.decrement()
        channel_packet_tuple=[]
        final_channel_packet_tuple=[]
        if self.mode == 'competition':
            if len(detected_free_channel_ids)>0:
                for node in self.db:
                    candidate = node.get_next_packet(current_time)
                    if candidate is not None:
                        channel_id=random.choice(detected_free_channel_ids)
                        new_potential=(channel_id,candidate)
                        channel_packet_tuple.append(new_potential)
                for element in channel_packet_tuple:
                    # check for conflicts or prop delay
                    conflict_found=False
                    propagation_found=False
                    for compared in channel_packet_tuple:
                        if element[0]==compared[0] and element[1].packet_id!=compared[1].packet_id:
                            conflict_found=True
                            break
                    if element[0] not in actual_free_channel_ids:
                        propagation_found=True
                    if conflict_found or propagation_found:
                        # destroy
                        for node in self.db:
                            if node.id==element[1].source_id:
                                node.destroyed.append(element[1])
                                node.C_collision=node.C_collision+1
                                node.backoff_time=random.uniform(0, (2**node.C_collision)-1)*myglobal.timestep
                    else:
                        # add to tx
                        for node in self.db:
                            if node.id == element[1].source_id:
                                node.C_collision=0
                        final_channel_packet_tuple.append(element)
                for node in self.db:
                    if node.C_collision>=myglobal.N_collision:
                        self.switch_to_polling(node.id)
                        break
                return final_channel_packet_tuple
            else:
                return None
        elif self.mode == 'polling':
            for node in self.db:
                if node.flag_B=='send':
                    candidate = node.get_next_packet(current_time)
                    if candidate is None:
                        node.flag_B='stop'
                        node.C_idle=myglobal.T_idle
                    else:
                        channel_id=random.choice(actual_free_channel_ids)
                        new_potential=(channel_id,candidate)
                        final_channel_packet_tuple.append(new_potential)
                        return final_channel_packet_tuple
            for node in self.db:
                if node.C_load==0 or node.C_idle==0:
                    self.switch_to_competition(node.id)
        else:
            print('Error - cannot find rack mode')
            return None

    def switch_to_competition(self,node_id):
        print('switching to compete')
        self.mode='competition'
        for node in self.db:
            node.flag_A = 'competition'
            node.flag_B = 'stop'

    def switch_to_polling(self,node_id):
        print('switching to polling')
        self.mode='polling'
        for node in self.db:
            node.flag_A = 'polling'
            if node.id==node_id:
                node.flag_B = 'send'
                node.C_send=myglobal.T_send
            else:
                node.flag_B = 'stop'

    def get_next_packet(self,current_time):
        for node in self.db:
            candidate=node.get_next_packet(current_time)
            if candidate is not None:
                return candidate
        return None

    def process_new_packets(self,current_time):
        for node in self.db:
            node.process_new_packets(current_time)

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
        self.receiver=[]
        self.dropped=[]
        self.destroyed=[]
        self.flag_A=None # competition, polling
        self.flag_B = None # send, stop
        self.C_send=0
        self.C_idle=0
        self.C_collision=0
        self.C_load=0
        self.backoff_time=0

    def process_new_packets(self,current_time):
        new_packets=self.traffic.get_new_packets(current_time)
        for packet in new_packets:
            is_in_buffer=False
            if packet.packet_qos=='low':
                is_in_buffer=self.buffer_low.add(packet)
                print('Added packet=' + str(packet.packet_id) + ' in low buffer node=' + str(self.id))
            elif packet.packet_qos=='med':
                is_in_buffer=self.buffer_med.add(packet)
                print('Added packet=' + str(packet.packet_id) + ' in  med buffer node=' + str(self.id))
            elif packet.packet_qos=='high':
                is_in_buffer=self.buffer_high.add(packet)
                print('Added packet=' + str(packet.packet_id) + ' in high buffer node=' + str(self.id))
            if not is_in_buffer:
                print('Dropped packet='+str(packet.packet_id)+' in node='+str(self.id))
                self.dropped.append(packet)

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








