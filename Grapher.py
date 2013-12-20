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


#the nodes have a radius, but for the purposes of speed/efficiency, we do a bounding box collision detection
def checkCollision(node, pos):
    if pos[0] < node.position[0] - node.radius:
        return False
    if pos[0] > node.position[0] + node.radius:
        return False
    if pos[1] < node.position[1] - node.radius:
        return False
    if pos[1] > node.position[1] + node.radius:
        return False
    return True

class Grapher:

    #all draw functions must take a screen, node and camera position (as tuple)
    def defaultnodedrawfunction(self, screen, node, graph, cameraposition):
        pass

    graph = None
    
    nodedrawfunction = None
    size = (600, 600)
    camera = None

    running = False
    _quit = False #this can be changed using the stop() function with either another thread or the exit button at the top of the screen. When it does, the while loop in the thread breaks

    _thread = None

    _mousemode = 0 # 0 - the mouse is unclicked and not performing any tasks, 1 - the mouse is controlling a node, 2 - the mouse is controlling the camera
    _lastmousepos = (0, 0)
    _clickednode = None
    _clickednodestatic = False
    
    _eventslist = []

    def __init__(self, graph = None, size = (600, 600), nodedrawfunction = None):
        if graph == None:
            self.graph = Graph.Graph()
        else:
            self.graph = graph

        self.size = size
        
        if nodedrawfunction == None:
            self.nodedrawfunction = self.defaultnodedrawfunction
        else:
            self.nodedrawfunction = nodedrawfunction

        self.camera = Camera()
            

    def setGraph(self, graph):
        self.graph = graph

    def setNodeDrawFunction(self, nodedrawfunction):
        self.nodedrawfunction = nodedrawfunction

    def getEvents(self):
        e = self._eventslist[:]
        self._eventslist = []
        return e

    def _processMouseButtonClick(self, event):
        if self._mousemode == 0 and event.button == 1:
            for n in self.graph.nodes:
                if checkCollision(self.graph.nodes[n], self.getRelativeMousePosition()): #the mouse is colliding with a node
                    self._clickednode = n
                    self._clickednodestatic = self.graph.nodes[n].static
                    self.graph.nodes[n].static = True
                    self._mousemode = 1
                    return

            #if we have reached this point it wasn't a node collision, therefore set it to camera mode
            #just making sure we've definitely deselected the clicked node here
            self._clickednode = None

            self._mousemode = 2

        elif event.button == 3:
            self._eventslist = self._eventslist + [(1, event.button)]#the code to add an event to the event queue will go here
                        
                    

    def _processMouseButtonRelease(self, event):
        if event.button == 1:
            if self._mousemode == 1: #deselecting the node that was selected
                self.graph.nodes[self._clickednode].static = self._clickednodestatic
                self.clickednode = None
                self._mousemode = 0
                return
            elif self._mousemode == 2:
                self._mousemode = 0


    def _processMouseMovement(self, event):
        if self._mousemode == 1:
            self.graph.nodes[self._clickednode].position = self.getRelativeMousePosition()
        elif self._mousemode == 2:
            self.camera.position = (self.camera.position[0] + (self._lastmousepos[0] - pygame.mouse.get_pos()[0]), self.camera.position[1] + (self._lastmousepos[1] - pygame.mouse.get_pos()[1]))
        self._lastmousepos = pygame.mouse.get_pos()


    #gets the mosue position considering the camera position
    def getRelativeMousePosition(self):
        p = pygame.mouse.get_pos()
        return (p[0] + self.camera.position[0], p[1] + self.camera.position[1])
        
    def start(self):
        self._thread = Thread(target = self._run)
        self._thread.start()

    #the main function which will be run in a separate thread
    def _run(self):
        self.running = True
        pygame.init()
        screen = pygame.display.set_mode((800, 600))

        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((20, 20, 20))


        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        #the main loop
        while not self._quit:

            self.graph.lock("grapher")

            #processing mouse and key events
            for event in pygame.event.get():
                if event.type == QUIT:
                    print "QUITTING: CLOSE BUTTON HAS BEEN CLICKED..."
                    self._quit = True
                elif event.type == MOUSEBUTTONDOWN:
                    self._processMouseButtonClick(event)
                elif event.type == MOUSEBUTTONUP:
                    self._processMouseButtonRelease(event)
                elif event.type == MOUSEMOTION:
                        self._processMouseMovement(event)
                elif event.type == KEYDOWN:
                    self._eventslist = self._eventslist + [event]
        
            screen.blit(background, (0, 0))
            

            #drawing the lines
            for r in self.graph.relationships: #for every key in relationships set
                for i in self.graph.relationships[r][0]:
                    #print "drawing relation between", r, "and", i
                    start = (self.graph.nodes[r].position[0]-self.camera.position[0], self.graph.nodes[r].position[1]-self.camera.position[1])
                    end = (self.graph.nodes[i].position[0]-self.camera.position[0], self.graph.nodes[i].position[1]-self.camera.position[1])
                    pygame.draw.aaline(
                                    screen,
                                    (255, 255, 255),
                                    start,
                                    end,
                                    1)
            #print "finished drawing relationships"

            #drawing the nodes
            for n in self.graph.nodes.values():
                #print "campos2", self.camera.position
                self.nodedrawfunction(screen, n, self.graph, self.camera.position)

            self.graph.doPhysics(1)

            self.graph.unlock("grapher")
            
            time.sleep(0.02)
	
            pygame.display.flip()

        self.running = False


class Camera():

    position = (0, 0)
    velocity = (0, 0)

    friction = 0.8
