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
from polydiavlika.myglobal import *
trafficc='big'
avgg=True
if trafficc=='big':
    filename='C:\\Pycharm\\Projects\\polydiavlika\\polydiavlika\\last_noprop_wait.csv'
elif trafficc=='small':
    filename = 'C:\\Pycharm\\Projects\\polydiavlika\\polydiavlika\\fast_1e9.csv'

class My_Group:
    def __init__(self,timestep):
        self.load_rate=None
        self.load=[]
        self.thru=[]
        self.drop=[]
        self.delay=[]
        self.dropprop=[]
        self.ro=[]
        self.ro_thru=[]
        self.ro_drop = []
        self.timestep=timestep
        self.byterate1=1e10/8 #bytes per sec for ro=1, ro(x)=Byterate(1)/(Byterate(x)*ro(1))=byterate(x)/byterate(1)

    def calc_ro_drop(self):
        total=0
        N=0
        for i in self.drop:
            total=total+i
            N=N+1
        if N>0:
            avg=total/N
            byteratex=avg/self.timestep
            ro=byteratex/self.byterate1
            return ro
        else:
            return 0

    def calc_ro_thru(self):
        total=0
        N=0
        for i in self.thru:
            total=total+i
            N=N+1
        if N>0:
            avg=total/N
            byteratex=avg/self.timestep
            ro=byteratex/self.byterate1
            return ro
        else:
            return 0

    def calc_ro(self):
        total=0
        N=0
        for i in self.load:
            total=total+i
            N=N+1
        if N>0:
            avg=total/N
            byteratex=avg/self.timestep
            ro=byteratex/self.byterate1
            return ro
        else:
            return 0

    def calc_avgload2(self):
        return self.load_rate/self.byterate1

    def calc_avgload(self):
        total=0
        N=0
        for i in self.load:
            total=total+i
            N=N+1
        if N>0:
            return total/N
        else:
            return 0

    def calc_dropprop(self):
        total=0
        N=0
        for i in self.dropprop:
            total=total+i
            N=N+1
        if N>0:
            return total/N
        else:
            return 0
    def calc_delay(self):
        total=0
        N=0
        for i in self.delay:
            total=total+i
            N=N+1
        if N>0:
            return total/N
        else:
            return 0

    def calc_thru(self):
        total=0
        N=0
        for i in self.thru:
            total=total+i
            N=N+1
        if N>0:
            return total/N
        else:
            return 0

    def calc_drop(self):
        total=0
        N=0
        for i in self.drop:
            total=total+i
            N=N+1
        if N>0:
            return total/N
        else:
            return 0
class Record():
    def __init__(self,packet_id,time,size,qos,source_id,
                 destination_id,time_buffer_in,time_buffer_out,
                 time_trx_in,time_trx_out,mode):
        self.packet_id=int(packet_id)
        self.time=float(time)
        self.packet_size=float(size)
        self.packet_qos=qos
        self.source_id=int(source_id)
        self.destination_id = int(destination_id)
        self.time_buffer_in=float(time_buffer_in)
        self.time_buffer_out =float(time_buffer_out)
        self.time_trx_in =float(time_trx_in)
        self.time_trx_out =float(time_trx_out)
        self.plot_time=0
        self.mode=mode

class My_Timeslot():
    def __init__(self,tbegin,tend):
        self.t_begin=tbegin
        self.t_end=tend
        self.load=0
        self.loaded=0
        self.delay=0
        self.delayed=0
        self.drop=0
        self.dropped=0
        self.thru=0
        self.thrud=0

def find_closest(element,list_of_things):
    diff=math.inf
    outvalue=None
    for thing in list_of_things:
        if abs(element-thing)<diff:
            diff=abs(element-thing)
            outvalue=thing
    return outvalue


db=[]
with open(filename) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        new_rec=Record(row['packet_id'],row['time'],row['packet_size'],
                       row['packet_qos'], row['source_id'], row['destination_id'],
                       row['time_buffer_in'], row['time_buffer_out'],
                       row['time_trx_in'],row['time_trx_out'],row['mode'] )
        db.append(new_rec)

my_tbegin=0
my_tend=0.008
samples=100
tbegin_range=np.linspace(my_tbegin, my_tend, samples)
list_of_new_dbs=[]
total_load=0
total_time=my_tend-my_tbegin
timestep=total_time/samples

timeslot_list=[]
for tbegin in tbegin_range:
    new_timeslot=My_Timeslot(tbegin,tbegin+timestep)
    timeslot_list.append(new_timeslot)

