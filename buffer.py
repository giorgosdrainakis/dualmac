import csv
from polydiavlika import myglobal

class Buffer():
    def __init__(self,size):
        self.size=size
        self.db=[]

    def has_packets(self):
        if len(self.db)>0:
            return True

    def remove_packet(self,id):
        for pack in self.db:
            if pack.id==id:
                self.db.remove(pack)
                break

    def get_next_packet(self):
        mypacket=self.db[0]
        self.db.pop(0)
        return mypacket

    def add(self,packet,current_time):
        current_buffer_size=self.get_current_size()
        if current_buffer_size+packet.packet_size<=self.size:
            packet.time_buffer_in=current_time
            self.db.append(packet)
            #print('source '+str(packet.source_id)+'exist '+str(current_buffer_size)+',new='+str(packet.packet_size)+', tota='+str(self.size))
            return True
        else:
            #print('source ' + str(packet.source_id) + 'exist ' + str(current_buffer_size) + ',new=' + str(
                #packet.packet_size) + ', tota=' + str(self.size))
            return False #drop

    def delete_by_id(self,id):
        for element in self.db:
            if element.id==id:
                self.db.remove(element)
                break

    def encode_packet_WAA(self,pos):
        mystr = []
        if len(self.db)>pos:
            current_packet=self.db[pos]
            #todo
        else:
            for i in range(0,myglobal.WAA_packet_image_bits):
                mystr.append(-1)
            return mystr

    def get_current_size(self):
        mysize=0
        for element in self.db:
            mysize=mysize+element.packet_size
        return mysize



