import Grapher
import Graph
import Node
import random
import time
import pygame

def drawfunction(screen, node, graph, cameraposition):
    intpos = (int(node.position[0]), int(node.position[1]))
    relationships = len(graph.relationships[node.UID][0]) + len(graph.relationships[node.UID][1])
    pygame.draw.circle(screen, (200, 200, 200), intpos, 5, 0)

graph = Graph.Graph()

lastnodeadded = 0

g = Grapher.Grapher(graph = graph)

lastnodeadded = lastnodeadded + 1
g.graph.addNode(Node.Node(str(lastnodeadded), position = (300, 300)))

g.setDrawFunction(drawfunction)

g.start()



while True:
    print g.getEvents()
    lastnodeadded = lastnodeadded + 1
    g.graph.addNode(Node.Node(str(lastnodeadded), position = (random.randint(0, 600), random.randint(0, 600))))
    g.graph.addRelationship(str(lastnodeadded), str(lastnodeadded-1))
    time.sleep(2)
