#this object is going to contain a graph which is in turn going to contain a bunch of nodes.
#The primary thing this class does is draw the nodes. This is the level that the camera is implemented at.
#the user can supply a function to draw nodes on the graph.
#the function takes a node and a camera and is used to draw every node on the graph
#the grapher object also completely handles scrolling around the map, so that does not count as input.

#as of right now this class contains an infinite while loop. This may need to
#be changed if we are to make this useful in other applications

import Graph
import Node
import FramerateAverager
import pygame
import math
from pygame.locals import *
import time
import random
from threading import *

#some constants that the user can change in order to change the way the nodes act
ATTRACTIVE_FORCE_CONSTANT = 50 #10000
REPULSIVE_FORCE_CONSTANT = 10000 #30000000
MINIMUM_SPRING_SIZE = 65 #65
FRICTION_COEFFICIENT = 0.0005 #represents how much velocity the node will retain after 1 second
PER_FRAME_FRICTION_COEFFICIENT = 1 #this will be calculated whenever we change the friction coefficient or framerate

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

#takes two tuples with two values each, and returns a tuple with the value t1+t2
def tupleAdd(tuple1, tuple2):
    return (tuple1[0]+tuple2[0], tuple1[1]+tuple2[1])

#takes two tuples with two values each, and returns a tuple with the value t1-t2
def tupleSubtract(tuple1, tuple2):
    return (tuple1[0]-tuple2[0], tuple1[1]-tuple2[1])

