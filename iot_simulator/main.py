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

print("Connecting to MQTT Broker")
mqtt_client_handler = MqttClientHandler("IoT-Simulator",mqtt_credentials.MQTT_BROKER, mqtt_credentials.MQTT_PORT)
print("Connected to MQTT Broker")

# %%
def setup_unlimited(env, recipe, mqtt_client_handler):
  bottle_counter = 1
  # Send the Recipe to the MQTT Broker
  
  mqtt_client_handler.publish_payload(config.TOPIC_PREFIX + "recipe", recipe.start_iot_message(), retain=True)


  while True:
    bottle_id = str(int(time.time()))[-8:]
    bottle = Bottle(env,bottle_id, recipe, dispensers, mqtt_client_handler)
    env.process(bottle.run(dispensers, env))
    yield env.timeout(2)    
    print("Bottle {} created at {}".format(bottle_counter,env.now))
    bottle_counter = bottle_counter +1 


if __name__ == "__main__":
  print("This is the main file")
  # %% Define the Environment
  env = simpy.rt.RealtimeEnvironment(factor=1, strict=False)

  red = np.random.randint(0,30)
  blue = np.random.randint(0,30)
  green = np.random.randint(0,30)

  today = time.strftime("%Y-%m-%d")
  id = int(time.time())%42

  recipe_1 = Recipe({"red":red, "blue":blue, "green":green}, id,today)

  # %% Define the dispensers in the factory
  dispenser_1 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "red", config.MAXIMUM_DISPENCER_SIZE_G, mqtt_client_handler)
  dispenser_2 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "blue", config.MAXIMUM_DISPENCER_SIZE_G, mqtt_client_handler)
  dispenser_3 = dispenser(env, config.MAXIMUM_DISPENCER_SIZE_G, "green", config.MAXIMUM_DISPENCER_SIZE_G, mqtt_client_handler)

  dispensers = [dispenser_1, dispenser_2, dispenser_3]

  # Start the process that continuously checks the current fill level of the dispensers
  env.process(dispenser_control(env, dispensers, config.THRESHOLD))

  # Start the process that creates new bottles
  env.process(setup_unlimited(env, recipe_1, mqtt_client_handler))

  # Run the simulation
  env.run(until=10000)

  print("Simulation finished at {}".format(env.now))