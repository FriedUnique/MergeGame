from utils import Vector2, roundTupleValues

import pygame
from enum import Enum

pygame.init()


class Button:
    """
    Custom Button Class. Kinda shit but it does the job. A more thought through on GitHub.
    """
    class TextAlignement(Enum):
        TopLeft = 1
        TopMiddle = 2
        TopRight = 3

        CenterLeft = 4
        CenterMiddle = 5
        CenterRight = 6

        BottomLeft = 7
        BottomMiddle = 8
        BottomRight = 9

    class ButtonStates(Enum):
        Idle = 1
        Hover = 2
        Pressing = 3

    def __init__(self, name = "Button", position = Vector2(0, 0), scale = Vector2(1, 1), text = "Button", textColor = (0, 0, 0), fontSize = 32,
                normalBackground = (255, 255, 255), onHoverBackground = (220, 230, 235), onPressedBackground = (220, 230, 235), onClicked=None, active=True):
        """
        onClicked is a listener function, will be called when button object is clicked
        """
        self.position = Vector2(position.x - int(10*scale.x/2), position.y - int(10*scale.y/2))
        self.scale = scale
        self.name = name
        self.isActive = active
        self.ta = Button.TextAlignement.CenterMiddle
        self.state: Button.ButtonStates = Button.ButtonStates.Idle

        self.buttonRect = pygame.Rect((self.position.x, self.position.y, 10*scale.x, 10*scale.y))

        self.textColor = textColor
        self.font = pygame.font.Font(None, fontSize)

        self.textPos = (position.x, position.y)
        self.listener = onClicked
        
        #customization
        self.text = text
        self.changeText(self.text)

        self.colors = {
            Button.ButtonStates.Idle: normalBackground,
            Button.ButtonStates.Hover: onHoverBackground,
            Button.ButtonStates.Pressing: onPressedBackground
        }

        
    def alignText(self):
        textW, textH = self.font.size(self.text)
        x = self.position.x
        y = self.position.y
        w = self.scale.x*10
        h = self.scale.y*10

        if(self.ta == Button.TextAlignement.CenterMiddle):
            self.textPos = (x + w/2 - textW/2, y + h/2 - textH/2)
        else:
            raise ValueError(f"{self.ta.name} not implemented yet, or it is a bad type!")

        self.textPos = roundTupleValues(self.textPos)

    def draw(self, surface):
        if not self.isActive: return
        
        pygame.draw.rect(surface, self.colors[self.state], self.buttonRect)
        surface.blit(self.txt_surface, self.textPos)
    
    def handleEvents(self, _e):
        if not self.isActive: return

        try:
            if pygame.mouse.get_pressed()[0]:
                if self.buttonRect.collidepoint(pygame.mouse.get_pos()):
                    self.state = Button.ButtonStates.Pressing

                    if self.listener != None: self.listener(self) # feeds one positional argument, the button object

                else:
                    self.state = Button.ButtonStates.Idle
            elif not pygame.mouse.get_pressed()[0]:
                if self.buttonRect.collidepoint(pygame.mouse.get_pos()):
                    self.state = Button.ButtonStates.Hover
                else:
                    self.state = Button.ButtonStates.Idle
        except AttributeError:
            pass
    
    def changeTa(self, alignement: TextAlignement):
        self.ta = alignement
        self.alignText()

    def changeText(self, newText: str):
        self.text = newText
        self.alignText()
        self.txt_surface = self.font.render(self.text, True, self.textColor)

    def SetActive(self, activate):
        self.isActive = activate

"""
def alignText(self):
        textW, textH = self.font.size(self.text)
        x = self.position.x
        y = self.position.y
        w = self.scale.x*10
        h = self.scale.y*10

        #* Top
        if(self.ta == self.TextAlignement.TopLeft):
            self.textPos = (x, y)
        elif(self.ta == self.TextAlignement.TopMiddle):
            self.textPos = (x + w/2 - textW/2, y)
        elif(self.ta == self.TextAlignement.TopRight):
            self.textPos = (x + textW/2 + 5, y)

        #*Center
        elif(self.ta == self.TextAlignement.CenterLeft):
            self.textPos = (x, y + h/2 - textH/2)
        elif(self.ta == self.TextAlignement.CenterMiddle):
            self.textPos = (x + w/2 - textW/2, y + h/2 - textH/2)
        elif(self.ta == self.TextAlignement.CenterRight):
            self.textPos = (x + textW/2 + 5, y + h/2 - textH/2)

        #*Bottom
        elif(self.ta == self.TextAlignement.BottomLeft):
            self.textPos = (x, y + h - textH)
        elif(self.ta == self.TextAlignement.BottomMiddle):
            self.textPos = (x + w/2 - textW/2, y + h - textH)
        elif(self.ta == self.TextAlignement.BottomRight):
            self.textPos = (x + textW/2 + 5, y + h - textH)

        else:
            raise ValueError(f"{self.ta.name} not implemented yet, or it is a bad type!")

        self.textPos = roundTupleValues(self.textPos)

"""