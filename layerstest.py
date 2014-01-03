import random
import Node
import Graph
import Grapher

graph = Graph.Graph()
g = Grapher.Grapher(graph = graph)
g.size = (1500, 1000)

Grapher.MINIMUM_SPRING_SIZE = 25
Grapher.REPULSIVE_FORCE_CONSTANT = 10000



layers = []
numberoflayers = 6
lastnodeadded = 0

lastnodeadded = lastnodeadded+1

graph.addNode(Node.Node(str(lastnodeadded)))
layers = layers+[[str(lastnodeadded)]]

for layerno in range(2, numberoflayers):
    layers = layers + [[]]
    nodesonthislayer = len(layers[layerno-1-1])*3
    for i in range(0, nodesonthislayer):
        lastnodeadded = lastnodeadded + 1
        
        graph.addNode(Node.Node(str(lastnodeadded), position = (random.randint(0, 1000), random.randint(0, 1000))))
        twonodes = (random.choice(layers[layerno-1-1]), str(lastnodeadded))
        graph.addRelationship(twonodes[0], twonodes[1])
        
        layers[layerno-1] = layers[layerno-1] + [str(lastnodeadded)]

g.start()
