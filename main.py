#!/usr/bin/python

import sys, time
import matplotlib.pyplot as plt
import numpy.random as random

from engine import Engine
from network import Network




class Simulator(Engine):
    def __init__(self, kwargs):
        super().__init__(kwargs['maximum_tick'] if kwargs['maximum_tick'] else 0)
        
        self.network = Network([], [])
        self.package_size = 100
        self.normal_loc = 50.0
        self.normal_scale = 2.0
        pass
    
    def update(self, tick):
        pass
    
    # package_size = 100
    # normal_loc = 50.0
    # normal_scale = 2.0
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



# OLSR / AODV


    
    
    # class Node():
    #     def __init__(self, name):
    #         """_summary_

    #         Args:
    #             name (string): the name of the node.
    #         """
    #         self.name = name
    #         self.packages_in = [] # file de paquet arrivé
    #         self.packages_out = [] # file fifo paquet au départ

    #     def pre_update(self):
    #         self.packages_out.extend(self.packages_in)
    #         self.packages_in = []
            
    #     def post_update(self):
    #         # scheduler prend un 
    #         # random entre 0 et max
    #         # package cycle_arrive + 1
    #         # on move envoie > reception
    #         pass
            
    # class Route():
    #     def __init__(self, node_source, node_destination, route_throughput):
    #         self.maximum_throughput = route_throughput
    #         self.node_source = node_source
    #         self.node_destination = node_destination
        
    #     def update(self):
    #         self.current_throughput = random.randint(0, self.maximum_throughput + 1)
        
    
    # def __init__(self):
    #     self.nodes = [] # routeurs

    # def add_traffic(node_source, node_destination):
    #     pass
    
    # def add_node(self, node_name, routes): # routes list of tuple (network_node_name, network_route_throughput)
    #     for (node, throughput) in routes:
    #         if node in self.nodes:
    #             self.add_route(node_name, node, throughput)
    #     pass
    
    # def add_route(self, nodeA, nodeB, debit):
    #     node_destination = {nodeB: debit}
    #     self.nodes[nodeA].extend(node_destination)
    #     pass
    
    # def update(self, tick):
    #     for node in self.nodes:
    #         node.pre_update()

    #     for node in self.nodes:
    #         node.post_update()
        
    # des nodes

    # source / destination
    # 










        
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


def main(argc, argv, kwargs):
    
    # parameters: 
    # nolimit 0
    # npackage mean
    # scénario
    
    print(kwargs)
    sys.exit(0)
    engine = Simulator(kwargs) 
    engine.launch()
    return 0

if __name__ == '__main__':
    kwargs = { kwarg[0]:kwarg[1] for kwarg in [ args.split('=') for args in sys.argv if args.find('=') > 0 ] }
    sys.exit(main(len(sys.argv), sys.argv, kwargs))
    

# https://plotly.com/python/network-graphs/