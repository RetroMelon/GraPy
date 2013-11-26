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
import random

g = Graph.Graph()

totalnodes = 7

for i in range(1, totalnodes):
    numberofconnections = random.randint(1, 4)
    if numberofconnections >= i:
        numberofconnections = 0

    g.addNode(Node.Node(str(i), position = (random.randint(1, 600), random.randint(1, 600))))

    if not i<=2:
        relationslist = []
        for j in range(0, numberofconnections):
            relation = random.choice(range(1, i-1))
            if not relation in relationslist:
                g.addRelationship(str(i), str(relation))
                relationslist = relationslist + [relation]
    

pygame.init()
screen = pygame.display.set_mode((600, 600))

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((20, 20, 20))


    # Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()


while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            print "QUIT"
        elif event.type == pygame.KEYDOWN:
            numberofconnections = random.randint(1, 4)
            if numberofconnections >= totalnodes:
                numberofconnections= 0

            g.addNode(Node.Node(str(totalnodes), position = (random.randint(1, 600), random.randint(1, 600))))

            relationslist = []
            if numberofconnections != 0:
                for j in range(0, numberofconnections):
                    relation = random.choice(range(1, totalnodes-2))
                    if not relation in relationslist:
                        g.addRelationship(str(totalnodes), str(relation))
                        relationslist = relationslist + [relation]

            totalnodes = totalnodes + 1

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
