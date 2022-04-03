import sys

from engine import Engine
from network import Network
import matplotlib.pyplot as plt

class Simulator(Engine):
    def __init__(self, scenario: str, kwargs={}):
        super().__init__(kwargs)
        self._scenario = scenario
        self._networks = [ Network(in_format(scenario), protocol) for protocol in list(map(int, Network.Protocol)) ]
        
    def render(self):
        x = [ i for i in range(self._load['start'], self._load['stop'], self._load['step']) ]
        
        labels = [ 'average_delay', 'pourcentage_destination', 'buffer_occupation' ]
        for network in self._networks:
            self._fig, _ = plt.subplots(2, 2, layout='tight', figsize=(9, 7))
            
            self._fig.suptitle('Étude des métriques de routage en fonction de la charge dans un réseau 5G', fontsize=14, y=1)
            self._fig.subplots_adjust(bottom=0.3, wspace=0.5, hspace=0.1) # adjusts the subplot layout parameters
            
            axes = self._fig.axes
            axes[0].set_axis_off() # turns the x- and y-axis off
            axes[1].get_shared_x_axes().join(*axes[1:]) # share x between subplots
        
            cm = network.render(axes[0]) # renders the network in matplotlib
            
            axes[1].set_title('Délai moyen pour les utilisateurs', fontsize=12)
            axes[1].set_ylabel('y - délai moyen (en cycle)', fontsize=10)
            axes[1].plot(x, [100] * len(x), linestyle='dashed')
            
            axes[2].set_title('Pourcentage des paquets déservis', fontsize=12)
            axes[2].set_ylabel('y - paquets à destination', fontsize=10)
            
            axes[3].set_title('Taux d\'occupation des buffers', fontsize=12)
            axes[3].set_ylabel('y - occupation moyenne', fontsize=10)
        
            for i, axe in enumerate(axes[1:]): 
                ys = {}
                    
                for statistics in network.statistics_plots:
                    for k, v in statistics[labels[i]].items():
                        if not k in ys:
                            ys[k] = []
                        ys[k].append(v)

                for j, (k, y) in enumerate(ys.items()):
                    if len(ys.items()) > 2 or type(k) is tuple or i == 2:
                        if type(k) is tuple:
                            k = k[0] + ' -> ' + k[1]
                        axe.plot(x, y, label=k, color=cm(j / len(ys)))

                axe.grid(True)
                axe.legend(loc='best')
            
            self._fig.savefig(out_format(self._scenario, network.protocol.name), bbox_inches='tight', dpi=300)
            self._fig.clf() # clears the figure for the next rendering
            
    def update(self, tick: int, load: int):
        """ Updates the simulation.

        Args:
            tick (int): the current cycle of the simulation.
            load (int): the current load of the network.
        """
        for network in self._networks:
            network.update(tick, load)

    def clear(self):
        """ Clears all the buffers in the simulation.
        """
        for network in self._networks:
            network.clear()

out_format = lambda x, y: 'ressources/results/{}_{}.png'.format(x, y)
in_format = lambda x: 'ressources/dataframes/{}.csv'.format(x)

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
