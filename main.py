#%% TODO:
# - add conveyor belt
# - add randomness
# - add json-export

#!pip install simpy
import simpy
import logging
import numpy as np


logging.basicConfig(filename='example.log',  level=logging.INFO)

#%% Load Simulation Parameters
import config

#%%

from control_mechanims import dispenser_control
#from control_mechanims import trigger_emergency_stop
#from control_mechanims import stop_everything

from production_planning import Bottle
from production_planning import Recipe

from facory_parts import dispenser
# from facory_parts import Conveyor

# %%


     

# %%
def setup(env, num_bottles, recipe):
  for i in range(num_bottles):
    bottle = Bottle(env,i, recipe, dispensers)
  yield env.timeout(0)

# %%
env = simpy.Environment()

recipe_1 = Recipe({"red":10,"blue":20,"green":15},2022,20)

# %%

dispenser_1 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "red", config.MAXIMUM_DISPENCER_SIZE_G)
dispenser_2 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "blue", config.MAXIMUM_DISPENCER_SIZE_G)
dispenser_3 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "green", config.MAXIMUM_DISPENCER_SIZE_G)

dispensers = [dispenser_1, dispenser_2, dispenser_3]

# %%

#conveyor = Conveyor(env, TIME_MOVEMENT)

# %%
#env.process(trigger_emergency_stop(env, 10,50))
env.process(dispenser_control(env, dispensers, config.THRESHOLD))
env.process(setup(env, num_bottles = config.NUM_BOTTLES, recipe = recipe_1))
env.run(until=config.SIM_TIME)


# %%

# %%
