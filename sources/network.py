import numpy as np
import pandas as pd
import cmasher as cmr
import networkx as nx
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
        SHORTEST_PATH = 1
        LSOR = 2
        MAX_BOTTLENECK = 3
        FASTEST_BUFFER = 4
        EMPTIEST_BUFFER = 5
        HYDRBID = 6
        
    class _Node():
        def __init__(self, node_name):
            self.name = str(node_name)
            self.packages_in = [] # packages that have just been received
            self.packages_out = [] # packages that will be sent
        
        def __eq__(self, other):
            if isinstance(other, type(self)):
                return self.name == other.name
            return False
        
        def set_packages_in(self, packages: list):
            """ Adds the specified packages at the end of the buffer.

            Args:
                packages (list): the list of received packages.
            """
            self.packages_in.extend(packages)
        
        def set_packages_out(self, packages: list):
            """ Sets the specified packages ready for send.

            Args:
                packages (list): the list of new packages to send from this node.
            """
            self.packages_out.extend(packages)
    
    def __init__(self, filename: str, protocol=0):
        super().__init__(filename)
        
        # creates a list of node object to be used in the simulation
        self._nodes = {}
        for vertex in self.get_vertices():
            self._nodes[vertex] = self._Node(vertex)
        
        # setups the protocol routing algorithm
        self.__setup(self.Protocol(protocol)) 
        
        # creates objects to store the data for statistics
        self._statistics_tmp = { e:{ 'package_arrived': 0, 'package_sent': 0, 'total_delay': 0 } for e in self._emitters }
        self.statistics_plots = []
        
    def get_nodes(self):
        """ Returns the list of nodes.

        Returns:
            out (list): the list of nodes.
        """
        return self._nodes[:]
    
    def clear(self):
        # retrives the data from the simulation to be cleared
        plot_y = { 'average_delay': {}, 'pourcentage_destination': {}, 'buffer_occupation': {} }
        
        # 1. average delay
        plot_y['average_delay']['sum_average'] = 0
        for k, v in self._statistics_tmp.items():
            delay = 0
            if v['package_arrived'] > 0:
                delay = v['total_delay'] / v['package_arrived']
            plot_y['average_delay'][k] = delay
            plot_y['average_delay']['sum_average'] += delay
        
        # 2. pourcentage of packages sent to the destination
        arrived, sent = 0, 0
        plot_y['pourcentage_destination']['pourcentage_total'] = 0
        for k, v in self._statistics_tmp.items():
            arrived += v['package_arrived']
            sent += v['package_sent']
            plot_y['pourcentage_destination'][k] = 0
            if v['package_sent'] > 0:
                plot_y['pourcentage_destination'][k] = v['package_arrived'] / v['package_sent'] * 100
        if sent > 0:
            plot_y['pourcentage_destination']['pourcentage_total'] = arrived / sent * 100

        # 3. average buffer occupation
        plot_y['buffer_occupation']['average_occupation'] = np.mean([ len(node.packages_out) for node in self._nodes.values() ])

        # refresh the data for the next simulation
        for k in self._statistics_tmp:
            self._statistics_tmp[k] = dict.fromkeys(self._statistics_tmp[k], 0)

        # store the data for the rendering
        self.statistics_plots.append(plot_y)
        
        # clear the data of the nodes
        for node in self._nodes.values():
            node.packages_out = []
            node.packages_in = []
            
    def render(self, pltax):
        pos = nx.kamada_kawai_layout(self._graph) # alternatively, pos = nx.spectral_layout(self._graph)
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
        
        return cm
       
    def update(self, tick: int, load: int):
        # current throughput is randomized around its average_throughput
        for (u, v, w) in self.get_weighted_edges():
            nx.set_edge_attributes(self._graph, {(u, v): { 'current_throughput': max(0, int(random.normal(w, np.sqrt(w)))) }})
        
        # generates n packages for each node source
        for (u, v) in self._emitters:
            packages = [ p | { 'from': u, 'to': v, 'sent': tick } for p in self.generate_packages(100, load) ]
            self._nodes[u].set_packages_out(packages)
            self._statistics_tmp[(u, v)]['package_sent'] += len(packages)
        
        # moves the packages according to the path given by the routing algorithm
        for name, node in self._nodes.items():
            nexts = {}
            for (src, dst) in set([ (p['from'], p['to']) for p in node.packages_out ]):
                nexts[(src, dst)] = self.__process_next(src, dst, name)
            
            throughput_nexts = { next: self._graph[name][next]['current_throughput'] for next in set(nexts.values()) }
            
            while node.packages_out and throughput_nexts[nexts[(node.packages_out[-1]['from'], node.packages_out[-1]['to'])]] > 0:
                package = node.packages_out.pop(0)
                throughput_nexts[nexts[(package['from'], package['to'])]] -= 1
                self._nodes[nexts[(package['from'], package['to'])]].set_packages_in([package])
        
        # moves the packages from 'reception' to 'ready_to_send' queue and retrieves the data from packages arrived before deletion
        for name, node in self._nodes.items():
            for package in node.packages_in:
                if package['to'] == name:
                    stats = self._statistics_tmp[(package['from'], package['to'])]
                    stats['total_delay'] += tick - package['sent'] + 1
                    stats['package_arrived'] += 1
                else:
                    node.packages_out.append(package)
            node.packages_in = []
            
    def generate_packages(self, package_size: int, package_sample: int):
        """ Generates randomized packages from the specified parameters.

        Args:
            package_size (int): the specified fixed size (in bits) for all packages. Must be non-negative.
            package_sample (int): the average number of packages to be generated in [0, 2*package_sample]. Must be non-negative.
        Returns:
            out (ndarray): samples of packages from the parameterized generation.
        """
        packages = []
        samples = random.randint(0, package_sample + package_sample + 1)
        
        for _ in range(samples):
            package = { "data": random.randint(0, 2, size=(package_size)) } # generate an n-dimensional array of random bits
            packages.append(package)
        
        return packages
    
    def __olsr(self, src, dst):
            max, result = 0.0, None
            
            for path in sorted(nx.all_simple_paths(self._graph, src, dst), key=len):
                avg = np.mean([ self._graph[path[n]][path[n + 1]]['average_throughput'] for n in range(len(path) - 1) ])
                if avg > max:
                    max = avg
                    result = path

            return result
    
    def __lsor(self, src, dst, forward_range=1, paths=None):
            max, result = 0.0, None
            
            if paths is None:
                paths = sorted(nx.all_simple_paths(self._graph, src, dst), key=len)
            for path in paths:
                avg = np.mean([ self._graph[path[n]][path[n + 1]]['current_throughput'] for n in range(len(path[:forward_range + 1]) - 1) ])
                if avg > max:
                    max = avg
                    result = path
                    
            return result
        
    def __shortest_path(self, src, dst):
        return min(nx.all_simple_paths(self._graph, src, dst), key=len)
    
    def __path_max_bottleneck(self, src, dst, paths=None):
        max, result = 0.0, None

        if paths is None:
            paths = sorted(nx.all_simple_paths(self._graph, src, dst), key=len)
        for path in paths:
            bottle_neck = min( self._graph[path[n]][path[n + 1]]['average_throughput'] for n in range(len(path) - 1) )
            if bottle_neck > max:
                max = bottle_neck 
                result = path
                
        return result
    
    def __path_min_buffer(self, src, dst):
            min, result = np.inf, None
            
            for path in sorted(nx.all_simple_paths(self._graph, src, dst), key=len):
                size = len(self._nodes[path[1]].packages_out)
                if size < min:
                    if size == 0:
                        return path
                    min = size
                    result = path
                     
            return result
        
    def __path_fastest_buffer(self, src, dst, paths=None):
        result, max = None, -1
        
        if paths is None:
            paths = sorted(nx.all_simple_paths(self._graph, src, dst), key=len)
        for path in paths:
            node = self._nodes[path[1]]
            if not node.packages_out:
                return path
            else:
                tick = node.packages_out[0]['sent']
                if tick > max:
                    max = tick
                    result = path

        return result
    
    def __hybrid_solution(self, src, dst):
        funcs = {
            lambda src, dst, paths: self.__lsor(src, dst, 2, paths),
            self.__path_max_bottleneck,
            self.__path_fastest_buffer
        }
        
        paths = sorted(nx.all_simple_paths(self._graph, src, dst), key=len)
        ranks = [ i for i in range(len(paths)) ] # for the shortest path
        
        for func in funcs:
            tmp = paths[:]
            for i in range(len(ranks)):
                path = func(src, dst, tmp)
                ranks[paths.index(path)] += i
                tmp.remove(path)
            
        return paths[ranks.index(min(ranks))]
        
    def __setup(self, protocol):
        self.protocol = protocol
        funcs = {
            self.Protocol.OLSR: self.__olsr,
            self.Protocol.SHORTEST_PATH: self.__shortest_path,
            self.Protocol.MAX_BOTTLENECK: self.__path_max_bottleneck
        }
        
        self._paths = {}
        if protocol in funcs:
            self._paths = { (u, v) : funcs[protocol](u, v) for (u, v) in self._emitters }
            # for debug purpose print(self.protocol.name + " : " + str(self._paths))
            
    def __process_next(self, src, dst, node_name):
        funcs = {
            self.Protocol.LSOR: self.__lsor,
            self.Protocol.FASTEST_BUFFER: self.__path_fastest_buffer,
            self.Protocol.EMPTIEST_BUFFER: self.__path_min_buffer,
            self.Protocol.HYDRBID: self.__hybrid_solution
        }
        
        paths = dict(self._paths)
        if self.protocol in funcs:
            paths[(src, dst)] = funcs[self.protocol](node_name, dst)
            
        return paths[(src, dst)][paths[(src, dst)].index(node_name) + 1]
    
