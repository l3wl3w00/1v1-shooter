import pygame
from TextButton import TextButton
class InputText(TextButton):
    def __init__(self,game,pos,func):
        
        super().__init__(
            pos,"",None,reactToUp = True,
            bgColor = (255,255,255),borderColor = (0,0,0)
        )
        self.onEnter = func
        self.game = game

        self.active = False

    def tick(self):
        if self.game.handler.mouseUp:
            if self.mouseOver():
                self.active = True
            else:
                self.active = False
        if self.active:
            if self.game.handler.currEvent == None:
                return
            
            if (self.game.handler.currEvent.unicode.isalpha() or self.game.handler.currEvent.unicode.isnumeric()
            or self.game.handler.currEvent.key == pygame.K_SPACE) and len(self.text)<=12:
                self.text += self.game.handler.currEvent.unicode
            elif self.game.handler.currEvent.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif self.game.handler.currEvent.key == pygame.K_RETURN:
                self.onEnter()
                self.text = ""
                
                # createMap(SaveWin.inputText.text)
                # SaveWin.inputText.text = ""