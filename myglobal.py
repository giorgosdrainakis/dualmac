ROOT='C:\\Pycharm\\Projects\\polydiavlika\\dualmac\\'
TRAFFIC_DATASETS_FOLDER='traffic_datasets\\'
PROPAGATION_TIME=10/(2e8) #PROPAGATION_TIME=0 10/(2e8)
TOLERANCE = 1e-9
N_collision = 16
T_send = 1e-4
T_load = 4e-5
T_idle = (2.56)*(1e-8)+PROPAGATION_TIME
timestep = (0.8)*(1e-9) #timestep = 0.8e-9
WAITING=timestep
timeslot=(10)*(1e-9) #timeslot=(51.2)*(1e-9)
INTRA_REMOVE_INTER=True