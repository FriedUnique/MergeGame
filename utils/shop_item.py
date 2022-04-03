from utils import Vector2, Button, Text

import pygame
pygame.init()

class ShopItem:
    def __init__(self, pos: Vector2, itemName: str, descriptionText: str, fulfillment):
        """fulfillment: function which is called when the buyButton is clicked"""
        self.font = pygame.font.Font(None, 32)
        self.isToggled = True

        self.position = pos
        self.buyButton = Button("buyButton", pos, Vector2(int(self.font.size(itemName)[0]/10)+2, int(self.font.size(itemName)[1]/10)+2), itemName, onClicked=fulfillment,
                                normalBackground=(38, 41, 84), onHoverBackground=(31, 36, 76), textColor=(255, 255, 255))

        self.description = Text(Vector2(15, 480), text=descriptionText, color=(255, 255, 255))

    def draw(self, screen):
        if not self.isToggled: return

        self.buyButton.draw(screen)

        if self.buyButton.state == Button.ButtonStates.Hover:
            pygame.draw.rect(screen, (255, 255, 255), (0, 475, 550, 550))
            self.description.draw(screen)

    def update(self):
        if not self.isToggled: return

        self.buyButton.handleEvents(None)

    def toggle(self):
        self.isToggled = not self.isToggled

        self.buyButton.isActive = self.isToggled
        self.description.isActive = self.isToggled
