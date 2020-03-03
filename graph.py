import math
import heapq
import random
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]



class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def neighbors(self, current):
        if current in self.__graph_dict:
            return self.__graph_dict[current]
        else:
            return []
    def cost(self, current, next):
        # w = math.sqrt((current.key[0]-next.key[0])*(current.key[0]-next.key[0]) + (current.key[1]-next.key[1])*(current.key[1]-next.key[1]))
        
        w = math.sqrt((current[0]-next[0])*(current[0]-next[0]) + (current[1]-next[1])*(current[1]-next[1]))
        return round(w,2)


    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        vertex1 = edge.pop()
        if edge:
            # not a loop
            vertex2 = edge.pop()
        else:
            # a loop
            vertex2 = vertex1
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def find_isolated_vertices(self):
        """ returns a list of isolated vertices. """
        graph = self.__graph_dict
        isolated = []
        for vertex in graph:
            print(isolated, vertex)
            if not graph[vertex]:
                isolated += [vertex]
        return isolated

    def find_path(self, start_vertex, end_vertex, path=[]):
        """ find a path from start_vertex to end_vertex 
            in graph """
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in graph:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex, 
                                               end_vertex, 
                                               path)
                if extended_path: 
                    return extended_path
        return None
    

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to 
            end_vertex in graph """
        graph = self.__graph_dict 
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex, 
                                                     end_vertex, 
                                                     path)
                for p in extended_paths: 
                    paths.append(p)
        return paths

    def is_connected(self, 
                     vertices_encountered = None, 
                     start_vertex=None):
        """ determines if the graph is connected """
        if vertices_encountered is None:
            vertices_encountered = set()
        gdict = self.__graph_dict        
        vertices = gdict.keys() 
        if not start_vertex:
            # chosse a vertex from graph as a starting point
            start_vertex = vertices[0]
        vertices_encountered.add(start_vertex)
        if len(vertices_encountered) != len(vertices):
            for vertex in gdict[start_vertex]:
                if vertex not in vertices_encountered:
                    if self.is_connected(vertices_encountered, vertex):
                        return True
        else:
            return True
        return False

    def vertex_degree(self, vertex):
        """ The degree of a vertex is the number of edges connecting
            it, i.e. the number of adjacent vertices. Loops are counted 
            double, i.e. every occurence of vertex in the list 
            of adjacent vertices. """ 
        adj_vertices =  self.__graph_dict[vertex]
        degree = len(adj_vertices) + adj_vertices.count(vertex)
        return degree

class Map:
    def __init__(self, map_dict):
        self.map = {}
        self.generate(map_dict)
        
    def generate(self, map_dict):
        for name , map in map_dict.items():
            vk = {v:k for k, v in map[1].items()}
            loc = { }
            for k in map[0].keys():
                loc[map[1][k]] = [map[1][n] for n in map[0][k]]
            
            self.map[name] = {'kk':map[0],'kv':map[1],'vk': vk, 'loc': loc}

    def empty(self):
        return len(self.map) == 0
    
    def put(self, name, map):
        vk = {v:k for k, v in map[1]}
        loc = { }
        for k in map[0].keys():
            loc[map[1][k]] = [map[1][n] for n in map[0][k]]
        
        self.map[name] = {'kk':map[0],'kv':map[1],'vk': vk, 'loc': loc}
    
    def get(self, name=None):
        if name != None and name in self.map.keys():
            return self.map[name]
        return self.get_random()

    def get_random(self):
        _ , map = random.choice(list(self.map.items()))
        return map
        
map_dict = {
    "default": (
        {   "a" : ["b","d"],
            "b" : ["c","a"],
            "c" : ["f", "e","b"],
            "d" : ["e",'a'],
            "e" : ["c", "h", "i", "d"],
            "f" : ["c", "g", "j"],
            "g" : ["f","k"],
            "h" : ["e", "j"],
            "i" : ["e", "j"],
            "j" : ["f", 'e', "h", "i"],
            "k" : ["g"]
        },
        {
            "a" : (100, 300),
            "b" : (50, 100),
            "c" : (300, 200),
            "d" : (100, 600),
            "e" : (250, 400),
            "f" : (400, 100),
            "g" : (500, 390),
            "h" : (600, 500),
            "i" : (530, 280),
            "j" : (620, 30),
            "k" : (800, 100),
        }
    ),
    "travel": (
        {   "arad" : ["Sibiu","Zerind","Timisoara"],
            "Timisoara" : ["arad","Lugoj"],
            "Lugoj" : ["Timisoara",'Mehadia'],
            "Mehadia" : ["Lugoj", "Drobeta"],
            "Drobeta" : ["Mehadia", "Cariova"],
            "Cariova" : ["Rimnichu", 'pitesti', "Drobeta"],
            "Rimnichu" : ["Sibiu", 'Cariova', "pitesti"],
            "Zerind" : ["arad", "Oradea"],
            "Oradea" : ["Zerind", "Sibiu"],
            "Sibiu" : ["Oradea", 'arad', "Rimnichu","Fagaras"],
            "pitesti" : ["Rimnichu", 'Cariova', "Bucharest"],
            "Fagaras" : ["Sibiu", "Bucharest"],
            "Bucharest" : ["pitesti", 'Fagaras', "Giurgiu","Urziceni"],
            "Urziceni" : ["Hirsova", 'vaslui', "Bucharest"],
            "Hirsova" : ["Urziceni", "Eforie"],
            "vaslui" : ["Urziceni", "Iasi"],
            "Iasi" : ["vaslui", "Neamt"],
        },
        {
            "arad" : (60, 200),
            "Timisoara" : (58, 330),
            "Lugoj" : (140, 375),
            "Mehadia" : (150, 460),
            "Drobeta" : (150, 580),
            "Cariova" : (255, 590),
            "Rimnichu" : (290, 290),
            "Zerind" : (100, 100),
            "Oradea" : (200, 50),
            "Sibiu" : (210, 250),
            "pitesti" : (360, 360),
            "Fagaras" : (370, 220),
            "Bucharest" : (460, 420),
            "Urziceni" : (520, 380),
            "Hirsova" : (590, 420),
            "vaslui" : (570, 300),
            "Iasi" : (570, 190),
            "Neamt" : (540, 50),
            "Eforie" : (590, 580),
            "Giurgiu" : (450, 570),
        }
    ),
}
