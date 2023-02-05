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
        # self.aDown = False
        # self.sDown = False
        # self.dDown = False
        # self.leftDown = False
        # self.rightDown = False
        # self.downDown = False
        # self.wUp = False
        # self.aUp = False
        # self.sUp = False
        # self.dUp = False
        # self.tUp = False
        # self.wHold = False
        # self.sHold = False
    def setAllFalse(self):
        self.mouseUp = False
        self.mouseDown = False

        self.wDown = False
        self.tDown = False

        self.upDown = False
        self.spaceDown = False

        self.currEvent = None