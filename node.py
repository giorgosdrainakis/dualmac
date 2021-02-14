import math
class Nodes:
    db=[]

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
        if self.buffer_high.has_packets():
            return self.buffer_high.get_next_packet()
        elif self.buffer_med.has_packets():
            return self.buffer_med.get_next_packet()
        elif self.buffer_low.has_packets():
            return self.buffer_low.get_next_packet()
        else:
            return None







