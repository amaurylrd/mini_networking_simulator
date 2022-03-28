from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import math, time

class Launchable(ABC):
    def launch(self):
        self.start()
        self.stop()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class Engine(Launchable):
    def __init__(self, kwargs={}):
        self._maximum_tick = 0
        if 'maximum_tick' in kwargs:
            self._maximum_tick = min(1, int(kwargs['maximum_tick']))
            
    def start(self):
        plt.style.use('bmh')
        
        self._fig, (left_ax, right_ax) = plt.subplots(1, 2)
        self._fig.tight_layout() # adjusts the padding between and around subplots
        right_ax.set_title("Délai moyen en fonction de la charge dans un un réseau 5G", fontsize=18)
        left_ax.set_axis_off() # turns the x- and y-axis off
        
        self._maximum_tick = 10 # TODO for debugging
        
        tick = 0
        while self._maximum_tick == 0 or tick < self._maximum_tick:
            self.update(tick)
            tick += 1

        self.render(left_ax, right_ax)
        
    @abstractmethod
    def update(slef, tick: int):
        pass
    
    @abstractmethod
    def render(slef, left_ax, right_ax):
        pass
    
    def stop(self):
        self._fig.savefig('foo.png', bbox_inches='tight', transparent=True)
        plt.close(self._fig)
        