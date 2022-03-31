import sys

from engine import Engine
from network import Network

class Simulator(Engine):
    def __init__(self, scenario: str, kwargs={}):
        super().__init__(kwargs)
        self._networks = [ Network(scenario, protocol) for protocol in list(map(int, Network.Protocol)) ]
        
    def render(self, lax, rax):
        for network in self._networks:
            network.render(lax) # draws the network 
            
        # plots the statistics of the simulation
        # range(10, 100, 10)
        # x, y = [], []
        # for k in range(1, 20):
        #     x.append(int(k))
        #     y.append(s)
        # plt.plot(x, y)
        # plt.show() 
            
        #TODO statistic avec rax pour tous les networks
    
    def update(self, tick: int, load: int):
        """ Updates the simulation.

        Args:
            tick (int): The current cycle of the simulation.
        """
        for network in self._networks:
            network.update(tick, load)

    def clear(self):
        for network in self._networks:
            network.clear()

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
