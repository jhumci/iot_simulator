
import simpy
import logging
import numpy as np
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
    self.temperature = self.generate_temperature(int(time.time()), 10,  24 * 60 * 60, 1)



  def generate_temperature(self, unix_time, amplitude, period, noise_level):
      """
      Generates a sine-shaped temperature profile with a daily pattern based on Unix time,
      with added random noise.

      Args:
          unix_time (float or numpy array): Unix time in seconds.
          amplitude (float): Amplitude of the sine wave.
          period (float): Period of the sine wave in seconds.
          noise_level (float): Magnitude of the random noise.

      Returns:
          float or numpy array: Simulated temperature value(s) with noise.
      """
      # Convert Unix time to radians based on the period
      theta = 2 * np.pi * unix_time / period

      # Generate the sine wave
      temperature = amplitude * np.sin(theta) + 25

      # Add random noise to the temperature
      noise = np.random.normal(scale=noise_level)
      temperature += noise

      return temperature

  def get_fill_amount(self, amount_grams):

    # If there is still something in there
    if self.fill_level_grams > amount_grams:
      # get a amount out with variation sigma
      mean_amount_grams = amount_grams+(config.FILLING_ERROR_SENSITIVITY_FILL_LEVEL*((self.fill_level_grams-self.max_size_g)/self.max_size_g))
      random_amount_grams = np.random.normal(mean_amount_grams,config.SIGMA_FILLING_ERROR,1)[0]
      self.fill_level_grams = self.fill_level_grams - random_amount_grams * (self.temperature/25)/2
      return random_amount_grams
    else:
      # get everything out
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
    self.temperature = self.generate_temperature(int(time.time()), 10,  24 * 60 * 60, 1)
    logging.info(self.iot_message(self.env, bottle)) 



    self.mqtt_client.publish_payload(config.TOPIC_PREFIX + "dispenser_" + self.color, self.iot_message(self.env, bottle))
    self.mqtt_client.publish_payload(config.TOPIC_PREFIX + "temperature", self.iot_message_temp(self.env))
    #self.mqtt_client.publish_payload(config.TOPIC_PREFIX + "dispenser_" + self.color + "/vibration", self.iot_message_vibration(self.env, bottle))
    #yield env.timeout(self.get_fill_amount(bottle.recipe.color_levels_grams[self.color]))
    
    yield self.env.timeout(config.TIME_MOVEMENT)

  def compute_vibration(self, fill_amount, temperature_c, fill_level):
    return 10 + fill_amount * 10 + 2 * (20 - temperature_c) - 1 * fill_level/200


  def iot_message(self,env, bottle):
    return '{{"dispenser": "{}","bottle": "{}", "time" : {}, "fill_level_grams" : {}, "recipe" : {}, "vibration-index" : {}}}'.format(self.color, bottle.id, int(time.time()), self.fill_level_grams, bottle.recipe.number,self.compute_vibration(bottle.color_levels_grams[self.color] ,self.temperature, self.fill_level_grams))

  def iot_message_temp(self,env):
    return '{{"dispenser": "{}", "time" : {}, "temperature_C" : {}}}'.format(self.color, int(time.time()), self.temperature)

  def iot_message_vibration(self,env, bottle):
    return '{{"dispenser": "{}","bottle": "{}", "time" : {}, "vibration-index" : {}}}'.format(self.color, bottle.id, int(time.time()), )

