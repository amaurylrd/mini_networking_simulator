from asyncio import protocols
import sys

from engine import Engine
from network import Network

class Simulator(Engine):
    def __init__(self, scenario: str, kwargs={}):
        super().__init__(kwargs)
        protocols = 1
        self._networks = [ Network(scenario) ] * protocols

    def render(self, lax, rax):
        self._networks[0].render(lax)
        #TODO statistic avec rax pour tous les networks
    
    def update(self, tick: int):
        """ Updates the simulation.

        Args:
            tick (int): The current cycle of the simulation.
        """
        for network in self._networks:
            network.update(tick, None)



# OLSR / AODV


# chemin métriques
# moyenne, somme ?
# source qui interfaire avec la vraie source/destination pour contrer le meilleur débit
# bottleneck, delai, le plus court
# pathloss... contraintes basiques


# plt.savefig("numpy_random_numbers_stantard_normal_distribution.png", bbox_inches='tight')



def main(argc, argv, kwargs):
    if argc < 2:
        print("Usage: <scenario> <options*>")
        return 1
    
    engine = Simulator(argv[1], kwargs)
    engine.launch()
    return 0

if __name__ == '__main__':
    kwargs = { kwarg[0]:kwarg[1] for kwarg in [ args.split('=') for args in sys.argv if args.find('=') > 0 ] }
    sys.exit(main(len(sys.argv), sys.argv, kwargs))
    

# https://plotly.com/python/network-graphs/