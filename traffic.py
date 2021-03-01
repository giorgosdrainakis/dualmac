import csv
import math

from polydiavlika import myglobal

class Packet:
    def __init__(self,packet_id,time,packet_size,packet_qos,source_id,destination_id):
        self.packet_id=int(packet_id)
        self.time=float(time)
        self.packet_size=float(packet_size)
        self.packet_qos=packet_qos
        self.source_id=int(source_id)
        self.destination_id=int(destination_id)
        self.time_buffer_in=-1
        self.time_buffer_out=-1
        self.time_trx_in=-1
        self.time_trx_out=-1
        self.mode=''

    def show(self):
        outp=str(self.packet_id)+','+\
             str(self.time) + ','+\
            str(self.packet_size) + ',' +\
                str(self.packet_qos) + ',' +\
                str(self.source_id) + ','+ \
                str(self.destination_id) + ','+ \
                str(self.time_buffer_in) + ',' + \
             str(self.time_buffer_out) + ',' + \
             str(self.time_trx_in) + ',' + \
             str(self.time_trx_out) + ',' + \
             str(self.mode)
        return outp
class Traffic_per_packet():
    def __init__(self,file):
        self.db=[]
        self.load(file)

    def load(self,file):
        with open(myglobal.ROOT+myglobal.TRAFFIC_DATASETS_FOLDER+file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                new_packet = Packet(row['packet_id'], row['time'], row['packet_size'],row['packet_qos'],row['source_id'],row['destination_id'])
                self.add(new_packet)

    def add(self,packet):
        self.db.append(packet)

    def get_next_arrival(self,current_time):
        for packet in self.db:
            if packet.time>=current_time:
                return packet.time

    def get_new_packets(self,current_time):
        packet_list=[]
        for packet in self.db:
            #if math.isclose(current_time,packet.time,abs_tol=myglobal.TOLERANCE): # legacy
            if packet.time<=current_time:
                packet_list.append(packet)
                #packet.time_buffer_in=current_time
                self.db.remove(packet)
            else:
                break
        return packet_list






