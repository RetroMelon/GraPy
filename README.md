GraPy (A simple force directed graph library for Python).
====================
By [RetroMelon](https://github.com/RetroMelon)

GraPy is a simple library that makes it easy for users to create interactive force directed graphs. It utilises PyGame to allow for custom draw functions for nodes, relationships, foreground and background of the graph. The visualisation comes with default dragging functionality for nodes, however, users can poll for mouse events in order to create their own custom behaviours. Since the visualisation runs in a separate thread, the user can add, delete and edit nodes and relationships and have their changes appear in realtime in the visualisation.

A screenshot of the wikipedia browser demo:

<img src="https://github.com/RetroMelon/GraPy/blob/master/docs/Wikipedia%20Browser.png?raw=true" 
alt="WIKIPEDIA BROWSER DEMO" width="400" height="329" border="10" />


#Installing

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

