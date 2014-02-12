#RIGHT CLICK TO ADD A NODE
#RIGHT CLICK AN EXISTING NODE TO REMOVE IT
#SCROLL WHEEL WHILE ON TOP OF A NODE TO REMOVE IT, AND ADD RELATIONSHIPS BETWEEN ALL OF IT'S RELATED NODES (THAT DIDN'T ALREADY HAVE A RELATIONSHIP)
#CLICK THE SCROLL WHEEL ON A NODE TO MAKE IT STATIONARY, SO IT IS UNMOVABLE BY OTHER NODES
NUMBER_OF_NODES_TO_CONNECT_TO = 2

from FDGraph import *
import random
import time
import math
import threading
import pygame

graph = Graph.Graph()

lastnodeadded = 0

g = Grapher.Grapher(graph = graph)        

def drawfunction(screen, node, graph, position):
    pygame.draw.circle(screen, (255, 255, 255), position, 3, 0)

#returns a single NODE that is closest to the given node
def findsingleclosest(node, listofnodes):
    closestnode = listofnodes[0]
    distance = Node.findDistance(node, closestnode)
    
    for n in listofnodes:
        dist = Node.findDistance(node, n)
        if dist < distance:
            distance = dist
            closestnode = n

    return closestnode

#returns a list of all of the closest nodes to the given one
def findclosest(node, graph, numbertofind):
    closestnodes = []
    allnodes = graph.nodes.values()[:]
    allnodes.remove(node)
    
    for i in range(numbertofind):
        newclosest = findsingleclosest(node, allnodes)
        closestnodes = closestnodes + [newclosest]
        allnodes.remove(newclosest)

    return closestnodes

#takes a graph and a grapher (g)
def mainthread():
    global graph, g, lastnodeadded, NUMBER_OF_NODES_TO_CONNECT_TO
    while g.running:
        events = g.getEvents()
        for e in events:
            print "recieved event:", e
            #if the event is a mouse click event and the mousebutton is the right click
            if e[0] == 0 and e[1] == 3:
                if not e[2] == None:
                    graph.lock()
                    graph.removeNode(e[2])
                    graph.unlock()
                else:
                    #adding a node with random relationships if one doesn't already exist
                    lastnodeadded = lastnodeadded + 1
                    graph.lock()
                    n = Node.Node(str(lastnodeadded), position = g.getRelativeMousePosition())
                    graph.addNode(n)

                    numbertofind = NUMBER_OF_NODES_TO_CONNECT_TO
                    if lastnodeadded < NUMBER_OF_NODES_TO_CONNECT_TO + 1:
                        numbertofind = len(graph.nodes)-1
                    
                    for closestnode in findclosest(n, graph, numbertofind):
                        graph.addRelationship(n.UID, closestnode.UID)
                        
                    graph.unlock()
            elif e[0] == 0 and (e[1] == 4 or e[1] == 5): #if we scroll the mouse wheel over a node
                if not e[2] == None:
                    #we are going to add relationships between every node this one is connected to to each other as long as they don't already have them
                    graph.lock()
                    n = e[2]#the UID of the node clicked
                    if n in graph.relationships: #we need to check if it exists in the relationships dictionary because there is a chance it has been deleted since the event was generated
                        allrelationships = graph.relationships[n][0] + graph.relationships[n][1]
                        for relatednode in allrelationships:
                            for relatednode2 in allrelationships:
                                if relatednode == relatednode2:
                                    continue
                                else: #if the nodes do not currently have a relationship with oneanother, add one
                                    if (not relatednode2 in graph.relationships[relatednode][0]) and (not relatednode2 in graph.relationships[relatednode][1]):
                                        graph.addRelationship(relatednode, relatednode2)
                        graph.removeNode(n)
                    graph.unlock()
            elif e[0] == 0 and e[1] == 2:
                if not e[2] == None:
                    graph.nodes[e[2]].static = not graph.nodes[e[2]].static
        time.sleep(0.2)
    print "FDGRAPHER HAS FINISHED. QUITTING MAIN THREAD..."

    

lastnodeadded = lastnodeadded + 1
graph.addNode(Node.Node(str(lastnodeadded), position = (300, 300)))

g.setNodeDrawFunction(drawfunction)
g.start()

maint = threading.Thread(target = mainthread)
maint.start()





