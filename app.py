import os ;
import networkx as nx ;
import csv ;
from pyvis.network import Network ;


def csvIN () :
    output = []
    with open('DATA.csv') as csvfile:
        array = csv.reader(csvfile)
        loopableArray = list(array)

    for line in loopableArray:
        output.append((line[0],line[1]))

    return output



def main():
    net = Network(notebook=True)
    edgelist = csvIN()
    dir_network = nx.Graph(edgelist)
    net.from_nx(dir_network)
    net.show("example.html")
    
    
main()