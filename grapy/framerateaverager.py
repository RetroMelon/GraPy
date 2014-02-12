class FramerateAverager:

    _numberOfFramerates = 5
    _framerates = []

    minFramerate = 20

    def __init__(self, numberofframerates = 5):
        self._numberOfFramerates = numberofframerates
        self._framerates = [50.0]*numberofframerates
        
    def addFramerate(self, framerate):
        if framerate <= self.minFramerate:
            framerate = self.minFramerate
        self._framerates = self._framerates[1:] + [framerate*1.0]

    def addFrametime(self, frametime):
        self.addFramerate(1000.0/frametime)

    def getAverageFramerate(self):
        return sum(self._framerates)/self._numberOfFramerates
