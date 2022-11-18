#%% TODO:
# - add lichtschranke
# - add conveyor belt
# - add randomness
# - add json-export
# - unimited bottle creator. 1. Start process after each bottle is created. 2. Delete Bottles 


#!pip install simpy
import simpy
import logging
import numpy as np
import time


logging.basicConfig(filename='example.log',  level=logging.INFO)

#%% Load Simulation Parameters
import config
import mqtt_credentials

#%%

from control_mechanims import dispenser_control
#from control_mechanims import trigger_emergency_stop
#from control_mechanims import stop_everything

from production_planning import Bottle
from production_planning import Recipe

from facory_parts import dispenser
# from facory_parts import Conveyor

# %%
from mqtt import MqttClient
# %%

mqtt_client = MqttClient("IoT-Simulator",mqtt_credentials.MQTT_BROKER, mqtt_credentials.MQTT_PORT)

     

# %%
def setup_limited(env, num_bottles, recipe, mqtt_client):
  for i in range(num_bottles):
    bottle = Bottle(env,i, recipe, dispensers,mqtt_client)
  yield env.timeout(0)

# %%
def setup_unlimited(env, recipe, mqtt_client):
  bottle_counter = 1
  while True:
    bottle = Bottle(env,bottle_counter, recipe, dispensers,mqtt_client)
    bottle_counter = bottle_counter +1 
  yield env.timeout(0)


# %%
#env = simpy.Environment()
env = simpy.rt.RealtimeEnvironment(factor=1, strict = False)

recipe_1 = Recipe({"red":10,"blue":20,"green":15},2022,20)

# %%

dispenser_1 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "red", config.MAXIMUM_DISPENCER_SIZE_G, mqtt_client)
dispenser_2 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "blue", config.MAXIMUM_DISPENCER_SIZE_G, mqtt_client)
dispenser_3 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "green", config.MAXIMUM_DISPENCER_SIZE_G, mqtt_client)

dispensers = [dispenser_1, dispenser_2, dispenser_3]

# %%

#conveyor = Conveyor(env, TIME_MOVEMENT)

# %%
#env.process(trigger_emergency_stop(env, 10,50))
env.process(dispenser_control(env, dispensers, config.THRESHOLD))
env.process(setup_limited(env, config.NUM_BOTTLES, recipe_1, mqtt_client))
#env.process(setup_unlimited(env, recipe_1, mqtt_client))
env.run(until=config.SIM_TIME)


# %%
