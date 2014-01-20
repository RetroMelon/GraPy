#right click a node to crawl it.
#after it has been crawled, a few links will show up for it.
#if you want more nodes to show up for it, click it again.

from FDGraph import *
from crawlingfunctions import *
from threading import *
import pygame

#takes two tuples with two values each, and returns a tuple with the value t1-t2
def tupleSubtract(tuple1, tuple2):
    return (tuple1[0]-tuple2[0], tuple1[1]-tuple2[1])

#adds a new node to the graph near it's parent. assumes that it hasn't been crawled
def addnewnode(graph, name, parent):
    parentposition = graph.nodes[parent].position
    nodeposition = (parentposition[0] + 30, parentposition[1]+30)
    n = Node.Node(name, position = nodeposition)
    n.data = [0, 0, 0]
    n.data[0] = False
    n.data[1] = []
    n.data[2] = 0

    graph.addNode(n)
    graph.addRelationship(name, parent)

#spawns a new node near a given parent node
def spawnfrommetadata(graph, parent):
    if not len(graph.nodes[parent].data[1]) > 0:
        return

    #taking note of the new node name before removing it from the parent node's list
    newnodename = graph.nodes[parent].data[1][0]
    graph.nodes[parent].data[1] = graph.nodes[parent].data[1][1:]

    #checking to make sure the node doesn't already exist
    print newnodename
    if newnodename in graph.nodes:
        spawnfrommetadata(graph, parent)
    else:
        addnewnode(graph, newnodename, parent)
        

#takes a graph to add the new node to. adds a true statement to the node's metadata along with a list of all of the pages crawled to the node's extra data, and the size of this list as the second element
#does the following:
#finds unique links on page
#the node should already exist, so update the node metadata to say it's been crawled
#create a few new nodes from it's metadata, and remove them from the metadata
def crawlthread(graph, page):
    print "CURRENTLY CRAWLING:", page
    uniquelinks = findlinksonpage(page)

    graph.lock()
    graph.nodes[page].data[0] = True
    graph.nodes[page].data[1] = uniquelinks
    graph.nodes[page].data[2] = len(uniquelinks)

    if len(uniquelinks) > graph.data[0]:
        graph.data[0] = len(uniquelinks)

    for i in range(0, 5):
        spawnfrommetadata(graph, page)

    graph.unlock()


#a custom draw function for the nodes.
def customdraw(screen, node, graph, position):
    #n produces a colour gradient between 0 and 254 depending on the number of relationships
    #n = (((1 + 1.0/(0.35*(relationships+1)))**(0.35*relationships)-1)/1.71828)*254 #tends to 254 as relaitonships tend to infinity

    #if the node has not been crawled, colour it grey.
    #if the node has been crawled, colour it more red depending on how many links it still has left to pop up, and totally blue when that is none.
    if node.data[0]: #if it has been crawled
        importance = float(node.data[2]) / graph.data[0] #ranges from 0 to 1. 1 being the most important
        node.radius = int(8 + 20 * importance)
        pygame.draw.circle(screen, (int(255*importance), 0, 255-int(255*importance)), position, node.radius, 0)

        f = pygame.font.Font(None, 20).render(node.UID, 1, (255, 255, 255))
        f2 = pygame.font.Font(None, 20).render(str(len(node.data[1]))+"/"+str(node.data[2]), 1, (255, 255, 255))
        screen.blit(f, tupleSubtract(position, (0, -10)))#blitting the text with an x offset of 15 pixels
        screen.blit(f2, tupleSubtract(position, (0, -23)))
    else:
        node.radius = 8
        pygame.draw.circle(screen, (100, 100, 100), position, node.radius, 0)

        f = pygame.font.Font(None, 20).render(node.UID, 1, (255, 255, 255))
        screen.blit(f, tupleSubtract(position, (0, -10)))#blitting the text with an x offset of 15 pixels
    

#assumes the graph is currently locked
def registernodeclick(graph, name):
    node = graph.nodes[name]
    if node.data[0]: #if it has been crawled, pop another node from its metadata
        spawnfrommetadata(graph, name)
    else:
        t = Thread(target = crawlthread, args = (graph, name))
        t.start()
    
print "SETTING UP GRAPH AND GRAPHER..."
graph = Graph.Graph()
graph.data = [1]
g = Grapher.Grapher(graph = graph)
g.setNodeDrawFunction(customdraw)
print "SETUP COMPLETE..."

tocrawl = raw_input("\nWhich wikipedia page should we crawl?   ")

n = Node.Node(tocrawl)
n.data = [0, 0, 0]
n.data[0] = False
n.data[1] = []
n.data[2] = 0

graph.addNode(n)

g.start()

while True:
    graph.lock()
    events = g.getEvents()
    for e in events:
        print e
        if e[0] == 1 and e[1] == 3 and e[2] != None:
            registernodeclick(graph, e[2])

    graph.unlock()
    
