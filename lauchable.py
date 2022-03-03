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