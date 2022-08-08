from pickle import FALSE
from re import I
import networkx as nx ;
import csv ;
from pyvis.network import Network ;
import requests ;
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
    print("\nThe number of redirects scanned: ",len(output))    
    graph = nx.Graph(output)
    return graph

#creates an interactive visual using pyvis.network    
def visualize (graph) :
    net = Network(notebook=True)
    dir_network = nx.Graph(graph)
    net.from_nx(dir_network)
    net.show("output.html")

#finds a group that could technically be a chain
def getParentNodes (graph) :
    parentNodes = []
    for n in graph.nodes :
        if len(list(graph.neighbors(n))) > 1 :
            parentNodes.append(n)
    return parentNodes

#finds a group that has more than one parent node
def findOffender(graph,parentNodes) :
    alreadyChecked = []
    groupWithIssues = []

    for parentNode in parentNodes:
        if parentNode not in alreadyChecked: 
            neighbors = list(nx.all_neighbors(graph,parentNode))
            for i in neighbors:
                if i not in alreadyChecked:
                    size = list(graph.neighbors(i))
                    if (len(size) > 1):
                        alreadyChecked.append(i)
                        groupWithIssues.append(i)
    
    return groupWithIssues
            
def writeClusters(graph,parentNodes) :
    for i in parentNodes :
        r = requests.get("https://contenderbicycles.com"+i)
        print(r.status_code)


def main():
    net = Network(notebook=True)
    graph = csvIN()
    l = findOffender(graph,getParentNodes(graph))
    print("----------------------------------")
    for item in l:
        print(item)
    visualize(graph)
     
main()