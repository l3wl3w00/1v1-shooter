class EventHandler:
    def __init__(self):
        self.mouseUp = False
        self.mouseDown = False

        self.wDown = False
        self.tDown = False

        self.tHold = False
        self.spaceHold = False

        self.upDown = False
        self.spaceDown = False

        self.aHold = False
        self.dHold = False
        
        self.leftHold = False
        self.rightHold = False
        self.currEvent = None

        self.mx = 0
        self.my = 0
        self.relativeMx = 0
        self.relativeMy = 0
    def setAllFalse(self):
        self.mouseUp = False
        self.mouseDown = False

        self.wDown = False
        self.tDown = False

        self.upDown = False
        self.spaceDown = False

        self.currEvent = None