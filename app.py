from doctest import master
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
def visualize (graph,name) :
    net = Network(notebook=True)
    dir_network = nx.Graph(graph)
    net.from_nx(dir_network)
    net.show(name+".html")

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
#given a node it returns an edgelist of the subgraph
def edgelistFromNode (graph,node):
    edgelist = []
    trivialedges = list(graph.neighbors(node))
    for i in trivialedges:
        edge1 = (i,node)
        edgelist.append(edge1)
    allnodes = list(nx.all_neighbors(graph,node))
    for i in allnodes :
        neighbors = list(graph.neighbors(i))
        for n in neighbors:
            edge = (n,i)
            if edge not in edgelist:
                edgelist.append(edge)
    return edgelist
            
def writeClusters(graph,parentNodes) :
    for i in parentNodes :
        r = requests.get("https://contenderbicycles.com"+i)
        print(r.status_code)


def init():
    graph = csvIN()
    l = findOffender(graph,getParentNodes(graph))
    
    listofgraphs = []
    listofedgelists = []
    for item in l:
        edge = edgelistFromNode(graph,item)
        listofedgelists.append(edge)
        listofgraphs.append(nx.Graph(edge))
         
    return listofgraphs,listofedgelists

def makeVisuals(listofgraphs):
    count = 1
    for item in listofgraphs:
        visualize(item,"graph"+str(count))
        count += 1
    
    
     
if __name__ =="__main__":
    listofgraphs, listofedges = init()
    makeVisuals(listofgraphs)
    count = 1
    with open('log.txt','w') as f:
        for item in listofedges:
            f.write("-------------------- ")
            f.write(str(count)+"\n")
            count += 1
            for e in item:
                f.write(str(e)+"\n")
            f.write("---------------------\n")