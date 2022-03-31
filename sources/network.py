import numpy as np
import pandas as pd
import cmasher as cmr
import networkx as nx
import statistics as stats
import numpy.random as random

from enum import IntEnum, unique

class Graph():
    def __init__(self, filepath: str):
        """ Constructs a directed graph with the specified edges.
        
        Args:
            filepath (str): the path of the csv containing the data.
        """
        df = pd.read_csv(filepath) # dataframe retrieving graph edges from the csv
        self._graph = nx.from_pandas_edgelist(df, edge_attr=['average_throughput'], create_using=nx.DiGraph(directed=True))
        
        nx.set_edge_attributes(self._graph, values=None, name='current_throughput') # sets for each edge None as the current throughput
        
        self._emitters = set() # the set of routes (src, dst) specified in the csv
        for column in df.iloc():
            src, dst = column['source'], column['destination']
            if dst == dst and src != dst and self._graph.has_node(dst) and nx.shortest_path(self._graph, src, dst):
                self._emitters.add((src, dst))
        
    def get_weighted_edges(self):
        """ Returns all the edges of the graph formated like so (source, target, weight).

        Returns:
            out (list): all the edges of the graph.
        """
        return list(self._graph.edges(data='average_throughput'))
    
    def get_edges(self):
        """ Returns all the edges of the graph formated like so (source, target).

        Returns:
            out (list): all the edges of the graph.
        """
        return list(self._graph.edges())
    
    def get_vertices(self):
        """ Returns all the vertices of the graph.

        Returns:
            out (NodeView): the nodes from the graph.
        """
        return nx.nodes(self._graph)
    
    def get_adjacency_list(self):
        """ Returns all the edges as an adjacency list.

        Returns:
            out (list): lines of data in adjlist format.
        """
        return nx.generate_adjlist(self._graph)

