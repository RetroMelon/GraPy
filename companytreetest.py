from FDGraph import *
import random

#we read a list of names from a text file just for some random UID's
names = []
num = 1

def getname():
    global names, num
    
    name = ""
    if len(names)!=0:
        name = names[0]
        names = names[1:]
    else:
       num = num+1
       name = str(num)
    return name



namesfile = open("names.txt", "r")
names = names + ["BOSS"]
for line in namesfile:
    if len(line)<3:
        continue
    names = names + [line[:-1]]

graph = Graph.Graph()
g = Grapher.Grapher(graph = graph)
g.size = (1500, 1000)

Grapher.MINIMUM_SPRING_SIZE = 25
Grapher.REPULSIVE_FORCE_CONSTANT = 10000
Grapher.FRICTION_COEFFICIENT = 0.005



layers = []
numberoflayers = 6

name = getname()

graph.addNode(Node.Node(name))
layers = layers+[[name]]

for layerno in range(2, numberoflayers):
    layers = layers + [[]]
    nodesonthislayer = len(layers[layerno-1-1])*3
    for i in range(0, nodesonthislayer):
        name = getname()
        
        graph.addNode(Node.Node(name, mass = 0.5, position = (random.randint(0, 1000), random.randint(0, 1000))))
        twonodes = (random.choice(layers[layerno-1-1]), name)
        graph.addRelationship(twonodes[0], twonodes[1])
        
        layers[layerno-1] = layers[layerno-1] + [name]

g.start()
