import Grapher
import Graph
import Node
import random
import time
import pygame
import math

def drawfunction(screen, node, graph, cameraposition):
    intpos = (int(node.position[0]), int(node.position[1]))
    relationships = len(graph.relationships[node.UID][0]) + len(graph.relationships[node.UID][1])

    #n produces a colour gradient between 0 and 254 depending on the number of relationships
    n = (((1 + 1.0/(0.35*(relationships+1)))**(0.35*relationships)-1)/1.71828)*254 #tends to 254 as relaitonships tend to infinity

    pygame.draw.circle(screen, (int(n), 0, 255-int(n)), (intpos[0]-cameraposition[0], intpos[1]-cameraposition[1]), node.radius, 0)

    f = pygame.font.Font(None, 20).render(node.UID, 1, (255, 255, 255))
    screen.blit(f, (node.position[0]-cameraposition[0]-5, node.position[1]-cameraposition[1]-5))

graph = Graph.Graph()

lastnodeadded = 0

g = Grapher.Grapher(graph = graph)

lastnodeadded = lastnodeadded + 1
graph.addNode(Node.Node(str(lastnodeadded), position = (300, 300)))

g.setNodeDrawFunction(drawfunction)

g.start()


Quit = False
while not Quit:
    events = g.getEvents()
    if len(events) > 0:
        removed = False
        for e in events:
            if e[0] == 1:
                for n in graph.nodes:
                    if Grapher.checkCollision(graph.nodes[n], g.getRelativeMousePosition()):
                        graph.lock()
                        graph.removeNode(n)
                        removed = True
                        graph.unlock()
                        break
        if not removed:
            lastnodeadded = lastnodeadded + 1
            graph.lock()
            graph.addNode(Node.Node(str(lastnodeadded), position = g.getRelativeMousePosition()))
            graph.unlock()
            if lastnodeadded > 4:
                numtoadd = random.randint(2, 4)
                for i in range(0, numtoadd):
                    othernode =  random.choice(graph.nodes.keys())
                    if othernode == lastnodeadded:
                        continue
                    graph.addRelationship(str(lastnodeadded), othernode)
            else:
                graph.addRelationship(str(lastnodeadded), str(lastnodeadded-1))
    time.sleep(0.2)


