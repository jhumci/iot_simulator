# %% Simulation Parameters

TIME_FACTOR = 1   # Time to till one gram of peletts
TIME_MOVEMENT = 2 # Time to move between stations
TIME_FOR_SLOWEST_STATION = 20 # Time for the station all others have to wait for
THRESHOLD = 40 # Refill Threshold for dispensers
MAXIMUM_DISPENCER_SIZE_G = 800 # Refill Threshold for dispensers
SIGMA_FILLING_ERROR = 0.3 
FILLING_ERROR_SENSITIVITY_FILL_LEVEL = 0.01 # How much less is filled in if the fill level decreases

SIM_TIME = 10000
NUM_BOTTLES = 100 # Number of Bottles to run
