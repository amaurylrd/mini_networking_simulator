class Graph():
    def __init__(self, edges=[]):
        """ Constructs a graph with the specified edges.
        
        Args:
            edges (list): the list of tuple within at least the 2 first elements are ordered nodes.
        """
        self._graph = {}

        for edge_tuple in edges:
            for vertex in list(edge_tuple[:2]):
                if not vertex in self._graph:
                    self._graph[vertex] = []
        
        for edge_tuple in edges:
            self._graph[edge_tuple[0]].append(edge_tuple[1:])
        
    def get_vertices(self):
        """ Returns all the vertices of the graph.

        Returns:
            out (list): the vertices from the graph.
        """
        return list(self._graph.keys())
    
    def get_edges(self):
        """ Returns all the edges as an adjacency list.

        Returns:
            out (list): the edges from the graph.
        """
        return self._graph.copy()
    
    def __get_neighbours(self, vertex):
        return [ tuple[0] for tuple in self._graph[vertex] ]
    
    def get_neighbours(self, vertex, depth=1):
        """ Returns the neighbours of the specified vertex (by default, with a depth of 1).

        Args:
            vertex (any): The specified vertex.
            depth (int, optional): The depth of recursion. Defaults to 1.

        Returns:
            out (ndarray): At position i the list of neighbours far from i + 1 vertices.
        """
        neigbours = [self.__get_neighbours(vertex)]
        
        for _ in range(1, depth):
            next_neigbours = []
            
            for neigbour in neigbours[:-1]:
                next_neigbours.append(self.__get_neighbours(neigbour))
            
            if not next_neigbours:
                return neigbours
            else:
                neigbour.append(list(dict.fromkeys(next_neigbours)))

        return neigbours

    def add_edge(self, edge):
        for vertex in list(edge[:2]):
            if not self._graph[vertex]:
                self._graph[vertex] = []
        
        self._graph[edge[0]].append(edge[1:])
        
    def dfs(self, start, visited=None):
        if self._graph[start]:
            return [ x for x in self.__dfs(start, visited) if x is not start ]  
        return []
    
    def __dfs(self, start, visited):
        if visited is None:
            visited = set()
        visited.add(start)

        for next in set(self._graph[start]) - visited:
            self.__dfs(next[0], visited)

        return visited

    # idée de fonction pour la classe graph
    # find_shortest_path
    # get all simple
    # find shortest with weight


        
    
        
# class Node():
#     def __init__(self, node_name):
#         self._name = node_name
        
#     def get_name(self):
#         return self._name