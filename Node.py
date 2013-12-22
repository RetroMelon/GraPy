import math
#the node class is one that has a UID, and some physical properties to define its location in space.
#the node class knows only of itself, so has no knowledge of which nodes it is connected to.
#it calculates all forces that would act upon itself, never forces that would act upon another node.

attractiveForceConstant = 7000
repulsiveForceConstant = 3000000
minSpringSize = 65
frictionCoefficient = 0.95

#def finds the distance as a scalar (the hypot of the x and y positions
def findDistance(node1, node2):
    d = math.hypot((node2.position[0] - node1.position[0]), (node2.position[1] - node1.position[1]))
    
    n = 0.000002 * repulsiveForceConstant

    if d < n: #this prevents the distance being tiny and the nodes flying off in to infinity
        d = n
    return d

def findDistanceTuple(node1, node2):
    return (node2.position[0]-node1.position[0]+0.01, node2.position[1]-node1.position[1]+0.01)

def findAngle(node1, node2):
    distanceTuple = findDistanceTuple(node1, node2)
    return math.atan2(distanceTuple[1], distanceTuple[0])

class Node:

    UID = ""
    
    position = (0.0, 0.0)
    velocity = (0.0, 0.0)
    acceleration = (0.0, 0.0)
    
    mass = 0.25
    static = False
    charge = 1.0

    radius = 7

    def __init__(self, uid, position = (0.0, 0.0), velocity = (0.0, 0.0), mass = 0.5, static = False, charge = 10, boundingbox = ((-5, -5), (5, 5)), neighbours = []):
        self.UID = uid
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.static = static
        self.charge = charge
        self.boundingbox = boundingbox
        self.neighbours = neighbours

    #put all get and set methods here.
    #change of plan; apparently python does not use get and set methods.

    #these methods find the force acting on SELF given the other node, not the forces self is producing on the other node.
    #when we say force we are referring to a tuple with x and y values in that order
    #a force represents the actual direction of travel of the node, so we don't need to negate the force before applying it or anything
    def calculateAttractiveForce(self, other):
        forcemagnitude = self._calcAttractiveForceMagnitude(other)
        distanceangle = findAngle(self, other)

        forcex = math.cos(distanceangle) * forcemagnitude
        forcey = math.sin(distanceangle) * forcemagnitude

        return (forcex, forcey)
        

    #calculates the total value of the attractive force
    def _calcAttractiveForceMagnitude(self, other):
        distance = findDistance(self, other)
        return attractiveForceConstant * (distance - minSpringSize) #we should perhaps add in a minimum string length later on.

    def calculateRepulsiveForce(self, other):
        forcemagnitude = self._calcRepulsiveForceMagnitude(other)
        distanceangle = findAngle(self, other)

        forcex = math.cos(distanceangle) * forcemagnitude
        forcey = math.sin(distanceangle) * forcemagnitude
        
        return (forcex, forcey)

    def _calcRepulsiveForceMagnitude(self, other):
        distancetuple = findDistanceTuple(self, other)
        return -repulsiveForceConstant*1.0*(self.charge * other.charge)/findDistance(self, other)**2#(1.0*(distancetuple[0]**2 + distancetuple[1]**2))

    def calculateAttractiveForces(self, nodeslist):
        return map(self.calculateAttractiveForce, nodeslist)

    def calculateRepulsiveForces(self, nodeslist):
        return map(self.calculateRepulsiveForces, nodeslist)

    def applyForce(self, force):
        self.acceleration = (self.acceleration[0] + force[0]/self.mass, self.acceleration[1] + force[1]/self.mass)

    def applyForces(self, forcelist):
        map(applyforce, forcelist)

    #time interval is expressed in milliseconds
    def move(self, timeinterval):
        if not self.static:
            fractiontomove = timeinterval/1000.0

            self.velocity = (self.velocity[0] + self.acceleration[0]*fractiontomove, self.velocity[1] + self.acceleration[1]*fractiontomove)
            self.velocity = (self.velocity[0]*frictionCoefficient, self.velocity[1]*frictionCoefficient)
            self.position = (self.position[0] + self.velocity[0]*fractiontomove, self.position[1] + self.velocity[1]*fractiontomove)
        self.acceleration = (0, 0)
