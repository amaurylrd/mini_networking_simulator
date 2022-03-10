from graph import Graph

class Network(Graph):
    def __init__(self, routes, edges):
        super().__init__(edges)
        
        #if routes:
        #    for (source, destination) in routes:
                
                # possible route
        #else:
        #    raise Exception("Network requires at least 1 route.")
        
        self.routes = routes
        
    def add_route(self, source, destination):
        if  not self._graph[source] or  not self._graph[destination]:
            raise Exception("Routes must include existing nodes.")
        if source == destination:
            raise Exception("Routes must include 2 different nodes.")     
        #if self.dfs
        self.routing.append((source, destination))
    
    # shadow network 
    
    
    
    def update(self):
        #for node in self.get_vertices(): # copy ! pas bien
        #    node.pre_update()

        #for source 

        # self.current_throughput = random.randint(0, self.maximum_throughput + 1)
        
        # post update
        pass