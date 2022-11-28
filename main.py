#%% TODO:
# - add lichtschranke
# - add conveyor belt
# - add randomness
# - add json-export
# - unimited bottle creator. 1. Start process after each bottle is created. 2. Delete Bottles 
# https://simpy.readthedocs.io/en/latest/examples/carwash.html

#!pip install simpy
import simpy
import logging
import numpy as np
import time

logging.basicConfig(filename='example.log',  level=logging.INFO)

#%% Load Simulation Parameters
import config
import mqtt_credentials


from control_mechanims import dispenser_control
from production_planning import Bottle
from production_planning import Recipe
from facory_parts import dispenser
from mqtt import MqttClientHandler

# %% Define Connection to MQTT Broker

mqtt_client_handler = MqttClientHandler("IoT-Simulator",mqtt_credentials.MQTT_BROKER, mqtt_credentials.MQTT_PORT)


# %%
def setup_unlimited(env, recipe, mqtt_client_handler):
  bottle_counter = 1
  while True:
    bottle = Bottle(env,bottle_counter, recipe, dispensers, mqtt_client_handler)
    env.process(bottle.run(dispensers, env))
    yield env.timeout(22)    
    print("Bottle {} created at {}".format(bottle_counter,env.now))
    bottle_counter = bottle_counter +1 

    if bottle_counter == 10:
      break


# %% Define the Environment

env = simpy.Environment()
#env = simpy.rt.RealtimeEnvironment(factor=1)
recipe_1 = Recipe({"red":10,"blue":20,"green":15},2022,20)

# %% Define the dispensers in the factory
# dispensers have a fill process

dispenser_1 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "red", config.MAXIMUM_DISPENCER_SIZE_G, mqtt_client_handler)
dispenser_2 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "blue", config.MAXIMUM_DISPENCER_SIZE_G, mqtt_client_handler)
dispenser_3 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "green", config.MAXIMUM_DISPENCER_SIZE_G, mqtt_client_handler)

dispensers = [dispenser_1, dispenser_2, dispenser_3]

#%%

# Starte the process, that continuously checks the current fill level of the dispensers
env.process(dispenser_control(env, dispensers, config.THRESHOLD))

# %%
# Start the process that creates new bottles
env.process(setup_unlimited(env, recipe_1, mqtt_client_handler))

# %%
# Run the simulation

env.run()

# %%
