import logging
import time
import numpy as np
import json
import config

class Recipe(object):
  def __init__(self, color_levels_grams, id, creation_date):
    self.color_levels_grams = color_levels_grams
    self.number = id
    self.creation_date = creation_date

  def start_iot_message(self):
    return '{{"id": "{}", "creation_date" : {}, "color_levels_grams" : {}}}'.format(self.number, self.creation_date, json.dumps(self.color_levels_grams))

class Bottle(object):
    def __init__(self, env, id, recipe, dispensers, mqtt_client):
        self.env = env
        self.dispensers = dispensers
        self.id = id
        self.recipe = recipe
        self.color_levels_grams = dict.fromkeys(recipe.color_levels_grams, 0)
        self.mqtt_client = mqtt_client
        self.is_cracked = np.random.choice(["1", "0"], p=[config.SHARE_CRACKED, 1-config.SHARE_CRACKED])
        self.drop_oscillation = ["{:.10f}".format(num) for num in self.drop_oscillation()]

    def drop_oscillation_simple(self):
      if self.is_cracked == "1":
          return (1.3 * np.sin(2 * np.pi * 700 * np.linspace(0, 0.2, 500)) + 1.9 * np.sin(2 * np.pi * 300 * np.linspace(0, 0.2, 500) + np.sin(2 * np.pi * 400 * np.linspace(0, 0.2, 500)))) *  np.random.normal(1, 0.15, 500)
      else:
          return (np.sin(2 * np.pi * 100 * np.linspace(0, 0.2, 500)) + np.sin(2 * np.pi * 200 * np.linspace(0, 0.2, 500)) + np.sin(2 * np.pi * 300 * np.linspace(0, 0.2, 500)) + np.random.normal(0, 0.3, 500)) *  np.random.normal(1, 0.1, 500)

    def drop_oscillation(self):
      # Randomize frequencies and amplitudes for more variability
      freq1 = np.random.uniform(20, 25)  # Random frequency between 50 and 750
      freq2 = np.random.uniform(100, 100)  # Another random frequency for variety
      freq3 = np.random.uniform(50, 75)  # And a third one
      amp1 = np.random.uniform(0.5, 2.0)  # Amplitude between 0.5 and 2.0
      amp2 = np.random.uniform(0.5, 2.0)  # Another amplitude for variety
      noise_scale = np.random.uniform(0.1, 0.3)  # Scale of the normal noise
      noise_mean = np.random.choice([0, 1])  # Mean of the noise, can be 0 or 1

      if self.is_cracked == "0":
        return (amp1 * np.sin(2 * np.pi * freq1 * np.linspace(0, 0.2, 500)) + 
            amp2 * np.sin(2 * np.pi * freq2 * np.linspace(0, 0.2, 500) + 
            np.sin(2 * np.pi * freq3 * np.linspace(0, 0.2, 500)))) * np.random.normal(noise_mean, 0.15, 500)
      else:
        return (np.sin(2 * np.pi * freq1 * np.linspace(0, 0.2, 500)) + 
            np.sin(2 * np.pi * freq2 * np.linspace(0, 0.2, 500)) + 
            np.sin(2 * np.pi * freq3 * np.linspace(0, 0.2, 500)) + 
            np.random.normal(0, noise_scale, 500)) * np.random.normal(noise_mean, 0.1, 500)
      
    def final_iot_message(self):
      return '{{"bottle": "{}", "time" : {}, "final_weight" : {}}}'.format(self.id, int(time.time()) , self.color_levels_grams[self.dispensers[0].color] + self.color_levels_grams[self.dispensers[1].color] + self.color_levels_grams[self.dispensers[2].color])

    def drop_iot_message(self):
      return '{{"bottle": "{}", "drop_oscillation" : {}}}'.format(self.id, json.dumps(self.drop_oscillation))

    def ground_truth(self):
      return '{{"bottle": "{}", "is_cracked" : {}}}'.format(self.id, json.dumps(self.is_cracked))

    def run(self, dispensers, env):
        for dispenser in dispensers:
            request = dispenser.res.request()
            yield request
            yield self.env.process(dispenser.fill(self))
            yield dispenser.res.release(request) 

        logging.info(self.final_iot_message())
        self.mqtt_client.publish_payload(config.TOPIC_PREFIX + "scale/final_weight", self.final_iot_message())
        self.mqtt_client.publish_payload(config.TOPIC_PREFIX +"drop_oscillation", self.drop_iot_message())
        self.mqtt_client.publish_payload(config.TOPIC_PREFIX + "ground_truth", self.ground_truth())