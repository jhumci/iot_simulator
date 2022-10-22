#%% TODO:
# - add conveyor belt
# - add randomness
# - add json-export

#!pip install simpy
import simpy
import logging
import numpy as np


logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)

# %%

TIME_FACTOR = 1   # Time to till one gram of peletts
TIME_MOVEMENT = 2 # Time to move between stations
TIME_FOR_SLOWEST_STATION = 20 # Time for the station all others have to wait for
THRESHOLD = 40 # Refill Threshold for dispensers
MAXIMUM_DISPENCER_SIZE_G = 200 # Refill Threshold for dispensers
SIGMA_FILLING_ERROR = 0.3 
SIM_TIME = 1000
NUM_BOTTLES = 100 # Number of Bottles to run


#%%

# A recipe that describes the mixture and number of bottles to be filled
class Recipe(object):
  def __init__(self, color_levels_grams, date, number):
    self.color_levels_grams = color_levels_grams
    self.date = date
    self.number = number
#%%

# A dispenser that holds an amount of pellets
class dispenser(object):
  def __init__(self, env, fill_level_grams,color):
    self.env = env
    self.fill_level_grams = fill_level_grams
    self.res = simpy.Resource(env, capacity=1)
    self.color = color

  def get_fill_amount(self, amount_grams):

    # If there is still something in there
    if self.fill_level_grams > amount_grams:
      # get a amount out with variation sigma
      random_amount_grams = np.random.normal(amount_grams,SIGMA_FILLING_ERROR,1)[0]
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

    logging.info(self.iot_message()) 

    yield env.timeout(TIME_FOR_SLOWEST_STATION)
    #yield env.timeout(self.get_fill_amount(bottle.recipe.color_levels_grams[self.color]))
    
    yield env.timeout(TIME_MOVEMENT)
    
  def iot_message(self):
    return '{{"dispenser": {}, "time" : {}, "fill_level_grams : {}"}}'.format(self.color, env.now, self.fill_level_grams)

class Conveyor(object):
    def __init__(self,env, time_between_stations_s):
        self.env = env
        self.res = simpy.Resource(env, capacity=1)
        self.time_between_stations_s = time_between_stations_s

    def run(self):
        yield env.timeout(self.time_between_stations_s) 

#%%
class Bottle(object):
    def __init__(self, env, id, recipe):
        self.env = env
        self.action = env.process(self.run())
        self.color_levels_grams = dict.fromkeys(recipe.color_levels_grams, 0)
        self.id = id
        self.recipe = recipe

    def final_iot_message(self):
      return '{{"bottle": {}, "time" : {}, "final_weight : {}"}}'.format(self.id, env.now, self.color_levels_grams[dispenser_1.color] + self.color_levels_grams[dispenser_2.color] + self.color_levels_grams[dispenser_3.color])


    def run(self):

        # Conveyor or first dispenser

        for dispenser in dispensers:
            request = dispenser.res.request()
            yield request
            yield self.env.process(dispenser.fill(self))
            yield dispenser.res.release(request) 

            #print('Moving bottle to geht weight \n')

        print('T={}s: Bottle {} is finished There are {}g in there.'.format(self.env.now, self.id, self.color_levels_grams[dispenser_1.color] + self.color_levels_grams[dispenser_2.color] + self.color_levels_grams[dispenser_3.color]))
        logging.info(self.final_iot_message()) 


# %%

def dispenser_control(env, dispensers):
    """Periodically check the level of the dispensers and refill the level falls below a threshold."""
    while True:
      for dispenser in dispensers:
        if dispenser.fill_level_grams < THRESHOLD:
            # We need to call the tank truck now!
            print("T= {}s: Refilling dispenser {} now!".format(env.now, dispenser.color))
            # Wait for the tank truck to arrive and refuel the station
            #yield env.timeout(100)
            dispenser.fill_level_grams = MAXIMUM_DISPENCER_SIZE_G

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
def setup(env, num_bottles, recipe):
  for i in range(num_bottles):
    bottle = Bottle(env,i, recipe)
  yield env.timeout(0)

# %%
env = simpy.Environment()

recipe_1 = Recipe({"red":10,"blue":20,"green":15},2022,20)

# %%

dispenser_1 = dispenser(env, MAXIMUM_DISPENCER_SIZE_G, "red")
dispenser_2 = dispenser(env, MAXIMUM_DISPENCER_SIZE_G, "blue")
dispenser_3 = dispenser(env, MAXIMUM_DISPENCER_SIZE_G, "green")

dispensers = [dispenser_1, dispenser_2, dispenser_3]

# %%

conveyor = Conveyor(env, TIME_MOVEMENT)

# %%
#env.process(trigger_emergency_stop(env, 10,50))
env.process(dispenser_control(env, dispensers))
env.process(setup(env, num_bottles = NUM_BOTTLES, recipe = recipe_1))
env.run(until=SIM_TIME)


# %%

# %%
