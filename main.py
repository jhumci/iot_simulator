#%%

#!pip install simpy
import simpy

TIME_FACTOR = 1   # Time to till one gram of peletts
TIME_MOVEMENT = 2 # Time to move between stations

#%%

# A recipe that describes the mixture and number of bottles to be filled
class Recipe(object):
  def __init__(self, red_grams, yellow_grams, blue_grams, date, number):
    self.red_grams = red_grams
    self.yellow_grams = yellow_grams
    self.blue_grams = blue_grams
    self.date = date
    self.number = number
#%%

# A dispencer that holds an amount of pellets
class Dispencer(object):
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

  def fill(self, amount_grams):
    yield  env.timeout(amount_grams)

#%%
class Bottle(object):
    def __init__(self, env, id, recipe):
        self.env = env
        self.action = env.process(self.run())
        self.red_grams = 0
        self.yellow_grams = 0
        self.blue_grams = 0
        self.id = id
        self.recipe = recipe

    def fill_me(self, dispencer):
        print("Got to red!")
        # Bottle blocks first dispencer
        request = dispencer.res.request()
        yield request
        print('Start filling bottle {} at {} dispenser at {}s'.format(self.id ,dispencer.color, self.env.now))

        # Get the fill amount
        self.red_grams = dispencer.get_fill_amount(self.recipe.red_grams)
        # Fill with the fill amount. Takes flexible time depending on the amount
        # we must also wait for all other dispencers before we move the conveyor belt
        yield self.env.process(dispencer_1.fill(self.recipe.red_grams)) & env.process(dispencer_2.fill(self.recipe.yellow_grams)) & env.process(dispencer_3.fill(self.recipe.blue_grams))
        # Releases if finished
        yield dispencer.res.release(request) 
        print('In bottle {} there are {} g of red'.format(self.id ,self.red_grams))
        print("Red dispenser is at: {}".format(dispencer.fill_level_grams))

    def run(self):

        # Conveyor or first dispencer
        #yield env.timeout(TIME_MOVEMENT)

        yield  self.env.process(self.fill_me(dispencer_1))

        # here we must way for all other dispencers
        print('Moving to next station \n')
        yield env.timeout(TIME_MOVEMENT)


        # Bottle blocks second dispencer
        yield  self.env.process(self.fill_me(dispencer_2))

        print('Moving to next station \n')
        yield env.timeout(TIME_MOVEMENT)



        # Bottle blocks third dispencer
        yield  self.env.process(self.fill_me(dispencer_3))

        print('Moving to geht weight \n')
        yield env.timeout(TIME_MOVEMENT)
        print('There are {}g in bottle {}.'.format(self.blue_grams + self.yellow_grams+ self.red_grams, self.id))



# %%
def setup(env, num_bottles, recipe):
  for i in range(num_bottles):
    bottle = Bottle(env,i, recipe)
    #env.process(bottle.run())
  yield env.timeout(0)

# %%
env = simpy.Environment()

recipe_1 = Recipe(10,20,15,2022,20)

# %%

dispencer_1 = Dispencer(env, 100, "red")
dispencer_2 = Dispencer(env, 100, "blue")
dispencer_3 = Dispencer(env, 100, "green")

# %%

env.process(setup(env, num_bottles = 2, recipe = recipe_1))
env.run()

# %%