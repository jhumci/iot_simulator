#%%

#!pip install simpy
import simpy

TIME_FACTOR = 1   # Time to till one gram of peletts
TIME_MOVEMENT = 2 # Time to move between stations

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
    if self.fill_level_grams > amount_grams:
      self.fill_level_grams = self.fill_level_grams - amount_grams
    else:
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
    #yield self.env.process(dispenser_1.fill(bottle.recipe.color_levels_grams[dispenser_1.color] )) & self.env.process(dispenser_2.fill(bottle.recipe.color_levels_grams[dispenser_1.color] )) & self.env.process(dispenser_3.fill(bottle.recipe.color_levels_grams[dispenser_2.color] ))
    # here we must way for all other dispensers
    yield  env.timeout(20)

class conveyor(object):
    def __init__(self,time_between_stations_s):
        self.env = env
        self.res = simpy.Resource(env, capacity=1)
        self.time_between_stations_s = time_between_stations_s

    def run():
        yield env.timeout(self.time_between_stations_s) 

#%%
class Bottle(object):
    def __init__(self, env, id, recipe):
        self.env = env
        self.action = env.process(self.run())
        self.color_levels_grams = dict.fromkeys(recipe.color_levels_grams, 0)
        self.id = id
        self.recipe = recipe


    def run(self):

        # Conveyor or first dispenser
        #yield env.timeout(TIME_MOVEMENT)

        request = dispenser_1.res.request()
        yield request
        yield self.env.process(dispenser_1.fill(self))
        yield dispenser_1.res.release(request) 
  
      
        
        #print('Moving to next station \n')
        #yield env.timeout(TIME_MOVEMENT)


        # Bottle blocks second dispenser
        request = dispenser_2.res.request()
        yield request
        yield self.env.process(dispenser_2.fill(self))
        yield dispenser_2.res.release(request) 
     
        #print('Moving to next station \n')
        #yield env.timeout(TIME_MOVEMENT)



        # Bottle blocks third dispenser
        request = dispenser_3.res.request()
        yield request
        yield self.env.process(dispenser_3.fill(self))
        yield dispenser_3.res.release(request) 
       
        #print('Moving bottle to geht weight \n')
        #yield env.timeout(TIME_MOVEMENT)
        print('T={}s: Bottle {} is finished There are {}g in there.'.format(self.env.now, self.id, self.color_levels_grams[dispenser_1.color] + self.color_levels_grams[dispenser_2.color] + self.color_levels_grams[dispenser_3.color]))
  


# %%
def setup(env, num_bottles, recipe):
  for i in range(num_bottles):
    bottle = Bottle(env,i, recipe)
    #env.process(bottle.run())
  yield env.timeout(0)

# %%
env = simpy.Environment()

recipe_1 = Recipe({"red":10,"blue":20,"green":15},2022,20)

# %%

dispenser_1 = dispenser(env, 100, "red")
dispenser_2 = dispenser(env, 100, "blue")
dispenser_3 = dispenser(env, 100, "green")

# %%

env.process(setup(env, num_bottles = 2, recipe = recipe_1))
env.run()

# %%