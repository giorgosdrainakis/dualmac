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

mytype='high'
filename='qos_'+str(mytype)+'.csv'

class Record():
    def __init__(self,packet_id,time,size,qos):
        self.packet_id=int(packet_id)
        self.time=float(time)
        self.size=int(size)
        self.qos=qos
        self.plot_time=0

def get_timerange():
    ll=[]
    ll=[x/10000 for x in range(0,1000,1)]
    return ll

file=TRAFFIC_DATASETS_FOLDER+filename
db=[]
with open(file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        new_rec=Record(row['packet_id'],row['time'],row['size'], row['qos'])
        db.append(new_rec)

timerange=get_timerange()
for rec in db:
    saved_time=0
    for time in timerange:
        if rec.time>=time:
            saved_time=time
        else:
            break
    rec.plot_time=saved_time

X=timerange
Y=[]
for x in timerange:
    y=0
    for rec in db:
        if rec.plot_time==x:
            y=y+rec.size
    Y.append(y)
#    Y.append(rec.size)

plt.xlabel('Time (sec)', fontsize=20)
plt.ylabel('Data generated (Bytes)', fontsize=20)
plt.grid(True, which='major', axis='both')
plt.title('QoS:' + str(mytype))
plt.plot(X,Y)
plt.show()