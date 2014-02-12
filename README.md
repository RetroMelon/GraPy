GraPy
====================
By [RetroMelon](https://github.com/RetroMelon)

GraPy is a simple library that makes it easy for users to create interactive force directed graphs. It utilises PyGame to allow for custom draw functions for nodes, relationships, foreground and background of the graph. The visualisation comes with default dragging functionality for nodes, however, users can poll for mouse events in order to create their own custom behaviours. Since the visualisation runs in a separate thread, the user can add, delete and edit nodes and relationships and have their changes appear in realtime in the visualisation.

#Demo

To run any of the demos, first either install the library using the installation guide below, or copy the ```grapy``` folder in to the ```tests``` folder. navigate to the ```tests``` folder, and click any of the .py files to run.

The demo that displays most of the library's functionality is ```wikipedia_browser.py```. To use the demo, run the python file and type the name of an article you wish to search for on wikipedia (no spaces required. eg, "computing_science"). Right click a grey node to crawl the wikipedia page for the given article name. Click the node again to diplay more links for the same article. Right click any of the child nodes to search them in turn. Nodes that have been searched are coloured and sized according to how many links to other articles are present on the page. To view any of the articles in browser, middle click the node.

A screenshot of the wikipedia browser demo:

<img src="https://github.com/RetroMelon/GraPy/blob/master/docs/Wikipedia%20Browser.png?raw=true" 
alt="WIKIPEDIA BROWSER DEMO" width="400" height="329" border="10" />


#Installing

GraPy depends on the [PyGame](http://pygame.org/news.html) library. Please ensure the correct version of pygame is installed on your machine.
##Via Python Install

1. Download the [zip archive](https://github.com/RetroMelon/GraPy/archive/master.zip) or clone the repo using: ```git clone git://github.com/RetroMelon/GraPy```
2. Open a shell in the folder containing setup.py
3. For a standard install, run:

```python setup.py install```

For an install where you can edit the code in the library easily, or remove the library easily after completion, run:

```python setup.py develop```

To remove the library after use, run:

```python setup.py develop --uninstall```

##Using Without Installing

To use the library without installing it to the system, download the [zip archive](https://github.com/RetroMelon/GraPy/archive/master.zip) or clone the repo using: ```git clone git://github.com/RetroMelon/GraPy```.

Copy the "grapy" folder in to the same directory as the scripts you with to import it to. Import GraPy with the line:

```import grapy```

To use GraPy to, for example, instantiate a node object, type:

```n = grapy.Node("node ID")```

