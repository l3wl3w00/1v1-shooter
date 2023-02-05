class Menu:
    def __init__(self,game,buttons):
        self.game = game
        self.buttons = buttons
    def tick(self):
        for button in self.buttons:
            if button.reactToUp:
                if self.game.handler.mouseUp:
                    if button.mouseOver():
                        if button.func != None:
                            button.func()
            else:
                if self.game.handler.mouseDown:
                    if button.mouseOver():
                        if button.func != None:
                            button.func()
            button.tick()
    def render(self):
        for button in self.buttons:
            button.render(self.game.win)