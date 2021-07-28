###########################################################################################################################
#               Hassan Shahzad
#               18i-0441
#               CS-D
#               FAST-NUCES ISB
#               chhxnshah@gmail.com
###########################################################################################################################

###################################################### Node Class #########################################################

class Node:
        
    def __init__(self, name, parent, g, h, f):                                          # Initializing the class
        self.name = name
        self.parent = parent
        self.g = g                                                                      # Distance to start node
        self.h = h                                                                      # Distance to goal node
        self.f = f                                                                      # Total cost
            
    def __eq__(self, other):                                                            # Comparing two nodes
        return self.name == other.name
    
    def __lt__(self, other):                                                            # Sorting nodes
        return self.f < other.f
    
    def __repr__(self):                                                                 # Printing nodes
        return ('({0},{1})'.format(self.name, self.f))
    
    def printNode(self):                                                                # Customized Printing of nodes
        print(self.name, end = " - ")
        print(self.parent, end = " : ")
        print(self.g, end = " : ")
        print(self.h, end=" : ")
        print(self.f)

###########################################################################################################################

###################################################### Graph Class ########################################################

class Graph:
    
    def __init__(self, graph_dict=None, directed=True):                                 # Initialize the class
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()
                
    def make_undirected(self):                                                          # Create an undirected graph by adding symmetric edges
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist
                    
    def connect(self, A, B, distance=1):                                                # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance
               
    def get(self, a, b=None):                                                           # Get neighbors or a neighbor
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)
            
    def nodes(self):                                                                    # Return a list of nodes in the graph
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

    def getNode(self, city, heuristics, end):                                           # Get a specific neighbour which has minimum cost
        nodes = list()
        min = 999
        for (b,dist) in self.graph_dict[city].items():
            if(b == end):
                return Node(city, b, dist, heuristics[b], dist+heuristics[b] )
            nodes.append(Node(city, b, dist, heuristics[b], dist+heuristics[b] ))
            if (dist+heuristics[b]) < min:
                min = dist+heuristics[b]
                minnode = Node(city, b, dist, heuristics[b], dist+heuristics[b] )       
        return minnode
        
    def printgraph(self):                                                               # Function to print each edge in the entire graph
         for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                print (self.graph_dict.setdefault(a,{})[b], end = " : ")
                print(a, end = " - ")
                print(b)


###########################################################################################################################

################################################## A* Implementation ######################################################
        

def A_Star(graph, heuristics, start, end):
    open_list = list()
    closed_list = list()  
    path = list()                                                                       # Will store the path we are taking
    curr_node = graph.getNode(start,heuristics, end)                                    # Starting node
    open_list.append(curr_node)
    totalcost = 0

    if(end not in graph.graph_dict):                                                    # Incase the goal state does not exist
        print("\n\n---------------------------\nGOAL STATE DOES NOT EXIST\n---------------------------\n\n")
        return  None

    while(curr_node.name != end):                                                       # Runs Until we cannot find the goal state or
        totalcost += curr_node.g
        path.append(curr_node.name)
        curr_node = open_list.pop()
        closed_list.append(curr_node)
        curr_node = graph.getNode(curr_node.parent,heuristics, end)
        open_list.append(curr_node)
        if(curr_node.name == end):
            path.append(curr_node.name)
            break

    print("FINAL COST -> " + str(totalcost))
    return path
    
###########################################################################################################################

########################################################## Main ###########################################################


# The main entry point for this module
def main():
    # Create a graph
    graph = Graph()
        
    # Create graph connections (Actual distance)
    graph.connect('Arad', 'Zerind', 75)
    graph.connect('Arad', 'Siblu', 140)
    graph.connect('Arad', 'Timisoara', 118)
    graph.connect('Zerind', 'Oradea', 71)
    graph.connect('Oradea', 'Siblu', 151)
    graph.connect('Siblu', 'Fugaras', 99)
    graph.connect('Siblu', 'Rimnicu Vilcea', 80)
    graph.connect('Rimnicu Vilcea', 'Pitesti', 97)
    graph.connect('Timisoara', 'Lugoj', 111)
    graph.connect('Lugoj','Mehadia', 70)
    graph.connect('Mehadia', 'Dobreta',75)
    graph.connect('Dobreta', 'Craiova', 120)
    graph.connect('Craiova','Rimnicu Vilcea', 146)
    graph.connect('Craiova','Pitesti', 138)
    graph.connect('Fugaras', 'Bucharest', 211)
    graph.connect('Pitesti', 'Bucharest', 101)
    graph.connect('Giurgiu', 'Bucharest', 90)
        
        
    # Make graph undirected, create symmetric connections
    graph.make_undirected()
        
    # Create heuristics (straight-line distance, air-travel distance) for Destination Bucharest
    heuristics = {}
    heuristics['Arad'] = 366
    heuristics['Bucharest'] = 0
    heuristics['Craiova'] = 160
    heuristics['Dobreta'] = 242
    heuristics['Fugaras'] = 176
    heuristics['Lugoj'] = 244
    heuristics['Mehadia'] = 241
    heuristics['Oradea'] = 380
    heuristics['Pitesti'] = 10
    heuristics['Rimnicu Vilcea'] = 193
    heuristics['Siblu'] = 253
    heuristics['Timisoara'] = 329
    heuristics['Zerind'] = 374
    heuristics['Giurgiu'] = 77
    
    
    
    
        
    # Print Graph Nodes
    graph.printgraph()
    print("--------------------------------\n\n")
    # Run search algorithm
    path = A_Star(graph, heuristics, 'Arad', 'Bucharest')        
    print("PATH: " ,end = " ")
    print(path)

# Tell python to run main method
if __name__ == "__main__": main()