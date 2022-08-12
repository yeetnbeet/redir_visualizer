import app;
import requests ;
import networkx as nx ;

def sortGraph(g):
    nodeList = list(g.nodes)
    sortedList = []
     
    flag = len(nodeList)
    while flag >= 1:
        for node in nodeList:
            if len(list(g.neighbors(node))) == flag:
                sortedList.append(node)
                
        flag -= 1  
    return [sortedList[0],sortedList]





graphlist,Ledgelist = app.init()

print(sortGraph(graphlist[250]))





    
    