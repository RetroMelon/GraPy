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
from threading import *


class Grapher:

    #all draw functions must take a screen, node and camera position (as tuple)
    def defaultdrawfunction(self, screen, node, graph, cameraposition):
        pass

    graph = None
    
    drawfunction = None
    size = (600, 600)

    running = False
    _quit = False #this can be changed using the stop() function with either another thread or the exit button at the top of the screen. When it does, the while loop in the thread breaks

    _thread = None
    _lock = None

    _eventslist = []

    def __init__(self, graph = None, size = (600, 600), drawfunction = None):
        if graph == None:
            self.graph = Graph.Graph()
        else:
            self.graph = graph

        self.size = size
        
        if drawfunction == None:
            self.drawfunction = self.defaultdrawfunction
        else:
            self.drawfunction = drawfunction

        self._lock = Lock()
            

    def setGraph(self, graph):
        self.graph = graph

    def setDrawFunction(self, drawfunction):
        self.drawfunction = drawfunction

    def getEvents(self):
        e = self._eventslist[:]
        self._eventslist = []
        return e
        
    def start(self):
        self._thread = Thread(target = self._run)
        self._thread.start()

    #the main function which will be run in a separate thread
    def _run(self):
        self.running = True
        pygame.init()
        screen = pygame.display.set_mode((600, 600))

        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((20, 20, 20))


        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        #the main loop
        while not self._quit:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self._quit = True
                else:
                    printstring = "EVENT:", event.type
                    if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                        printstring = printstring, ",", str(event.key)
                        self._eventslist = self._eventslist + [printstring]

            screen.blit(background, (0, 0))

            self._lock.acquire(1)

                #drawing the lines
            for r in self.graph.relationships: #for every key in relationships set
                for i in self.graph.relationships[r][0]:
                    start = (self.graph.nodes[r].position)
                    end = (self.graph.nodes[i].position)
                    pygame.draw.aaline(
                                    screen,
                                    (255, 255, 255),
                                    start,
                                    end,
                                    1)

            #drawing the nodes
            for n in self.graph.nodes.values():
                self.drawfunction(screen, n, self.graph, (0, 0))

            self.graph.doPhysics(1)

            self._lock.release()
            
            time.sleep(0.02)
	
            pygame.display.flip()
	
