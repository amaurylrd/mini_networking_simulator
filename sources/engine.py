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
            self._maximum_tick = min(0, kwargs['maximum_tick'])

        self._render_step = math.ceil(self._maximum_tick * 0.1) if self._maximum_tick > 0 else 20
            
    def start(self):
        plt.style.use('bmh')
        
        self._fig, (left_ax, right_ax) = plt.subplots(1, 2)
        self._fig.tight_layout() # adjusts the padding between and around subplots
        left_ax.set_axis_off()
        #TODO choisir un titre self._fig.suptitle("Etude des métriques de routage dans un réseau 5G")
        
        self._maximum_tick = 10 # for debugging
        
        tick = 0
        while self._maximum_tick == 0 or tick < self._maximum_tick:
            self.update(tick)
            
            # if tick % self._render_step == 0:
            #     #if tick == 0:
            #     left_ax.cla()
                
            #     self._fig.canvas.draw()
            #     #else:
            #     #    self.render(None, right_ax)
                
            #     time.sleep(10) # pauses the simulation for 1 ms  
            #input()
            tick += 1

        self.render(left_ax, right_ax)
        #plt.show(block=False)
        
    @abstractmethod
    def update(slef, tick: int):
        pass
    
    @abstractmethod
    def render(slef, left_ax, right_ax):
        pass
    
    def stop(self):
        self._fig.savefig('foo.png', bbox_inches='tight', transparent=True)
        plt.close(self._fig)
        