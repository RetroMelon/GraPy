import node
import threading
from debug import *
#The graph object contains a bunch of nodes and is responsible for maintaining
#the datastructure of nodes. and having physics act upon them

#the main datastructure is a dictionary of nodes. where the key is the UID and the value is the node
#the other datastructure is of all of the relationships.
#this datastructure uses the UID as a key
#the value is a list like this [[outgoingrelationships as UIDs], [incomingrelationships as UIDs]]

class Graph:
    
    nodes = {}
    relationships = {} #relationships contains 2 lists for each entry. the first is outgoing, the second is incoming

    data = [] #some arbitrary data the graph can store

    _lock = threading.Lock()

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()


    #takes a node to add to the graph
    #if the node already exists, we remove it and all its relationships, and re-add it
    def addNode(self, node):     
        if node.UID in self.nodes:
            self.removeNode(node.UID)

        self.nodes[node.UID] = node
        self.relationships[node.UID] = [[],[]]


    #takes the ID of a node to remove
    def removeNode(self, nodeID):
        if not nodeID in self.nodes:
            DebugMsg("TRIED TO REMOVE NODE "+str(nodeID)+" WHICH DIDN'T EXIST.")
            return

        outgoings = self.relationships[nodeID][0][:]
        
        for outgoingrelation in outgoings:
            self.removeRelationship(nodeID, outgoingrelation)

        incomings = self.relationships[nodeID][1][:]

        for incomingrelation in incomings:
            self.removeRelationship(incomingrelation, nodeID)

        del self.relationships[nodeID]
        del self.nodes[nodeID]


    #takes the IDs of the outgoing and imconing nodes
    def removeRelationship(self, outgoing, incoming):
        if (not outgoing in self.relationships):
            DebugMsg("TRIED TO REMOVE RELATIONSHIP "+str(outgoing)+"  >  "+str(incoming)+" WHEN OUTGOING DIDN'T EXIST.")
            return
        if (not incoming in self.relationships):
            DebugMsg("TRIED TO REMOVE RELATIONSHIP "+str(outgoing)+"  >  "+str(incoming)+" WHEN INCOMING DIDN'T EXIST.")
            return
        
        self.relationships[outgoing][0].remove(incoming)
        self.relationships[incoming][1].remove(outgoing)


    #adds a directional relationship to the graph between nodes
    def addRelationship(self, outgoing, incoming):
        if (not outgoing in self.relationships):
            DebugMsg("TRIED TO ADD RELATIONSHIP "+str(outgoing)+"  >  "+str(incoming)+" WHEN OUTGOING DIDN'T EXIST.")
            return
        if (not incoming in self.relationships):
            DebugMsg("TRIED TO ADD RELATIONSHIP "+str(outgoing)+"  >  "+str(incoming)+" WHEN INCOMING DIDN'T EXIST.")
            return
        if (outgoing == incoming):
            DebugMsg("TRIED TO ADD RELATIONSHIP BETWEEN NODE "+str(outgoing)+" AND ITSELF.")
            return
        if (incoming in self.relationships[outgoing][0]):
            DebugMsg("RELATIONSHIP "+str(outgoing)+"  >  "+str(incoming)+" ALREADY EXISTS.")
            return

        #adding the relationships in the appropriate locations
        self.relationships[outgoing][0] = self.relationships[outgoing][0] + [incoming]
        self.relationships[incoming][1] = self.relationships[incoming][1] + [outgoing]


    #the function that does all of the physics calculations. takes framerate
    #we do the following things:
        #calculate and apply attractive forces
        #calculate and apply repulsive forces
        #move each node
    def _doPhysics(self, framerate):
        self._calculateAttractiveForces()
        self._calculateRepulsiveForces()

        self._moveAllNodes(framerate)


    #we go through every outgoing relationship, and for each one apply a force to both the outgoing node and incoming
    def _calculateAttractiveForces(self):
        for nodeUID in self.relationships:
            for outgoingrelationUID in self.relationships[nodeUID][0]:
                fx, fy = self.nodes[nodeUID].calculateAttractiveForce(self.nodes[outgoingrelationUID])
                self.nodes[nodeUID].applyForce((fx, fy))
                self.nodes[outgoingrelationUID].applyForce((-fx, -fy))


    #this method calculates and applies repulsive forces for each node on oneanother. 
    def _calculateRepulsiveForces(self):
        for index, node in enumerate(self.nodes.values()):
            for node2 in self.nodes.values()[index+1:]:
                fx, fy = node.calculateRepulsiveForce(node2)
                node.applyForce((fx, fy))
                node2.applyForce((-fx, -fy))


    #applies each node's forces to it
    def _moveAllNodes(self, framerate):
        for n in self.nodes.values():
            n.move(framerate)
