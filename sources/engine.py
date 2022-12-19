import matplotlib.pyplot as plt

from abc import ABC, abstractmethod
from sys import stdout

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
        if 'time' in kwargs:
            self._maximum_tick = max(1, int(kwargs['time']))

    def start(self):
        plt.style.use('bmh')

        self._load = { 'start': 10, 'stop': 100, 'step': 5 }

        for load in range(self._load['start'], self._load['stop'], self._load['step']):
            tick = 0
            while self._maximum_tick == 0 or tick < self._maximum_tick:
                self.update(tick, load) # updates the simulation
                tick += 1

            # clears all in the simulation
            self.clear()

            # prints the progress bar up to 95%
            progress = load / self._load['stop']
            stdout.write("\rProgress: [{0:50s}] {1:.1f}% Complete".format('#' * int(progress * 50), progress * 100))
            stdout.flush()

        # renders the simulation and statistics
        self.render()

        # prints the progress bar at 100%
        stdout.write("\rProgress: [{0:50s}] 100.0% Complete".format('#' * 50))
        stdout.flush()
    
    @abstractmethod
    def clear(slef):
        pass
      
    @abstractmethod
    def update(slef, tick: int):
        pass
    
    @abstractmethod
    def render(slef):
        pass
    
    def stop(self):
        plt.close('all')
        