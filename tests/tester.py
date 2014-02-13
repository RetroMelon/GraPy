import grapy
import random
import time
import math
import threading

graph = grapy.Graph()

lastnodeadded = 0

g = grapy.Grapher(graph = graph)

#takes a graph and a grapher (g)
def mainthread():
    global graph, g, lastnodeadded
    while g.running:
        events = g.getEvents()
        for e in events:
            print "recieved event:", e
            #if the event is a mouse click event and the mousebutton is the right click
            if e[0] == 0 and e[1] == 3:
                if not e[2] == None:
                    graph.lock()
                    graph.removeNode(e[2])
                    graph.unlock()
                else:
                    lastnodeadded = lastnodeadded + 1
                    graph.lock()
                    graph.addNode(grapy.Node(str(lastnodeadded), position = g.getRelativeMousePosition()))
                    
                    if lastnodeadded > 4:
                        numtoadd = random.randint(2, 4)
                        for i in range(0, numtoadd):
                            othernode = random.choice(graph.nodes.keys())
                            if othernode == lastnodeadded:
                                continue
                            graph.addRelationship(str(lastnodeadded), othernode)
                    else:
                        graph.addRelationship(str(lastnodeadded), str(lastnodeadded-1))
                    graph.unlock()
        time.sleep(0.2)
    print "FDGRAPHER HAS FINISHED. QUITTING MAIN THREAD..."

    

lastnodeadded = lastnodeadded + 1
graph.addNode(grapy.Node(str(lastnodeadded), position = (300, 300)))

g.start()

maint = threading.Thread(target = mainthread)
maint.start()





