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
from dualmac.myglobal import *
# First run with avgg=False to check all samples (where they span)
# According to this plot-> set avgg=True and set grouping parameters to get finalized plots
# Plot label params at the end of the script (thruput-delay-overflow)

# Sampling params
avgg=False
filename= 'logs\\4nodes\\combined2022_03_14_12_54_26_649460.csv'
my_tbegin=0
my_tend=0.2
my_samples=100
# Grouping params
start_group_value=0
end_group_value=4e5
grouping_points=25

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

class My_Group:
    def __init__(self,timestep):
        self.nominal_load=None
        self.timeslots=[]
        self.timestep=timestep

    def get_stats_load_total_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_total())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)

    def get_stats_load_high_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_high())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)

    def get_stats_load_med_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_med())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)

    def get_stats_load_low_bps(self):
        mylist=[]
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_load_low())
        # bytes to bits and millisec to sec
        final_list=[((8*i)/self.timestep) for i in mylist]
        if len(final_list)==0:
            return 0, 0
        elif len(final_list)==1:
            return final_list[0],0
        else:
            return statistics.mean(final_list),statistics.stdev(final_list)

    def get_stats_thru_total_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_total())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_thru_high_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_high())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_thru_med_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_med())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_thru_low_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_thru_low())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_drop_total_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_total())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_drop_high_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_high())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_drop_med_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_med())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_drop_low_bps(self):
        mylist = []
        for tslot in self.timeslots:
            mylist.append(tslot.get_agg_drop_low())
        # bytes to bits and millisec to sec
        final_list = [((8 * i) / self.timestep) for i in mylist]
        if len(final_list) == 0:
            return 0, 0
        elif len(final_list) == 1:
            return final_list[0], 0
        else:
            return statistics.mean(final_list), statistics.stdev(final_list)

    def get_stats_drop_prob_total(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_total()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_total()/tslot.get_agg_load_total())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_drop_prob_high(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_high()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_high()/tslot.get_agg_load_high())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_drop_prob_med(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_med()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_med()/tslot.get_agg_load_med())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_drop_prob_low(self):
        mylist=[]
        for tslot in self.timeslots:
            if tslot.get_agg_load_low()==0:
                mylist.append(0)
            else:
                mylist.append(tslot.get_agg_drop_low()/tslot.get_agg_load_low())
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_delay_total(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_total()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_delay_high(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_high()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_delay_med(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_med()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_delay_low(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_delay_low()
            if res is not None:
                mylist.append(res)
        if len(mylist)==0:
            return 0,0
        elif len(mylist)==1:
            return mylist[0],0
        else:
            return statistics.mean(mylist),statistics.stdev(mylist)

    def get_stats_qdelay_total(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_total()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

    def get_stats_qdelay_high(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_high()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

    def get_stats_qdelay_med(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_med()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

    def get_stats_qdelay_low(self):
        mylist = []
        for tslot in self.timeslots:
            res=tslot.get_avg_qdelay_low()
            if res is not None:
                mylist.append(res)
        if len(mylist) == 0:
            return 0, 0
        elif len(mylist) == 1:
            return mylist[0], 0
        else:
            return statistics.mean(mylist), statistics.stdev(mylist)

class My_Group_List():
    def __init__(self,tbegin,tend,samples, start_group_value,end_group_value,grouping_points):
        self.db = []
        self.tbegin=tbegin
        self.tend=tend
        self.samples=samples
        self.start_group_value=start_group_value
        self.end_group_value=end_group_value
        self.grouping_point=grouping_points
        self.nominal_rates = np.linspace(self.start_group_value, self.end_group_value, self.grouping_point)
        print('(debug): Nominal Rates'+str(self.nominal_rates))
        timestep=(self.tend-self.tbegin)/self.samples
        for nomrate in self.nominal_rates:
            mygroup=My_Group(timestep)
            mygroup.nominal_load=nomrate
            self.db.append(mygroup)

    def find_closest(self,old_rate):
        diff = math.inf
        outvalue = None
        for nomrate in self.nominal_rates:
            if abs(old_rate - nomrate) < diff:
                diff = abs(old_rate - nomrate)
                outvalue = nomrate
        return outvalue

    def assign_timeslots_to_groups(self,timeslot_list):
        for timeslot in timeslot_list.db:
            # find closest nominal rate
            current_rate=timeslot.get_agg_load_total()
            new_rate=self.find_closest(current_rate)
            # assign timeslot to group based on previous rate
            found=False
            for group in self.db:
                if group.nominal_load==new_rate:
                    group.timeslots.append(timeslot)
                    found=True
            if not found:
                print('ERROR: Cannot assign timeslot with rate=' + str(new_rate))

    def get_groups_load_total_bps(self):
        avg_list=[]
        err_list=[]
        for gr in self.db:
            avg,err=gr.get_stats_load_total_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list,err_list

    def get_groups_load_high_bps(self):
        avg_list=[]
        err_list=[]
        for gr in self.db:
            avg,err=gr.get_stats_load_high_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list,err_list

    def get_groups_load_med_bps(self):
        avg_list=[]
        err_list=[]
        for gr in self.db:
            avg,err=gr.get_stats_load_med_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list,err_list

    def get_groups_load_low_bps(self):
        avg_list=[]
        err_list=[]
        for gr in self.db:
            avg,err=gr.get_stats_load_low_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list,err_list

    def get_groups_thru_total_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_total_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_high_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_high_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_med_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_med_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_thru_low_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_thru_low_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_total_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_total_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_high_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_high_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_med_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_med_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_low_bps(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_low_bps()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_total(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_total()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_high(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_high()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_med(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_med()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_drop_prob_low(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_drop_prob_low()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_total(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_total()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_high(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_high()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_med(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_med()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_delay_low(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_delay_low()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_total(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_total()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_high(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_high()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_med(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_med()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

    def get_groups_qdelay_low(self):
        avg_list = []
        err_list = []
        for gr in self.db:
            avg, err = gr.get_stats_qdelay_low()
            avg_list.append(avg)
            err_list.append(err)
        return avg_list, err_list

class My_Timeslot_List():
    def __init__(self,tbegin,tend,samples):
        self.db=[]
        self.tbegin=tbegin
        self.tend=tend
        self.samples=samples
        self.total_time = my_tend - my_tbegin
        self.timestep = self.total_time / samples
        tt_range = np.linspace(self.tbegin, self.tend, self.samples)
        for tt in tt_range:
            new_timeslot=My_Timeslot(tt,tt+self.timestep)
            self.db.append(new_timeslot)

    def init_with_db(self,record_db):
        for rec in record_db:
            for timeslot in self.db:
                if timeslot.t_begin <= rec.time and rec.time <= timeslot.t_end:
                    timeslot.load_total.append(rec.packet_size)
                    if rec.packet_qos=='high':
                        timeslot.load_high.append(rec.packet_size)
                    elif rec.packet_qos=='med':
                        timeslot.load_med.append(rec.packet_size)
                    elif rec.packet_qos=='low':
                        timeslot.load_low.append(rec.packet_size)

                    if rec.time_buffer_in > -1:
                        timeslot.delay_total.append(rec.time_trx_out - rec.time)
                        timeslot.qdelay_total.append(rec.time_trx_in - rec.time)
                        if rec.packet_qos == 'high':
                            timeslot.delay_high.append(rec.time_trx_out - rec.time)
                            timeslot.qdelay_high.append(rec.time_trx_in - rec.time)
                        elif rec.packet_qos == 'med':
                            timeslot.delay_med.append(rec.time_trx_out - rec.time)
                            timeslot.qdelay_med.append(rec.time_trx_in - rec.time)
                        elif rec.packet_qos == 'low':
                            timeslot.delay_low.append(rec.time_trx_out - rec.time)
                            timeslot.qdelay_low.append(rec.time_trx_in - rec.time)
                    else:
                        timeslot.drop_total.append(rec.packet_size)
                        if rec.packet_qos == 'high':
                            timeslot.drop_high.append(rec.packet_size)
                        elif rec.packet_qos == 'med':
                            timeslot.drop_med.append(rec.packet_size)
                        elif rec.packet_qos == 'low':
                            timeslot.drop_low.append(rec.packet_size)

            for timeslot in self.db:
                if timeslot.t_begin <= rec.time_trx_out and rec.time_trx_out <= timeslot.t_end:
                    timeslot.thru_total.append(rec.packet_size)
                    if rec.packet_qos == 'high':
                        timeslot.thru_high.append(rec.packet_size)
                    elif rec.packet_qos == 'med':
                        timeslot.thru_med.append(rec.packet_size)
                    elif rec.packet_qos == 'low':
                        timeslot.thru_low.append(rec.packet_size)


    def get_list_load_total(self):
        mylist=[]
        for element in self.db:
            mylist.append(element.get_agg_load_total())
        return mylist

    def get_list_thru_total(self):
        mylist=[]
        for element in self.db:
            mylist.append(element.get_agg_thru_total())
        return mylist

    def get_list_drop_total(self):
        mylist=[]
        for element in self.db:
            mylist.append(element.get_agg_drop_total())
        return mylist

class My_Timeslot():
    def __init__(self,tbegin,tend):
        self.t_begin=tbegin
        self.t_end=tend
        self.load_total=[]
        self.load_high=[]
        self.load_med= []
        self.load_low = []
        self.delay_total=[]
        self.delay_high=[]
        self.delay_med= []
        self.delay_low = []
        self.drop_total=[]
        self.drop_high=[]
        self.drop_med= []
        self.drop_low = []
        self.thru_total=[]
        self.thru_high=[]
        self.thru_med=[]
        self.thru_low=[]
        self.qdelay_total=[]
        self.qdelay_high=[]
        self.qdelay_med=[]
        self.qdelay_low=[]

    def get_agg_load_total(self):
        mytotal=0
        for el in self.load_total:
            mytotal=mytotal+el
        return mytotal

    def get_agg_load_high(self):
        mytotal=0
        for el in self.load_high:
            mytotal=mytotal+el
        return mytotal

    def get_agg_load_med(self):
        mytotal=0
        for el in self.load_med:
            mytotal=mytotal+el
        return mytotal

    def get_agg_load_low(self):
        mytotal=0
        for el in self.load_low:
            mytotal=mytotal+el
        return mytotal

    def get_agg_thru_total(self):
        mytotal=0
        for el in self.thru_total:
            mytotal=mytotal+el
        return mytotal

    def get_agg_thru_high(self):
        mytotal=0
        for el in self.thru_high:
            mytotal=mytotal+el
        return mytotal

    def get_agg_thru_med(self):
        mytotal=0
        for el in self.thru_med:
            mytotal=mytotal+el
        return mytotal

    def get_agg_thru_low(self):
        mytotal=0
        for el in self.thru_low:
            mytotal=mytotal+el
        return mytotal

    def get_agg_drop_total(self):
        mytotal=0
        for el in self.drop_total:
            mytotal=mytotal+el
        return mytotal

    def get_agg_drop_high(self):
        mytotal=0
        for el in self.drop_high:
            mytotal=mytotal+el
        return mytotal

    def get_agg_drop_med(self):
        mytotal=0
        for el in self.drop_med:
            mytotal=mytotal+el
        return mytotal

    def get_agg_drop_low(self):
        mytotal=0
        for el in self.drop_low:
            mytotal=mytotal+el
        return mytotal

    def get_avg_delay_total(self):
        mytotal=0
        N=0
        for el in self.delay_total:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None

    def get_avg_delay_high(self):
        mytotal=0
        N=0
        for el in self.delay_high:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None

    def get_avg_delay_med(self):
        mytotal=0
        N=0
        for el in self.delay_med:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None

    def get_avg_delay_low(self):
        mytotal=0
        N=0
        for el in self.delay_low:
            mytotal=mytotal+el
            N=N+1
        if N>0:
            return mytotal/N
        else:
            return None

    def get_avg_qdelay_total(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_total:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None

    def get_avg_qdelay_high(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_high:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None

    def get_avg_qdelay_med(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_med:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None

    def get_avg_qdelay_low(self):
        mytotal = 0
        N = 0
        for el in self.qdelay_low:
            mytotal = mytotal + el
            N = N + 1
        if N > 0:
            return mytotal / N
        else:
            return None

my_db=[]
with open(filename) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        new_rec=Record(row['packet_id'],row['time'],row['packet_size'],
                       row['packet_qos'], row['source_id'], row['destination_id'],
                       row['time_buffer_in'], row['time_buffer_out'],
                       row['time_trx_in'],row['time_trx_out'],row['mode'] )
        my_db.append(new_rec)

timeslot_list=My_Timeslot_List(my_tbegin,my_tend,my_samples)
timeslot_list.init_with_db(my_db)

if not avgg:
    LOAD=timeslot_list.get_list_drop_total()
    THRU=timeslot_list.get_list_thru_total()
    DROP=timeslot_list.get_list_drop_total()
    print(str(LOAD))
    print(str(THRU))
    print(str(DROP))
    plt.plot(LOAD,THRU,'o', label = "thru")
    plt.plot(LOAD, DROP,'o', label = "drop")
    plt.xlabel('Load (bytes per sec)', fontsize=25)
    plt.ylabel('Bits per sec', fontsize=25)
    plt.grid(True, which='major', axis='both')
    plt.title('Here is the title', fontsize=25)
    plt.legend()
    plt.show()
else: #Group stage
    group_list = My_Group_List(my_tbegin,my_tend,my_samples,start_group_value, end_group_value, grouping_points)
    group_list.assign_timeslots_to_groups(timeslot_list)


    avg,err=group_list.get_groups_load_total_bps()
    prLOAD_BIT=avg
    print('get_groups_load_total_bps' + '(avg)='+str(avg))
    print('get_groups_load_total_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_load_high_bps()
    print('get_groups_load_high_bps' + '(avg)='+str(avg))
    print('get_groups_load_high_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_load_med_bps()
    print('get_groups_load_med_bps' + '(avg)='+str(avg))
    print('get_groups_load_med_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_load_low_bps()
    print('get_groups_load_low_bps' + '(avg)='+str(avg))
    print('get_groups_load_low_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_thru_total_bps()
    prTHRU_BIT=avg
    print('get_groups_thru_total_bps' + '(avg)='+str(avg))
    print('get_groups_thru_total_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_thru_high_bps()
    print('get_groups_thru_high_bps' + '(avg)='+str(avg))
    print('get_groups_thru_high_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_thru_med_bps()
    print('get_groups_thru_med_bps' + '(avg)='+str(avg))
    print('get_groups_thru_med_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_thru_low_bps()
    print('get_groups_thru_low_bps' + '(avg)='+str(avg))
    print('get_groups_thru_low_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_drop_total_bps()
    prDROP_BIT=avg
    print('get_groups_drop_total_bps' + '(avg)='+str(avg))
    print('get_groups_drop_total_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_drop_high_bps()
    print('get_groups_drop_high_bps' + '(avg)='+str(avg))
    print('get_groups_drop_high_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_drop_med_bps()
    print('get_groups_drop_med_bps' + '(avg)='+str(avg))
    print('get_groups_drop_med_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_drop_low_bps()
    print('get_groups_drop_low_bps' + '(avg)='+str(avg))
    print('get_groups_drop_low_bps' + '(err)='+str(err))
    avg,err=group_list.get_groups_drop_prob_total()
    print('get_groups_drop_prob_total' + '(avg)='+str(avg))
    print('get_groups_drop_prob_total' + '(err)='+str(err))
    avg,err=group_list.get_groups_drop_prob_high()
    print('get_groups_drop_prob_high' + '(avg)='+str(avg))
    print('get_groups_drop_prob_high' + '(err)='+str(err))
    avg,err=group_list.get_groups_drop_prob_med()
    print('get_groups_drop_prob_med' + '(avg)='+str(avg))
    print('get_groups_drop_prob_med' + '(err)='+str(err))
    avg,err=group_list.get_groups_drop_prob_low()
    print('get_groups_drop_prob_low' + '(avg)='+str(avg))
    print('get_groups_drop_prob_low' + '(err)='+str(err))
    avg,err=group_list.get_groups_delay_total()
    print('get_groups_delay_total' + '(avg)='+str(avg))
    print('get_groups_delay_total' + '(err)='+str(err))
    avg,err=group_list.get_groups_delay_high()
    print('get_groups_delay_high' + '(avg)='+str(avg))
    print('get_groups_delay_high' + '(err)='+str(err))
    avg,err=group_list.get_groups_delay_med()
    print('get_groups_delay_med' + '(avg)='+str(avg))
    print('get_groups_delay_med' + '(err)='+str(err))
    avg,err=group_list.get_groups_delay_low()
    print('get_groups_delay_low' + '(avg)='+str(avg))
    print('get_groups_delay_low' + '(err)='+str(err))
    avg,err=group_list.get_groups_qdelay_total()
    print('get_groups_qdelay_total' + '(avg)='+str(avg))
    print('get_groups_qdelay_total' + '(err)='+str(err))
    avg,err=group_list.get_groups_qdelay_high()
    print('get_groups_qdelay_high' + '(avg)='+str(avg))
    print('get_groups_qdelay_high' + '(err)='+str(err))
    avg,err=group_list.get_groups_qdelay_med()
    print('get_groups_qdelay_med' + '(avg)='+str(avg))
    print('get_groups_qdelay_med' + '(err)='+str(err))
    avg,err=group_list.get_groups_qdelay_low()
    print('get_groups_qdelay_low' + '(avg)='+str(avg))
    print('get_groups_qdelay_low' + '(err)='+str(err))

    plt.plot(prLOAD_BIT, prTHRU_BIT, label="thruput bitrate")
    plt.plot(prLOAD_BIT,prDROP_BIT,  label="drop bitrate")
    plt.xlabel('Load (bps)', fontsize=25)
    plt.ylabel('Probability', fontsize=25)
    plt.grid(True, which='major', axis='both')
    plt.title('Both Waiting and Prop Delay', fontsize=25)
    plt.legend()
    plt.show()
