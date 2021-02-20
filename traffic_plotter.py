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
avgg=False
if trafficc=='big':
    filename='C:\\Pycharm\\Projects\\polydiavlika\\polydiavlika\\zeroBIG.csv'
elif trafficc=='small':
    filename = 'C:\\Pycharm\\Projects\\polydiavlika\\polydiavlika\\lastSMALL.csv'

class My_Group:
    def __init__(self):
        self.load_rate=None
        self.load=[]
        self.thru=[]
        self.drop=[]
        self.delay=[]
        self.dropprop=[]
        self.ro=[]
        self.ro_thru=[]
        self.ro_drop = []

    def calc_ro_drop(self):
        total=0
        N=0
        for i in self.drop:
            total=total+i
            N=N+1
        if N>0:
            return total/(N*1e7)
        else:
            return 0

    def calc_ro_thru(self):
        total=0
        N=0
        for i in self.thru:
            total=total+i
            N=N+1
        if N>0:
            return total/(N*1e7)
        else:
            return 0

    def calc_ro(self):
        total=0
        N=0
        for i in self.load:
            total=total+i
            N=N+1
        if N>0:
            return total/(N*1e7)
        else:
            return 0

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
                 time_trx_in,time_trx_out):
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

def get_timerange():
    ll=[]
    ll=[x*(4e-5) for x in range(0,2000,1)]
    return ll

def find_closest(element,list_of_things):
    diff=math.inf
    outvalue=None
    for thing in list_of_things:
        if abs(element-thing)<diff:
            diff=abs(element-thing)
            outvalue=thing
    return outvalue

file=filename
db=[]



with open(file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        new_rec=Record(row['packet_id'],row['time'],row['packet_size'],
                       row['packet_qos'], row['source_id'], row['destination_id'],
                       row['time_buffer_in'], row['time_buffer_out'],
                       row['time_trx_in'],row['time_trx_out'] )
        db.append(new_rec)

tbegin_range=np.linspace(0, 0.08, 100)
list_of_new_dbs=[]
total_load=0
total_time=0.08
timestep=0.08/100
for tbegin in tbegin_range:
    tend=tbegin+timestep
    new_db=[]
    for rec in db:
        if tbegin<=rec.time and rec.time<=tend:
            new_db.append(rec)
            total_load=total_load+rec.packet_size
    list_of_new_dbs.append(new_db)

total_load_rate=total_load/total_time
LOAD=[]
THRU=[]
DROP=[]
DELAY=[]

for new_db in list_of_new_dbs:
    load=0
    thru=0
    drop=0
    delay=0
    delay_total=0
    N=0
    for rec in new_db:
        load=load+rec.packet_size
        if rec.time_trx_out>0:
            thru=thru+rec.packet_size
            delay_total=delay_total+rec.time_trx_out-rec.time
            N=N+1
        if rec.time_buffer_in<0:
            drop=drop+rec.packet_size
    if N>0:
        delay=delay_total/N
    LOAD.append(load)
    THRU.append(thru)
    DROP.append(drop)
    DELAY.append(delay)
#Group stage
rates=[0*1e7,0.25*1e7,0.5*1e7,0.75*1e7,1*1e7,1.25*1e7]
mygroup_list=[]
for i in rates:
    mygroup=My_Group()
    mygroup.load_rate=i
    mygroup_list.append(mygroup)

for idx in range(0,len(LOAD)):
    myrate=LOAD[idx]
    my_new_rate=find_closest(myrate,rates)
    print('myrateis='+str(myrate))
    print('mynewrateis='+str(my_new_rate))
    found = False
    for gr in mygroup_list:
        print('Checking group with rate=' + str(gr.load_rate))
        if gr.load_rate==my_new_rate:
            print(str('found'))
            found=True
            print(str('adding load='+str(LOAD[idx])))
            print(str('adding THRU=' + str(THRU[idx])))
            print(str('adding DROP=' + str(DROP[idx])))
            #gr.load.append(LOAD[idx]/timestep) # old
            #gr.thru.append(THRU[idx]/timestep) # old
            #gr.drop.append(DROP[idx]/timestep) # old
            gr.load.append(LOAD[idx])
            gr.thru.append(THRU[idx])
            gr.drop.append(DROP[idx])
            gr.delay.append(DELAY[idx])
            if LOAD[idx]==0:
                gr.dropprop.append(0)
            else:
                gr.dropprop.append(DROP[idx]/LOAD[idx])
            break
    if not found:
        print(str('not found'))

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
    plt.plot(prLOAD,prTHRU, label = "thru")
    plt.plot(prLOAD, prDROP, label = "drop")
    #plt.plot(prLOAD, prDELAY, label="delay")
    #plt.plot(prLOAD, prDROPPROP, label="drop probability")
    #plt.plot(prTHRU, prDELAY, label="delay")
    #plt.plot(prRO, prRO_THRU, label="thruput")
    #plt.plot(prRO, prRO_DROP, label = "drop")
    #plt.xlabel('Load (bytes per sec)', fontsize=25)
    #plt.xlabel('Thruput (bytes per sec)', fontsize=25)
    #plt.ylabel('Bytes per sec', fontsize=25)
    #plt.ylabel('Sec', fontsize=25)
    #plt.ylabel('Probability', fontsize=25)
    plt.grid(True, which='major', axis='both')
    plt.title('Average samples KPIs for traffic='+str(trafficc) , fontsize=25)
    plt.legend()
    plt.show()
else:
    plt.plot(LOAD,THRU,'o', label = "thru")
    plt.plot(LOAD, DROP,'o', label = "delay")
    #plt.plot(LOAD, DELAY, 'o', label="delay")
    plt.xlabel('Load (bytes per sec)', fontsize=25)
    plt.ylabel('Bytes per sec', fontsize=25)
    plt.grid(True, which='major', axis='both')
    plt.title('Actual samples KPIs for traffic='+str(trafficc), fontsize=25)
    plt.legend()
    plt.show()