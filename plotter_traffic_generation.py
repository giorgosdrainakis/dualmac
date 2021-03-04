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

node_number=1
filename='test1.csv'
t_begin=0
t_end=0.008
samples=200
class Record():
    def __init__(self,packet_id,time,size,qos, source_id, destination_id):
        self.packet_id=int(packet_id)
        self.time=float(time)
        self.size=int(size)
        self.qos=qos
        self.source_id=source_id
        self.destination_id=destination_id
        self.plot_time=-1

def get_linspace():
    return numpy.linspace(t_begin, t_end, num=samples)

file=TRAFFIC_DATASETS_FOLDER+filename
db=[]
with open(file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        new_rec=Record(row['packet_id'],row['time'],row['packet_size'], row['packet_qos'], row['source_id'], row['destination_id'])
        db.append(new_rec)


qos_list=['low','med','high']
#qos_list=['high']
timerange=get_linspace()
for rec in db:
    if rec.qos in qos_list:
        #print('Checking rec=' + str(rec.time))
        saved_time=-1
        for time in timerange:
            #print('Time=' + str(time))
            if rec.time>=time:
                saved_time=time
            else:
                pass
        rec.plot_time=saved_time
        print('R=' + str(rec.plot_time))

X=timerange
Y=[]
total=0
print(str(X))
for x in X:
    y=0
    N=0
    for rec in db:
        if math.isclose(rec.plot_time,x,abs_tol=1e-8):
            y=y+rec.size
            total=total+rec.size
            N=N+1
    Y.append(y)
    print('N '+str(N))
#    Y.append(rec.size)
print(str(total/(t_end-t_begin)))
plt.xlabel('Time (sec)', fontsize=20)
plt.ylabel('Data generated (Bytes)', fontsize=20)
plt.grid(True, which='major', axis='both')
plt.title('Node:' + str(node_number))
plt.plot(X,Y)
plt.show()