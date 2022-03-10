from abc import ABC, abstractmethod

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
    def __init__(self, maximum_tick):
        self._maximum_tick = maximum_tick

    def start(self):
        tick = 0
    
        while tick <= self._maximum_tick:
            # generation par source
            # update(cycle) # package cycle_depart = cycle
            # on met les generations dans la source
            # envoie suivant politique
            # reception
            # statistique
            self.update(tick)
            tick += 1
        # generations paquets
        # simulation
        # plt.show()
    
    @abstractmethod
    def update(slef, tick):
        pass
    
    def stop(self):
        # affiche le graph
        # affiche les stats vers fichier etc..
        pass