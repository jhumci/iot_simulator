import simpy
import logging
import mqtt
import time
import numpy as np
import json

# A recipe that describes the mixture and number of bottles to be filled
class Recipe(object):
  def __init__(self, color_levels_grams, date, number):
    self.color_levels_grams = color_levels_grams
    self.date = date
    self.number = number

  def start_iot_message(self):
    return '{{"recipe": "{}", "time" : {}, "color_levels_grams" : {}}}'.format(self.date, int(time.time()), json.dumps(self.color_levels_grams))
#%%



#%%
class Bottle(object):
    def __init__(self, env, id, recipe, dispensers, mqtt_client):
        self.env = env
        self.dispensers = dispensers
        self.id = id
        self.recipe = recipe
        #self.action = env.process(self.run(dispensers,env))
        self.color_levels_grams = dict.fromkeys(recipe.color_levels_grams, 0)
        self.mqtt_client = mqtt_client
        # make 1 in 42 bottles randomly cracked using numpy
        self.is_cracked = np.random.choice(["1", "0"], p=[1/42, 41/42])
        self.drop_vibration = ["{:.10f}".format(num) for num in self.drop_vibration()]

    def drop_vibration(self):
      """make a vibration signal which i 0.2 seconds long and has a f
       different pattern (harmonic) for cracked and uncracked bottles
       also make it a litte random for each bottle"""
      if self.is_cracked:
          # make it a high frequency sinus signal with a little noise
          #return np.random.normal(100, 10, 1) + np.random.normal(100, 10, 0.1)
          # make it an harminic signal
          return np.sin(2 * np.pi * 100 * np.linspace(0, 0.2, 100)) + np.sin(2 * np.pi * 200 * np.linspace(0, 0.2, 100)) + np.sin(2 * np.pi * 300 * np.linspace(0, 0.2, 100) + np.sin(2 * np.pi * 400 * np.linspace(0, 0.2, 100)))
      else:
          # make it a low frequency sinus signal with a little noise
          return np.sin(2 * np.pi * 100 * np.linspace(0, 0.2, 100)) + np.sin(2 * np.pi * 200 * np.linspace(0, 0.2, 100)) + np.sin(2 * np.pi * 300 * np.linspace(0, 0.2, 100))
       
              


    def final_iot_message(self,env):
      return '{{"bottle": "{}", "time" : {}, "final_weight" : {}}}'.format(self.id, int(time.time()) , self.color_levels_grams[self.dispensers[0].color] + self.color_levels_grams[self.dispensers[1].color] + self.color_levels_grams[self.dispensers[2].color])

    def drop_iot_message(self,env):
      return '{{"bottle": "{}", "drop_vibration" : {}}}'.format(self.id, json.dumps(self.drop_vibration))

    def ground_truth(self,env):
      return '{{"bottle": "{}", "is_cracked" : {}}}'.format(self.id, json.dumps(self.is_cracked))

    def run(self, dispensers, env):

        # Conveyor or first dispenser

        for dispenser in dispensers:
            request = dispenser.res.request()
            yield request
            yield self.env.process(dispenser.fill(self))
            yield dispenser.res.release(request) 

            #print('Moving bottle to geht weight \n')

        print('T={}s: Bottle {} is finished There are {}g in there.'.format(self.env.now, self.id, self.color_levels_grams[dispensers[0].color] + self.color_levels_grams[dispensers[1].color] + self.color_levels_grams[dispensers[2].color]))
        logging.info(self.final_iot_message(env))
        self.mqtt_client.publish_payload("iot1/teaching_factory/scale/final_weight", self.final_iot_message(self.env))
        self.mqtt_client.publish_payload("iot1/teaching_factory/drop_vibration", self.drop_iot_message(self.env))
        self.mqtt_client.publish_payload("iot1/teaching_factory/ground_truth", self.ground_truth(self.env))   
