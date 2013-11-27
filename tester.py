import Grapher
import Graph
import Node
import random
import time
import pygame
import math

################################################
################################################
#USE PROPERTIES WITHIN GRAPH.PY TO EDIT NODES AND RELATIONSHIPS. IF IT
#IS OWNED BY A GRAPHER, MAKE A QUEUE OF CHANGES TO BE MADE, AND THEN
#ONCE THE GRAPHER IS FINISHED, MAKE ALL OF THE CHANGES.
################################################
################################################

def drawfunction(screen, node, graph, cameraposition):
    intpos = (int(node.position[0]), int(node.position[1]))
    relationships = len(graph.relationships[node.UID][0]) + len(graph.relationships[node.UID][1])

    #n produces a colour gradient between 0 and 254 depending on the number of relationships
    n = (((1 + 1.0/(0.35*(relationships+1)))**(0.35*relationships)-1)/1.71828)*254 #tends to 254 as relaitonships tend to infinity
        
    pygame.draw.circle(screen, (int(n), 0, 255-int(n)), intpos, 10, 0)

    f = pygame.font.Font(None, 20).render(str(relationships), 1, (255, 255, 255))
    screen.blit(f, (node.position[0]-5, node.position[1]-5))

graph = Graph.Graph()

lastnodeadded = 0

g = Grapher.Grapher(graph = graph)

lastnodeadded = lastnodeadded + 1
graph.addNode(Node.Node(str(lastnodeadded), position = (300, 300)))

g.setDrawFunction(drawfunction)

g.start()


Quit = False
while not Quit:
    events = g.getEvents()
    if len(events) > 0:
        lastnodeadded = lastnodeadded + 1
        graph.addNode(Node.Node(str(lastnodeadded), position = (random.randint(0, 600), random.randint(0, 600))))
        if lastnodeadded > 4:
            numtoadd = random.randint(2, 4)
            for i in range(0, numtoadd):
                graph.addRelationship(str(lastnodeadded), random.choice(graph.nodes.keys()))
        else:
            graph.addRelationship(str(lastnodeadded), str(lastnodeadded-1))
    time.sleep(0.2)
