from utils import Vector2, Button

import pygame
pygame.init()

class Text:
    """
    Displays the text when the 'draw(surface)' method is called.
    """
    def __init__(self, position = Vector2(0, 0), color = (255, 255, 255), font = pygame.font.Font(None, 32), text = "", active=True):
        self.text = text
        self.color = color
        self.font = font
        self.position = position

        self.isActive = active

        self.txt_surface = font.render(self.text, True, self.color) #change

    def blit_text(self, surface, text, pos, font):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, True, self.color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def draw(self, surface):
        if not self.isActive: return
        
        self.blit_text(surface, self.text, (self.position.x, self.position.y), self.font)
    
    def changeText(self, newText: str):
        self.text = newText
    
    def SetActive(self, activate):
        self.isActive = activate


class SplashText:
    def __init__(self, sWidth, sHeight):
        self.sDim = (sWidth, sHeight)
        w, h = int(sWidth/2), int(sHeight/2)

        self.bgColor = (0, 0, 0)
        self.textColor = (255, 0, 0)

        self.text = Text(Vector2(w, h), color=self.textColor, active=False, font=pygame.font.Font(None, 40))
        self.closeButton = Button("okButton", Vector2(w, sHeight-50), Vector2(15, 6), text="MENU", onClicked=self.accept, active=False)

        self.isToggled = False
        self.acceptFunction = None

    def update(self, _screen):
        if(self.isToggled):
            pygame.draw.rect(_screen, self.bgColor, (0, 0, self.sDim[0], self.sDim[1]))

            self.text.draw(_screen)
            self.closeButton.draw(_screen)
            self.closeButton.handleEvents(None)

    def accept(self, _b):
        # close popup 
        if self.acceptFunction != None: self.acceptFunction()

        self.text.SetActive(False)
        self.closeButton.SetActive(False)
        
        self.isToggled = False

    def loadInfo(self, msg: str, bText: str, f = None):
        self.text.color = self.textColor

        if f != None: self.acceptFunction = f

        self.closeButton.changeText(bText)
        self.closeButton.SetActive(True)

        self.text.changeText(msg)
        self.text.SetActive(True)
        self.isToggled = True