class Network(Graph):
    @unique
    class Protocol(IntEnum):
        OLSR = 0
        AODV = 1
        LSOR = 2
        MAX_BOTTLENECK = 3
        FASTEST_BUFFER = 4
        EMPTIEST_BUFFER = 5
        
    class _Node():
        def __init__(self, node_name):
            self.name = str(node_name)
            self.packages_in = [] # packages that have just been received
            self.packages_out = [] # packages that will be sent
        
        def __eq__(self, other):
            if isinstance(other, type(self)):
                return self.name == other.name
            return False
        
        # COMMENT S'EN SORTIR ?
        #
        # 1 passer self en argument de Node()
        # 2 passer self en argument de update()
        # 3 faire une troisième classe stylé
        # 4 recommencer du debut, mais a l'envers
        # 5 faire à manger
        # 6 faire caca

        def update(self, tick: int):
            """ Moves the packages from 'packages_in' to 'packages_out' buffer.
            
            Args:
                tick (int): The current tick in the simulation.
            """
            for package in self.packages_in:
                if package['to'] == self.name:
                    pass
                    # statistics = Network.statistics[(package['from'], package['to'])]
                    # statistics['total_tick'] += tick - package['sent']
                    # statistics['package_arrived'] += 1
                else:
                    self.packages_out.append(package)
            self.packages_in = []
            
        def get_packages_from_out(self, n: int):
            """ Returns the packages to be sent. Those packages are removed from the buffer.

            Args:
                n (int): The number of packages to pop.
                
            Returns:
                out (list): The list of packages to send from this node.
            """
            return [ self.packages_out.pop(0) for _ in range(min(len(self.packages_out), n)) ]
        
        def set_packages_in(self, packages: list):
            """ Adds the specified packages at the end of the buffer.

            Args:
                packages (list): The list of received packages.
            """
            self.packages_in.extend(packages)
        
        def set_packages_out(self, packages: list):
            """ Sets the specified packages ready for send.

            Args:
                packages (list): The list of new packages to send from this node.
            """
            self.packages_out.extend(packages)
        
        def get_buffer_size(self):
            """ Returns the size of the buffer.

            Returns:
                out (int): The length of the buffer.
            """
            return len(self.packages_out)
        
        def is_buffer_empty(self):
            """ Tells if the buffer is empty.

            Returns:
                out (bool): True if the buffer is empty, otherwise False.
            """
            return not self.packages_out
        
        def set_buffer_empty(self):
            self.packages_out = []
            self.packages_in = []
            
    def __init__(self, filename: str, protocol=0):
        super().__init__('ressources/dataframes/' + filename + '.csv')
        
        self._nodes = {} # creates a list of node object to be used in the simulation
        for vertex in self.get_vertices():
            self._nodes[vertex] = self._Node(vertex)
        
        self.__setup(self.Protocol(protocol))
        
        self.statistics = { e:{ 'package_arrived': 0, 'package_sent': 0, 'total_tick': 0 } for e in self._emitters }
    
    def get_nodes(self):
        """ Returns the list of nodes.

        Returns:
            out (list): the list of nodes.
        """
        return self._nodes[:]

    def render_stat(self):
        #somme des delais moyens
        res = 0
        for stat in self.statistics: 
            res += stat['total_tick'] / stat['package_arrived']
        print("somme des delais moyens", res)

        # pourcentage de paquets déservis pour le réseau caca prout forever young
        res2 = 0
        for stat in self.statistics:
            res2 += stat['package_arrived'] / stat['package_sent']
        res2 /= len(self.statistics)
        print("pourcentage caca", res2)
        
        # pourcentage de paquets déservis pour le réseau trop bien
        arrived = 0    
        sent = 0
        for stat in self.statistics:
            arrived += stat['package_arrived']
            sent += stat['package_arrived']
        res3 = arrived / sent
        print("pourcentage bien", res3)

        return res

    
    def clear(self):
        #ici
        #self.stat.append(self.render_stat()) #TODO
        
        for node in self._nodes.values():
            node.set_buffer_empty()
            
    def render(self, pltax):
        pos = nx.kamada_kawai_layout(self._graph)
        labels = nx.get_edge_attributes(self._graph, 'average_throughput')
        
        edges = self.get_edges()
        colors = [0] * len(edges)
        if self._paths:
            for i, emitter in enumerate(self._emitters):
                path = self._paths[emitter]
                color = i + 1
                for n in range(len(path) - 1):
                    edge = (path[n], path[n + 1])
                    colors[edges.index(edge)] = color
        
        cm = cmr.get_sub_cmap('cmr.torch', 0, 0.6, N=(len(self._emitters) + 1))

        nx.draw(self._graph, pos, ax=pltax, with_labels=True, width=1.5, edge_color=colors, edge_cmap=cm,
            node_color='#504e52', node_size=300, font_size=14, font_weight='bold', font_color='whitesmoke')
        
        nx.draw_networkx_edge_labels(self._graph, pos, ax=pltax, edge_labels=labels, font_size=10)        
    
    def update(self, tick: int, load: int):
        # current throughput is randomized around its average_throughput
        for (u, v, w) in self.get_weighted_edges():
            nx.set_edge_attributes(self._graph, {(u, v): { 'current_throughput': int(random.normal(w, 1.0)) }})
        
        # generates n packages for each node source
        for (u, v) in self._emitters:
            packages = [ p | { 'from': u, 'to': v, 'sent': tick } for p in self.generate_packages(100, load, 2) ]
            self._nodes[u].set_packages_out(packages)
            self.statistics[(u, v)]['package_sent'] += len(packages)
        
        for (node_name, node) in self._nodes.items():
            nexts = {}
            for (src, dst) in set([ (p['from'], p['to']) for p in node.packages_out ]):
                nexts[(src, dst)] = self.__process_next(src, dst, node_name)
            
            throughput_nexts = { next: self._graph[node_name][next]['current_throughput'] for next in set(nexts.values()) }
            
            while node.packages_out and throughput_nexts[nexts[(node.packages_out[-1]['from'], node.packages_out[-1]['to'])]] > 0:
                package = node.packages_out.pop(0)
                throughput_nexts[nexts[(package['from'], package['to'])]] -= 1
                self._nodes[nexts[(package['from'], package['to'])]].set_packages_in([package])
        
        # moves the packages from 'reception' to 'ready_to_send' queue
        for node in self._nodes.values():
            node.update(tick + 1)
                 
    def generate_packages(self, package_size: int, normal_loc=0.0, normal_scale=1.0):
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
    
    def __olsr(self, src, dst):
            max, result = 0.0, None
            
            for path in nx.all_simple_paths(self._graph, src, dst):
                avg = stats.fmean([ self._graph[path[n]][path[n + 1]]['average_throughput'] for n in range(len(path) - 1) ])
                if avg > max:
                    max = avg
                    result = path

            return result
    
    def __lsor(self, src, dst, forward_range=1):
            max, result = 0.0, None
            
            for path in nx.all_simple_paths(self._graph, src, dst):
                avg = stats.fmean([ self._graph[path[n]][path[n + 1]]['current_throughput'] for n in range(len(path[:forward_range])) ])
                if avg > max:
                    max = avg
                    result = path
                    
            return result
        
    def __aodv(self, src, dst):
        return min(nx.all_simple_paths(self._graph, src, dst), key=len)
    
    def __path_max_bottleneck(self, src, dst):
        paths = nx.all_simple_paths(self._graph, src, dst)
        max, result = 0.0, None

        for path in paths:
            bottle_neck = min( self._graph[path[n]][path[n + 1]]['average_throughput'] for n in range(len(path) - 1) )
            if bottle_neck > max:
                max = bottle_neck 
                result = path
                
        return result
    
    def __path_min_buffer(self, src, dst):
            min, result = np.inf, None
            
            for path in nx.all_simple_paths(self._graph, src, dst):
                size = self._nodes[path[1]].get_buffer_size()
                if size < min:
                    if size == 0:
                        return path
                    min = size
                    result = path
                     
            return result
        
    def __path_fastest_buffer(self, src, dst):
        result, max = None, -1
        
        for path in nx.all_simple_paths(self._graph, src, dst):
            node = self._nodes[path[1]]
            if node.is_buffer_empty():
                return path
            else:
                tick = node.packages_out[0]['sent']
                if tick > max:
                    max = tick
                    result = path

        return result
    
    def __setup(self, protocol):
        self.protocol = protocol
        func = {
            self.Protocol.OLSR: self.__olsr,
            self.Protocol.AODV: self.__aodv,
            self.Protocol.MAX_BOTTLENECK: self.__path_max_bottleneck
        }
        
        self._paths = {}
        if protocol in func:
            self._paths = { (u, v) : func[protocol](u, v) for (u, v) in self._emitters }
            print(self.protocol.name + " : " + str(self._paths))
            
    def __process_next(self, src, dst, node_name):
        func = {
            self.Protocol.LSOR: self.__lsor,
            self.Protocol.FASTEST_BUFFER: self.__path_fastest_buffer,
            self.Protocol.EMPTIEST_BUFFER: self.__path_min_buffer
        }
        
        if self.protocol in func:
            self._paths[(src, dst)] = func[self.protocol](node_name, dst)
        
        path = self._paths[(src, dst)]
        return path[path.index(node_name) + 1]
    
    # def le_meilleur_debit_median(src, dst):
        #     paths = nx.all_simple_paths(self._graph, src, dst)
        #     max, result = 0.0, None
            
        #     for path in paths:
        #         med = statistics.median([ neigbour['average_throughput'] for neigbour in path ])
        #         if med > max:
        #             max = med 
        #             result = path
                    
        #     return result