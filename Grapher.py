#this object is going to contain a graph which is in turn going to contain a bunch of nodes.
#The primary thing this class does is draw the nodes. This is the level that the camera is implemented at.
#the user can supply a function to draw nodes on the graph.
#the function takes a node and a camera and is used to draw every node on the graph
#the grapher object also completely handles scrolling around the map, so that does not count as input.

#as of right now this class contains an infinite while loop. This may need to
#be changed if we are to make this useful in other applications

import Graph
import Node
import pygame
from pygame.locals import *
import time


g = Graph.Graph()
n = Node.Node("UID1")
#n.static = True
n.position = (300, 300)


n2 = Node.Node("UID2")
n2.position = (10, 10)

n3 = Node.Node("UID3")
n3.position = (20, 40)

g.addNode(n)
g.addNode(n2)
g.addNode(n3)
g.addRelationship("UID1", "UID2")
g.addRelationship("UID1", "UID3")

for i in range(4, 20):
    n = Node.Node(str(i))
    n.position = (100 + i*2, 100 + i*3)
    g.addNode(n)
    if i % 2 == 0:
        g.addRelationship(n.UID, "UID1")
    if i % 3 == 0:
        g.addRelationship(str(i-1), n.UID)
        g.addRelationship(str(i-2), n.UID)
    

pygame.init()
screen = pygame.display.set_mode((600, 600))

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((20, 20, 20))


    # Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()

    # Event loop
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            print "QUIT"   

    screen.blit(background, (0, 0))

    #drawing the lines
    for r in g.relationships: #for every key in relationships set
        for i in g.relationships[r][0]:
            start = (g.nodes[r].position)
            end = (g.nodes[i].position)
            pygame.draw.aaline(
                    screen,
                    (255, 255, 255),
                    start,
                    end,
                    1)

            
    #drawing the nodes
    for n in g.nodes.values():
        intpos = (int(n.position[0]), int(n.position[1]))
        #print n.UID, intpos
        pygame.draw.circle(
                screen, 
                (0, 255, 255), 
                intpos,
                5,
                0)

    g.doPhysics(1)
    time.sleep(0.02)
    
    pygame.display.flip()
