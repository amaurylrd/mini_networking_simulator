import random

from graph import Graph

class Network(Graph):
    class Node():
        def __init__(self, node_name):
            self.name = str(node_name)
            self._packages_in = [] # packages that have just been received
            self._packages_out = [] # packages that will be sent
    
        def __eq__(self, other):
            if isinstance(other, type(self)):
                return self.name == other.name
            return False
        
        def update(self): #TODO comments
            self._packages_out.extend(self._packages_in)
            self._packages_in = []
        
        def get_packages(self, n: int):
            """ Returns the packages to be sent. Those packages are removed from the buffer.

            Args:
                n (int): The number of packages to send.

            Returns:
                out (list): The list of packages to send from this node.
            """
            return [ self._packages_out.pop(0) for _ in range(min(len(self._packages_out), n)) ]

        def set_packages(self, packages: list):
            """ Adds the specified packages at the end of the buffer.

            Args:
                packages (list): The list of received packages.
            """
            self._packages_in.extend(packages)
            
        def new_packages(self, packages: list, tick: int, destination: str):
            """ Sets the specified packages ready for send.

            Args:
                tick (int): The tick the package were sent.
                packages (list): The list of new packages to send from this node.
            """
            self._packages_out.extend([ package | { "from": self.name, "to": destination, "sent": tick } for package in packages ])
        
        def get_buffer_size(self):
            return len(self._packages_out)
        
        def is_buffer_empty(self):
            return not self._packages_out
        
        def toString(self):
            print(self.name, self._packages_in, self._packages_out)
            
    def __init__(self, routes, edges):
        """ Constructs a network mapped with the specified nodes.

        Args:
            routes (list): the list of active routes like so (<node_source>, <node_destination>).
            edges (list): the list of link in the network like so (<node_source>, <node_destination>, <maximum_throughput>).

        Raises:
            Exception: _description_ #TODO
        """
        super().__init__([ (source, destination, weight, None) for (source, destination, weight) in edges ])
        
        if routes:
            self._routes = []
            for (source, destination) in routes:
                if not (source in self._graph and destination in self._graph):
                    raise Exception("Routes must include existing nodes.")
                if source == destination:
                    raise Exception("Routes must include 2 different nodes.")
                #TODO if self.dfs
                self._routes.append((source, destination))
        else:
            raise Exception("Network requires at least 1 route.")
        
        self._nodes = {}
        for vertex in self.get_vertices():
            self._nodes[vertex] = self.Node(vertex)
        
    def update(self, tick, packages_generation):
        """ _summary_ #TODO

        Args:
            tick (int): The current tick in the simulation.
            packages_generation (method): The callback of the function used to generate packages.
        """
        for source in self._graph:
            for index, destination_tuple in enumerate(self._graph[source]):
                destination_list = list(destination_tuple)
                destination_list[2] = random.randint(0, destination_list[1] + 1) # current throughput is randomized in [0, maximum_throughput]
                self._graph[source][index] = tuple(destination_list)
        
        for _, node in self._nodes.items():
            node.update() # moves the packages from 'reception' to 'ready_to_send' queue
            
        for (source, destination) in self._routes:
            self._nodes[source].new_packages(packages_generation(), tick, destination) # generates n packages for each node source

        #3 pour tous les noeuds on vide les file d'envoie en fonction du debit vers un noeud choisit par ordonnanceur
        for source in self._graph:
            if self._graph[source] and not self._nodes[source].is_buffer_empty(): # if the node has any neighbour and data waiting in buffer
                next = random.choice(self.get_direct_neighbours(source)) #TODO le protocol choisit le meilleur node de source vers un de ces voisins, (node, maximun weight, current weight)
                print(next)
                n = 1
                packages = self._nodes[source].get_packages(n)
                
                r = []
                for index, package in enumerate(packages):
                    if package['to'] == self._nodes[next].name:
                        r.append(packages.pop(index)) # récupérer elapsed delai
                
                # statistics

                self._nodes[next].set_packages(packages) 
                
        for name, node in self._nodes.items():
            node.toString()
        
        
                
        

        #AODV
        #OLSR 1 dan le cours



scenario = Network(routes=[('s', 'd')], edges=[('s', 'l1', 200), ('l1', 'l2', 200), ('l2', 'd', 50), ('s', 'r1', 100), ('r1', 'r2', 100), ('r2', 'd', 100)])