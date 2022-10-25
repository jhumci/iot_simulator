import simpy
import logging
import mqtt

# A recipe that describes the mixture and number of bottles to be filled
class Recipe(object):
  def __init__(self, color_levels_grams, date, number):
    self.color_levels_grams = color_levels_grams
    self.date = date
    self.number = number
#%%



#%%
class Bottle(object):
    def __init__(self, env, id, recipe, dispensers, mqtt_client):
        self.env = env
        self.dispensers = dispensers
        self.id = id
        self.recipe = recipe
        self.action = env.process(self.run(dispensers,env))
        self.color_levels_grams = dict.fromkeys(recipe.color_levels_grams, 0)
        self.mqtt_client = mqtt_client

    def final_iot_message(self,env):
      return '{{"bottle": "{}", "time" : {}, "final_weight" : {}}}'.format(self.id, env.now, self.color_levels_grams[self.dispensers[0].color] + self.color_levels_grams[self.dispensers[1].color] + self.color_levels_grams[self.dispensers[2].color])


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
        self.mqtt_client.publish_payload("final_weight", self.final_iot_message(self.env))
   
