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
    badClusters = []
    for parentNode in parentNodes:
        neighbors = list(nx.all_neighbors(graph,parentNode))
        for i in neighbors:
            size = list(graph.neighbors(i))
            if (len(size) > 1):
                badClusters.append(i)

    for item in badClusters:
        duplicates = list(nx.all_neighbors(graph,item))
        for d in duplicates:
            if (d in badClusters):
                dlen = len(list(nx.all_neighbors(graph,d)))
                itemlen = len(list(nx.all_neighbors(graph,item)))
                if (dlen > itemlen):
                    badClusters.remove(item)
                else :    
                    badClusters.remove(d)
        
    badCluster = removeDuplicates(badClusters)
    res = []        
    for item in badCluster:
        res.append([item,len(list(nx.all_neighbors(graph,item)))])
    return res

def removeDuplicates(test_list):
    res = []
    for i in test_list:
        if i not in res:
            res.append(i)
    return res

def writeClusters(graph,parentNodes) :
    for i in parentNodes :
        r = requests.get("https://contenderbicycles.com"+i)
        print(r.status_code)




            

def main():
    net = Network(notebook=True)
    graph = csvIN()
    parentnodes = getParentNodes(graph)
    res = findOffender(graph,parentnodes)
    allbrokennodes = [] 
    for item in res :
        print("-----------------")
        allbrokennodes.append(item[0])
        print(item[0])        
        print(item[1])
        print("-----------------")
    print(len(res))
    print("|||||||||||||||||||||||||")
    visualize(graph)
    writeClusters(graph,allbrokennodes)
     
main()