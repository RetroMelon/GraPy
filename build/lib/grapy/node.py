import math
import grapher
#the node class is one that has a UID, and some physical properties to define its location in space.
#the node class knows only of itself, so has no knowledge of which nodes it is connected to.
#it calculates all forces that would act upon itself, never forces that would act upon another node.

#def finds the distance as a scalar (the hypot of the x and y positions)
def findDistance(node1, node2):
    d = math.hypot((node2.position[0] - node1.position[0]), (node2.position[1] - node1.position[1]))
    return d

def findDistanceTuple(node1, node2):
    return (node2.position[0]-node1.position[0]+0.01, node2.position[1]-node1.position[1]+0.01)

def findAngle(node1, node2):
    distanceTuple = findDistanceTuple(node1, node2)
    return math.atan2(distanceTuple[1], distanceTuple[0])

class Node:

    UID = ""
    data = []
    
    position = (0.0, 0.0)
    velocity = (0.0, 0.0)
    acceleration = (0.0, 0.0)

    _forcelist = []
    
    mass = 1
    static = False
    charge = 1.0

    radius = 9

    def __init__(self, uid, position = (0.0, 0.0), velocity = (0.0, 0.0), mass = 1, static = False, charge = 10, boundingbox = ((-5, -5), (5, 5)), neighbours = []):
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
        return grapher.ATTRACTIVE_FORCE_CONSTANT * (distance - grapher.MINIMUM_SPRING_SIZE) #we should perhaps add in a minimum string length later on.

    def calculateRepulsiveForce(self, other):
        forcemagnitude = self._calcRepulsiveForceMagnitude(other)
        distanceangle = findAngle(self, other)

        forcex = math.cos(distanceangle) * forcemagnitude
        forcey = math.sin(distanceangle) * forcemagnitude
        
        return (forcex, forcey)

    
    #a function similar to that of gravitation; a parabolic fall off. the distance^2 + charge*charge part means it can never exceed the repulsive force constant
    def _calcRepulsiveForceMagnitude(self, other):
        distance = findDistance(self, other)
        if distance<15:
            distance = 15
        return -grapher.REPULSIVE_FORCE_CONSTANT*1.0*(self.charge * other.charge)/((distance*0.2)**2 + (self.charge * other.charge))

    def calculateAttractiveForces(self, nodeslist):
        return map(self.calculateAttractiveForce, nodeslist)

    def calculateRepulsiveForces(self, nodeslist):
        return map(self.calculateRepulsiveForce, nodeslist)

    def applyForce(self, force):
        self._forcelist = self._forcelist + [force]

    def applyForces(self, forcelist):
        map(applyforce, forcelist)

    #calculates the frictional force but does not apply it
    def calculateFrictionalForce(self):
        return (self.velocity[0]*-grapher.FRICTION_COEFFICIENT*self.mass, self.velocity[1]*-grapher.FRICTION_COEFFICIENT*self.mass)
        
        
    #takes the framerate of the simulation. this should be an unchanging/static framerate, and should ideally not fluctuate
    def move(self, framerate):
        if not self.static:
            self.applyForce(self.calculateFrictionalForce())

            totalforce = (0, 0)
            for f in self._forcelist:
                totalforce = (totalforce[0] + f[0], totalforce[1] + f[1])
                
            self.acceleration = (self.acceleration[0] + (totalforce[0]/self.mass), self.acceleration[1] + (totalforce[1]/self.mass))

            self.velocity = (self.velocity[0] + self.acceleration[0]/framerate, self.velocity[1] + self.acceleration[1]/framerate)

            frictionalcoefficient = grapher.PER_FRAME_FRICTION_COEFFICIENT
            self.velocity = (self.velocity[0]*frictionalcoefficient, self.velocity[1]*frictionalcoefficient)

            self.position = (self.position[0] + self.velocity[0]/framerate, self.position[1] + self.velocity[1]/framerate)

        self.acceleration = (0.0, 0.0)
        self._forcelist = []
