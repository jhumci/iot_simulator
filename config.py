# %% Simulation Parameters

TIME_FACTOR = 1   # Time to till one gram of peletts
TIME_MOVEMENT = 2 # Time to move between stations
TIME_FOR_SLOWEST_STATION = 20 # Time for the station all others have to wait for
THRESHOLD = 40 # Refill Threshold for dispensers
MAXIMUM_DISPENCER_SIZE_G = 200 # Refill Threshold for dispensers
SIGMA_FILLING_ERROR = 0.3 
SIM_TIME = 10000
NUM_BOTTLES = 100 # Number of Bottles to run


MQTT_BROKER = 'd0b3cc94d52d409a920e09f9cb9f7050.s1.eu.hivemq.cloud' # eg. choosen-name-xxxx.cedalo.cloud
MQTT_PORT = 8883

MQTT_USER = "123456!pass"
MQTT_PASSWORD = "123456!pass"