#%%
import simpy
import logging
import numpy as np


#%% Load Simulation Parameters 
# TODO: Should be parameters 
import config

# %%


def dispenser_control(env, dispensers, threshold):
    """Periodically check the level of the dispensers and refill the level falls below a threshold."""
    while True:
      for dispenser in dispensers:
        if dispenser.fill_level_grams < threshold:
            # We need to call the tank truck now!
            print("T= {}s: Refilling dispenser {} now!".format(env.now, dispenser.color))
            # Wait for the tank truck to arrive and refuel the station
            yield env.timeout(100)
            dispenser.fill_level_grams = dispenser.max_size_g

        yield env.timeout(10)  # Check every 10 seconds

def trigger_emergency_stop(env, min_frequency, max_frequency):
    """Periodically stopp everything."""
    while True:
      env.process(stop_everything(env, 10,20))
      print("Something called the emergency stop!")
      wait_time = np.random.uniform(low=min_frequency, high=max_frequency)
      yield env.timeout(wait_time)  # Check every 10 seconds

# TODO: Make the other processes wait
def stop_everything(env, min_duration=10, max_duration=20):
    """Periodically stopp everything."""
    duration = np.random.uniform(low=min_duration, high=max_duration)
    print("Stopping for {}!".format(duration))
    env.timeout(duration) 
    yield env.timeout(duration) 
# %%
