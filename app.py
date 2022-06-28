from pickle import FALSE
import networkx as nx ;
import csv ;
from pyvis.network import Network ;
#virtual env GRAPH source GRAPH/bin/activate

#take csv and pulls it into tuples
#creates edge list and generates graph with it RETURNS graph
def csvIN () :
    output = []
    with open('DATA.csv') as csvfile:
        array = csv.reader(csvfile)
        loopableArray = list(array)
    for line in loopableArray:
        output.append((line[0],line[1]))    
    graph = nx.Graph(output)
    return graph
    
def visualize (graph) :
    net = Network(notebook=True)
    dir_network = nx.Graph(graph)
    net.from_nx(dir_network)
    net.show("output.html")

def getParentNodes (graph) :
    parentNodes = []
    for n in graph.nodes :
        if len(list(graph.neighbors(n))) > 1 :
            parentNodes.append(n)
    return parentNodes

def findOffender(graph,parentNodes) :
    badClusters = []
    for parentNode in parentNodes:
        neighbors = list(nx.all_neighbors(graph,parentNode))
        for i in neighbors:
            size = list(graph.neighbors(i))
            if (len(size) > 1):
                badClusters.append(i)
            
    print(badClusters)            

        
def main():
    net = Network(notebook=True)
    graph = csvIN()
    visualize(graph)
    parentnodes = getParentNodes(graph)
    findOffender(graph,parentnodes)
     
main()