for rec in db:
    for timeslot in timeslot_list:
        if timeslot.t_begin<=rec.time and rec.time<=timeslot.t_end:
            timeslot.load=timeslot.load+rec.packet_size
            timeslot.loaded=timeslot.loaded+1
            if rec.time_buffer_in>-1:
                pass
            else:
                timeslot.drop=timeslot.drop+rec.packet_size
                timeslot.dropped=timeslot.dropped+1

    for timeslot in timeslot_list:
        if timeslot.t_begin <= rec.time_trx_out and rec.time_trx_out <= timeslot.t_end:
            timeslot.thru = timeslot.thru + rec.packet_size
            timeslot.thrud = timeslot.thrud + 1
            timeslot.delay=timeslot.delay+(rec.time_trx_out-rec.time)
            timeslot.delayed=timeslot.delayed+1
LOAD=[]
THRU=[]
DROP=[]
DELAY=[]

for timeslot in timeslot_list:
    LOAD.append(timeslot.load)
    THRU.append(timeslot.thru)
    DROP.append(timeslot.drop)
    DELAY.append(timeslot.delay/timeslot.delayed)

#Group stage
rates=[0.5e5,1e5,1.5e5,2*1e5,2.5e5,3*1e5,3.5e5]
rates=[0.25e5,0.5e5,1e5,1.25*1e5,1.5e5,1.74*1e5]
rates=[0,0.5e4,1e4,1.5e5,2e5,2.5e5,3e5,3.5e5]
#rates=[0*1e5,1*1e5,2*1e5,3*1e5,4*1e5,5*1e5,6*1e5]
#rates=[0*1e6,0.5*1e6,1*1e6,1.5*1e6,2*1e6]
#rates=[0*1e7,0.25*1e7,0.5*1e7,1*1e7,1.5*1e7,2*1e7,2.5*1e7]
#rates=[0*1e6,0.5*1e6,1*1e6,1.5*1e6,2*1e6,2.5*1e6,3e6,3.5e6,4e6]
#rates=[0*1e6,0.5*1e6,1*1e6,1.5*1e6,2*1e6]

mygroup_list=[]
for i in rates:
    mygroup=My_Group(timestep)
    mygroup.load_rate=i
    mygroup_list.append(mygroup)

for idx in range(0,len(LOAD)):
    myrate=LOAD[idx]
    my_new_rate=find_closest(myrate,rates)
    found = False
    for gr in mygroup_list:
        if gr.load_rate==my_new_rate:
            found=True
            gr.load.append(LOAD[idx])
            gr.thru.append(THRU[idx])
            gr.drop.append(DROP[idx])
            gr.delay.append(DELAY[idx])
            if LOAD[idx]==0:
                gr.dropprop.append(0)
            else:
                gr.dropprop.append(DROP[idx]/LOAD[idx])
            break

prLOAD=[]
prTHRU=[]
prDROP=[]
prDELAY=[]
prDROPPROP=[]
prRO=[]
prRO_THRU=[]
prRO_DROP=[]
for gr in mygroup_list:
    prLOAD.append(gr.calc_avgload())
    prTHRU.append(gr.calc_thru())
    prDROP.append(gr.calc_drop())
    prDELAY.append(gr.calc_delay())
    prDROPPROP.append(gr.calc_dropprop())
    prRO.append(gr.calc_ro())
    prRO_THRU.append(gr.calc_ro_thru())
    prRO_DROP.append(gr.calc_ro_drop())

if avgg:
    #plt.plot(prLOAD,prTHRU, label = "thru")
    #plt.plot(prLOAD, prDROP, label = "drop")
    #plt.plot(prRO, prDELAY, label="delay")
    plt.plot(prRO, prDROPPROP, label="drop probability")
    #plt.plot(prTHRU, prDELAY, label="delay")
    #plt.plot(prRO, prRO_THRU,label="thruput")
    #plt.plot(prRO, prRO_DROP, label = "drop")
    #plt.xlabel('Load (bytes per sec)', fontsize=25)
    #plt.xlabel('Thruput (bytes per sec)', fontsize=25)
    #plt.ylabel('Bytes per sec', fontsize=25)
    #plt.ylabel('Sec', fontsize=25)
    #plt.ylabel('Probability', fontsize=25)
    plt.grid(True, which='major', axis='both')
    plt.title('Propagation delay=0, Waiting delay>0', fontsize=25)
    plt.legend()
    plt.show()
else:
    plt.plot(LOAD,THRU,'o', label = "thru")
    plt.plot(LOAD, DROP,'o', label = "drop")
    #plt.plot(LOAD, DELAY, 'o', label="delay")
    plt.xlabel('Load (bytes per sec)', fontsize=25)
    plt.ylabel('Bytes per sec', fontsize=25)
    plt.grid(True, which='major', axis='both')
    plt.title('Propagation delay>0, Waiting delay=0', fontsize=25)
    plt.legend()
    plt.show()