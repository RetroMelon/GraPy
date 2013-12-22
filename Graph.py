import Node
import threading
#The graph object contains a bunch of nodes and is responsible for maintaining
#the datastructure of nodes. and having physics act upon them

#the main datastructure is a dictionary of nodes. where the key is the UID and the value is the node
#the other datastructure is of all of the relationships.
#this datastructure uses the UID as a key
#the value is a list like this [[outgoingrelationships as UIDs], [incomingrelationships as UIDs]]

class Graph:
    
    nodes = {}
    relationships = {} #relationships contains 2 lists for each entry. the first is outgoing, the second is incoming

    _lock = threading.Lock()

    def lock(self, name):
        self._lock.acquire()

    def unlock(self, name):
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
            print "TRIED TO REMOVE NODE", nodeID, "WHICH DIDN'T EXIST."
            return
        
        for outgoingrelation in self.relationships[nodeID][0]:
            self.removeRelationship(nodeID, outgoingrelation)

        incomings = self.relationships[nodeID][1][:]

        for incomingrelation in incomings:
            self.removeRelationship(incomingrelation, nodeID)

        del self.relationships[nodeID]
        del self.nodes[nodeID]


    #takes the IDs of the outgoing and imconing nodes
    def removeRelationship(self, outgoing, incoming):
        if (not outgoing in self.relationships):
            print "TRIED TO REMOVE RELATIONSHIP", outgoing, " > ", incoming, "WHEN OUTGOING DIDN'T EXIST."
            return
        if (not incoming in self.relationships):
            print "TRIED TO REMOVE RELATIONSHIP", outgoing, " > ", incoming, "WHEN INCOMING DIDN'T EXIST."
            return
        
        self.relationships[outgoing][0].remove(incoming)
        self.relationships[incoming][1].remove(outgoing)


    #adds a directional relationship to the graph between nodes
    def addRelationship(self, outgoing, incoming):
        if (not outgoing in self.relationships):
            print "TRIED TO ADD RELATIONSHIP", outgoing, " > ", incoming, "WHEN OUTGOING DIDN'T EXIST."
            return
        if (not incoming in self.relationships):
            print "TRIED TO ADD RELATIONSHIP", outgoing, " > ", incoming, "WHEN INCOMING DIDN'T EXIST."
            return
        if (outgoing == incoming):
            print "TRIED TO ADD RELATIONSHIP BETWEEN NODE", outgoing, "AND ITSELF."
            return
        if (incoming in self.relationships[outgoing][0]):
            print "RELATIONSHIP", outgoing, " > ", incoming, "ALREADY EXISTS."
            return

        #adding the relationships in the appropriate locations
        self.relationships[outgoing][0] = self.relationships[outgoing][0] + [incoming]
        self.relationships[incoming][1] = self.relationships[incoming][1] + [outgoing]


    #the function that does all of the physics calculations. timeinterval is in miliseconds
    #we do the following things:
        #calculate and apply attractive forces
        #calculate and apply repulsive forces
        #move each node
    def doPhysics(self, timeinterval):
        self.calculateAttractiveForces()
        self.calculateRepulsiveForces()

        self.moveAllNodes(timeinterval)


    #we go through every outgoing relationship, and for each one apply a force to both the outgoing node and incoming
    def calculateAttractiveForces(self):
        for nodeUID in self.relationships:
            for outgoingrelationUID in self.relationships[nodeUID][0]:
                fx, fy = self.nodes[nodeUID].calculateAttractiveForce(self.nodes[outgoingrelationUID])
                self.nodes[nodeUID].applyForce((fx, fy))
                self.nodes[outgoingrelationUID].applyForce((-fx, -fy))


    #this method calculates and applies repulsive forces for each node on oneanother. 
    def calculateRepulsiveForces(self):
        valueslist = self.nodes.values()
        for index, node in enumerate(valueslist):
            for node2 in valueslist[index:]:
                fx, fy = node.calculateRepulsiveForce(node2)
                node.applyForce((fx, fy))
                node2.applyForce((-fx, -fy))
                

    #applies each node's forces to it
    def moveAllNodes(self, timeinterval):
        for n in self.nodes.values():
            n.move(timeinterval)