class Grapher:

    
    #Some other draw functions that we might want to use
    #all draw functions must take a screen, node and the position of the node as a tuple after compensation for the camera's position
    def drawwithoutcolouring(self, screen, node, graph, position):
        pygame.draw.circle(screen, (50, 50, 255), position, node.radius, 0)

        f = pygame.font.Font(None, 20).render(node.UID, 1, (255, 255, 255))
        screen.blit(f, tupleSubtract(position, (5, 5)))#blitting the text with a 5 pixel offset

    #all draw functions must take a screen, node and the position of the node as a tuple after compensation for the camera's position
    def defaultnodedrawfunction(self, screen, node, graph, position):
        relationships = len(graph.relationships[node.UID][0]) + len(graph.relationships[node.UID][1])

        #n produces a colour gradient between 0 and 254 depending on the number of relationships
        n = (((1 + 1.0/(0.35*(relationships+1)))**(0.35*relationships)-1)/1.71828)*254 #tends to 254 as relaitonships tend to infinity

        pygame.draw.circle(screen, (int(n), 0, 255-int(n)), position, node.radius, 0)

        f = pygame.font.Font(None, 20).render(node.UID, 1, (255, 255, 255))
        screen.blit(f, tupleSubtract(position, (5, 5)))#blitting the text with a 5 pixel offset

    def defaultvertexdrawfunction(self, screen, start, end):
        pygame.draw.aaline(screen, (255, 255, 255), start, end, 1)

    def defaultbackgrounddrawfunction(self, screen, cameraposition):
        screen.fill((20, 20, 20))

    def defaultforegrounddrawfunction(self, screen, cameraposition):
        pass

    graph = None

    backgrounddrawfunction = None
    nodedrawfunction = None
    linedrawfunction = None
    foregrounddrawfunction = None
    
    size = (800, 600)
    camera = None

    running = False
    _quit = False #this can be changed using the stop() function with either another thread or the exit button at the top of the screen. When it does, the while loop in the thread breaks

    _targetframerate = 50
    _realframerate = _targetframerate
    _frametime = 1000/_targetframerate #this is the time the current frame took to execute
    _frameaverager = None    
    
    _thread = None

    # 0 - the mouse is unclicked and not performing any tasks, 1 - the mouse is controlling a node, 2 - the mouse is controlling the camera
    _mousemode = 0 
    _lastmousepos = (0, 0)
    _clickednode = None
    _clickednodestatic = False
    
    _eventslist = []

    def __init__(self, graph = None, size = (800, 600), nodedrawfunction = None, vertexdrawfunction = None, framerate = 50):
        if graph == None:
            self.graph = Graph.Graph()
        else:
            self.graph = graph

        self.size = size
        
        if nodedrawfunction == None:
            self.nodedrawfunction = self.defaultnodedrawfunction
        else:
            self.nodedrawfunction = nodedrawfunction

        if vertexdrawfunction == None:
            self.vertexdrawfunction = self.defaultvertexdrawfunction
        else:
            self.vertexdrawfunction = vertexdrawfunction

        self.camera = Camera()
        self.backgrounddrawfunction = self.defaultbackgrounddrawfunction
        self.foregrounddrawfunction = self.defaultforegrounddrawfunction

        self._frameaverager = FramerateAverager.FramerateAverager()
        _targetframerate = framerate


    def setGraph(self, graph):
        self.graph = graph

    def setNodeDrawFunction(self, nodedrawfunction):
        self.nodedrawfunction = nodedrawfunction

    def setVertexDrawFunction(self, vertexdrawfunction):
        self.vertexdrawfunction = vertexdrawfunction

    def setBackgroundDrawFunction(self, backgrounddrawfunction):
        self.backgrounddrawfunction = backgrounddrawfunction

    def setForegroundDrawFunction(self, foregrounddrawfunction):
        self.foregrounddrawfunction = foregrounddrawfunction

    #this method gets a list of all of the mouse and key events since the last call.
    def getEvents(self):
        e = self._eventslist[:]
        self._eventslist = []
        return e

    
    #gets the mosue position considering the camera position
    def getRelativeMousePosition(self):
        p = pygame.mouse.get_pos()
        return (p[0] + self.camera.position[0], p[1] + self.camera.position[1])

    #returns the UID of the first node that it finds to collide with "position". "position" is a tuple of x and y coords.
    #if no nodes collide, None is returned
    def findCollidingNode(self, position):
        for n in self.graph.nodes:
                if checkCollision(self.graph.nodes[n], position):
                    return n
        return None

    #calculates the frictional coefficient for the frame, and changes the global variable
    def _calculateFrictionCoefficient(self, framerate):
        global PER_FRAME_FRICTION_COEFFICIENT
        PER_FRAME_FRICTION_COEFFICIENT = math.pow(FRICTION_COEFFICIENT, 1.0/framerate)

    def start(self):
        self._thread = Thread(target = self._run)
        self._thread.start()


    def _processInput(self):
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
        pygame.event.clear()
                        

    def _processMouseButtonClick(self, event):
        #for every mouse click we dispatch an event. a mouse event looks like
        #a tuple (eventtype(0 or click, 1 for release), eventbutton, node if clicked/None)
        #although we dispatch mouse events for mouse event 1, it is important to note that we will still drag the node around
        collidingnode = self.findCollidingNode(self.getRelativeMousePosition())
        
        #if the mouse is currently not doing anything, and we've clicked the primary mouse button, 
        if self._mousemode == 0 and event.button == 1:
            if not collidingnode == None:
                    self._clickednode = collidingnode
                    self._clickednodestatic = self.graph.nodes[collidingnode].static #taking note of whether the colliding node is static so we can reset it correctly later
                    self.graph.nodes[collidingnode].static = True
                    self._mousemode = 1
            else:
                self._mousemode = 2

        self._eventslist = self._eventslist + [(0, event.button, collidingnode)] #the code to add an event to the event queue will go here
             

    def _processMouseButtonRelease(self, event):
        collidingnode = self.findCollidingNode(self.getRelativeMousePosition())
        
        if event.button == 1:
            if self._mousemode == 1: #deselecting the node that was selected
                if self._clickednode in self.graph.nodes:
                    self.graph.nodes[self._clickednode].static = self._clickednodestatic
            self._resetmousemode()

        self._eventslist = self._eventslist + [(1, event.button, collidingnode)]


    def _processMouseMovement(self, event):
        if self._mousemode == 1:
            #we need to check if the clicked node still exists because there is a chance it could have been deleted since the last mouse move
            if self._clickednode in self.graph.nodes:
                self.graph.nodes[self._clickednode].position = self.getRelativeMousePosition()
            else:
                self._resetmousemode()
        elif self._mousemode == 2:
            self.camera.position = (self.camera.position[0] + (self._lastmousepos[0] - pygame.mouse.get_pos()[0]), self.camera.position[1] + (self._lastmousepos[1] - pygame.mouse.get_pos()[1]))
        self._lastmousepos = pygame.mouse.get_pos()


    def _resetmousemode(self):
        self._clickednode = None
        self._mousemode = 0


    #the main function which will be run in a separate thread
    def _run(self):
        self.running = True

        #setting up the pygame window
        pygame.init()
        screen = pygame.display.set_mode(self.size)

        framecount = 0
        frameclock = pygame.time.Clock()
        #The main loop
        while not self._quit:
            framecount = framecount + 1
            self._frametime = frameclock.tick_busy_loop(self._targetframerate)

            #adding a new frametime to the frameaverager and getting the average framerate
            self._frameaverager.addFrametime(self._frametime)
            self._realframerate = self._frameaverager.getAverageFramerate()
            #locking the graph datastructure so that it canot be changed while we iterate over it
            self.graph.lock()

            starttime = time.clock()
            #Processing mouse and key events
            self._processInput()
            inputtime = time.clock() - starttime

            starttime = time.clock()
            #doing all physics
            self._calculateFrictionCoefficient(self._realframerate)
            self.graph._doPhysics(self._realframerate)#self._realframerate)
            physicstime = time.clock() - starttime

            starttime = time.clock()
            #doing all drawing
            self.backgrounddrawfunction(screen, self.camera.position)
            
            for r in self.graph.relationships: #drawing lines
                for i in self.graph.relationships[r][0]:
                    start = (self.graph.nodes[r].position[0]-self.camera.position[0], self.graph.nodes[r].position[1]-self.camera.position[1])
                    end = (self.graph.nodes[i].position[0]-self.camera.position[0], self.graph.nodes[i].position[1]-self.camera.position[1])
                    self.vertexdrawfunction(screen, start, end) #we account for the camera position before passing it to the draw method

            for n in self.graph.nodes.values(): #drawing nodes
                pos = tupleSubtract(n.position, self.camera.position)
                self.nodedrawfunction(screen, n, self.graph, (int(pos[0]), int(pos[1])))

            pygame.display.flip()

            drawtime = time.clock() - starttime
            #unlocking the graph to allow other threads to use/edit it
            self.graph.unlock()

            #the slow print statements cause frametime abnormalities leading to bizarre node behaviour
            if(framecount%200 == 0):
                print "TIMES:  ", "Input", inputtime, "   Physics", physicstime, "   Draw", drawtime
                print "frametime:", self._frametime
                print "framerate used in calculation:", self._realframerate
                framecount = 0
	
        self.running = False


class Camera():

    position = (0, 0)
    velocity = (0, 0)

    friction = 0.8
