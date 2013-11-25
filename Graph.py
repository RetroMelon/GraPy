import Node
#The graph object contains a bunch of nodes and is responsible for maintaining
#the datastructure of nodes. and having physics act upon them

#the main datastructure is a dictionary of nodes. where the key is the UID and the value is the node
#the other datastructure is of all of the relationships.
#this datastructure uses the UID as a key
#the value is a list like this[[outgoingrelationships as UIDs], [incomingrelationships as UIDs]]

class Graph:

    nodes = {}
    relationships = {}

    nodestofind = 10 #each node is affected by its 10 closest neighbours

    #we need add and remove methods for nodes and relationships

    #adds a node to the dictionary. if the node already exists, remove the old one and add this one in place
    def addNode(self, node):
        if node.UID in self.nodes:
            self.removeNode(node.UID)

        self.nodes[node.UID] = node
        self.relationships[node.UID] = [[],[]]

    def removeNode(self, node):
        for outgoingrelation in relationships[node.UID][0]:
            removeRelationship(node.UID, outgoingrelation)
            #relationships[outgoingrelation][1].remove(node.UID)

        for incomingrelation in relationships[node.UID][1]:
            removeRelationship(incomingrelation, node.UID)
            #relationships[incomingrelation][0].remove(node.UID)

        del self.relationships[node.UID]
        del self.nodes[node.UID]

    def removeRelationship(self, outgoing, incoming):
        self.relationships[outgoing].remove(incoming)
        self.relationships[incoming].remove(outgoing)

    def addRelationship(self, outgoing, incoming):
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
                #print "calculating an attractive force for node", nodeUID
                fx, fy = self.nodes[nodeUID].calculateAttractiveForce(self.nodes[outgoingrelationUID])
                #print fx, fy
                self.nodes[nodeUID].applyForce((fx, fy))
                self.nodes[outgoingrelationUID].applyForce((-fx, -fy))

    #right now this method calculates repulsive forces for all nodes on the graph, but in future
    #a goood optimisation is only to calculate it for the closest nodes
    def calculateRepulsiveForces(self):
        for n in self.nodes.values():
            for m in self.nodes.values():
                if n == m:
                    continue
                n.applyForce(n.calculateRepulsiveForce(m))

    #applies each node's forces to it
    def moveAllNodes(self, timeinterval):
        for n in self.nodes.values():
            n.move(timeinterval)
