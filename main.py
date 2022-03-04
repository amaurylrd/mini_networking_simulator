#!/usr/bin/python

import sys, time
from typing import final
import matplotlib.pyplot as plt
import numpy.random as random

from lauchable import Launchable

class Engine(Launchable):
    def __init__(self):
        # init les packages graphiques (matplotlib ?)
        # gère les variables
        pass

    def start(self):
        test_loop()
        # generations paquets
        # simulation
        # plt.show()
        pass

    def stop(self):
        # affiche le graph
        # affiche les stats
        pass

class Simulator(Engine):
    def __init__(self):
        pass
    
    #package_size = 100
    #normal_loc = 50.0
    #normal_scale = 2.0
    def __generate_packages(package_size : int, normal_loc=0.0, normal_scale=1.0):
        """ Generates randomized packages from the specified parameters. 

        Args:
            package_size (int): the specified fixed size (in bits) for all packages. Must be non-negative.
            package_loc (float, optional): the mean of the gaussian distribution. Must be non-negative. Defaults to 0.0.
            package_spread (float, optional): the standard deviation of the gaussian distribution. Defaults to 1.0.

        Returns:
            out (ndarray): samples of packages from the parameterized generation.
        """
        packages = []
        normal_distribution = random.normal(normal_loc, normal_scale)
        samples = int(normal_distribution)
        
        for _ in range(samples):
            package = { "data": random.randint(0, 2, size=(package_size)) } # generate an n-dimensional array of random bits
            packages.append(package)
        
        return packages
    
    def update_simulation():
        pass
    
    def render_statistics():
        pass
    

def test_loop():
    TARGET_UPS = 60
    FIXED_DELTA_TIME = 1000 / TARGET_UPS
    MAX_ACCUMULATOR = 5 * FIXED_DELTA_TIME
    
    accumulator = 0
    cycle_starting_time = time.time_ns()
    while 1:
        current_time = time.time_ns()
        accumulator += (current_time - cycle_starting_time) / 1000000
        cycle_starting_time = current_time
        
        if (accumulator > MAX_ACCUMULATOR):
            accumulator = MAX_ACCUMULATOR
        
        while accumulator >= FIXED_DELTA_TIME:
            #self.update(DELTA_TIME)
            # update_simulation()
            print("salut")
            accumulator -= FIXED_DELTA_TIME
            
        # update_statistics

        
# Débit max = 2  W (bande passant)  log 2 V (niveau significatifs) en  bit/s
# le bruit formule SNR
# perte d'énergie du signal pendant sa propagation

# graph -> node chainé à X node

# Sujet 5

# chercher les différents algorithmes
# proposer les scénarios


# chemin métriques
# moyenne, somme ?
# source qui interfaire avec la vraie source/destination pour contrer le meilleur débit
# bottleneck, delai, le plus court
# pathloss... contraintes basiques

# loop
# update simulation cycle = 0 scheduling
# afficher simulation

# generation des sources
# tick en temps discret

# table routage / node

# statistics permanente


# plt.savefig("numpy_random_numbers_stantard_normal_distribution.png", bbox_inches='tight')
# plt.grid()


def main(argc, kwargs):
    # parameters: 
    # nolimit 0
    # npackage mean
    
    #print(kwargs)
    #test()
    engine = Simulator() # gère des variables, avec default kwargs ?
    engine.launch() # gère des variables ?
    return 0

if __name__ == '__main__':
    kwargs = { kwarg[0]:kwarg[1] for kwarg in [ args.split('=') for args in sys.argv if args.find('=') > 0 ] }
    sys.exit(main(len(sys.argv), kwargs))
    