
import simpy
import logging
import numpy as np
import mqtt
import time

#%% Load Simulation Parameters 
# TODO: Should be parameters 
import config


# A dispenser that holds an amount of pellets
class dispenser(object):
  def __init__(self, env, fill_level_grams,color,max_size_g, mqtt_client):
    self.env = env
    self.fill_level_grams = fill_level_grams
    self.res = simpy.Resource(env, capacity=1)
    self.color = color
    self.max_size_g = max_size_g
    self.mqtt_client = mqtt_client
    self.additional_variance = np.random.uniform(1,2) 

  def get_fill_amount(self, amount_grams):

    # If there is still something in there
    if self.fill_level_grams > amount_grams:
      # get a amount out with variation sigma
      mean_amount_grams = amount_grams+(config.FILLING_ERROR_SENSITIVITY_FILL_LEVEL*((self.fill_level_grams-self.max_size_g)/self.max_size_g))
      random_amount_grams = np.random.normal(mean_amount_grams,config.SIGMA_FILLING_ERROR,1)[0]
      self.fill_level_grams = self.fill_level_grams - random_amount_grams
      return random_amount_grams
    else:
      # geht everything out
      self.fill_level_grams = 0
      amount_grams = self.fill_level_grams
      return amount_grams

  def fill(self, bottle):


    # TODO: Add some randomness
    # Get the fill amount
    print('T={}s: Start filling bottle {} at {} dispenser'.format(self.env.now, bottle.id, self.color))
    bottle.color_levels_grams[self.color] = self.get_fill_amount(bottle.recipe.color_levels_grams[self.color])

    # TODO: Is hard coded ot take as long a the slowest dispenser
    # must be based on the mac fill time of all other stations
    # Fill with the fill amount. Takes flexible time depending on the amount
    # we must also wait for all other dispensers before we move the conveyor belt
    # yield self.env.process(dispenser_1.fill(bottle.recipe.color_levels_grams[dispenser_1.color] )) & self.env.process(dispenser_2.fill(bottle.recipe.color_levels_grams[dispenser_1.color] )) & self.env.process(dispenser_3.fill(bottle.recipe.color_levels_grams[dispenser_2.color] ))
    yield self.env.timeout(config.TIME_FOR_SLOWEST_STATION)
    logging.info(self.iot_message(self.env, bottle)) 
    self.mqtt_client.publish_payload("dispenser_" + self.color, self.iot_message(self.env, bottle))

    #yield env.timeout(self.get_fill_amount(bottle.recipe.color_levels_grams[self.color]))
    
    yield self.env.timeout(config.TIME_MOVEMENT)

  def iot_message(self,env, bottle):
    return '{{"dispenser": "{}","bottle": "{}", "time" : {}, "fill_level_grams" : {}}}'.format(self.color, bottle.id, int(time.time()), self.fill_level_grams)


class Conveyor(object):
    def __init__(self,env, time_between_stations_s):
        self.env = env
        self.res = simpy.Resource(env, capacity=1)
        self.time_between_stations_s = time_between_stations_s

    def run(self):
        yield self.env.timeout(self.time_between_stations_s) 
# %%
