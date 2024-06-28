import numpy as np

def dispenser_control(env, dispensers, threshold):
    """Periodically check the level of the dispensers and refill the level falls below a threshold."""
    while True:
      for dispenser in dispensers:
        if dispenser.fill_level_grams < threshold:
            # We need to call the tank truck now!
            print("T= {}s: Refilling dispenser {} now!".format(env.now, dispenser.color))
            # Wait for the tank truck to arrive and refuel the station
            yield env.timeout(100)
            dispenser.fill_level_grams = dispenser.max_size_g

        yield env.timeout(10)  # Check every 10 seconds

