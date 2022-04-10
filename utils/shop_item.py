from utils import Vector2, Button, Text

import pygame
pygame.init()

class ShopItem:
    def __init__(self, pos: Vector2, itemName: str, descriptionText: str, fulfillment):
        """fulfillment: function which is called when the buyButton is clicked"""
        font = pygame.font.Font(None, 32)
        self.isToggled = True
        self.canBuy = True
        self.descriptionText = descriptionText

        self.position = pos
        self.buyButton = Button("buyButton", pos, Vector2(int(font.size(itemName)[0]/10)+2, int(font.size(itemName)[1]/10)+2), itemName, onClicked=fulfillment,
                                normalBackground=(38, 41, 84), onHoverBackground=(31, 36, 76), onPressedBackground=(23, 28, 68), textColor=(255, 255, 255))

        self.description = Text(Vector2(25, 480), text=descriptionText, color=(0, 0, 0))

    def draw(self, screen):
        if not self.isToggled: return

        self.buyButton.draw(screen)

        if self.buyButton.state != Button.ButtonStates.Idle and self.canBuy:
            pygame.draw.rect(screen, (255, 255, 255), (0, 475, 550, 550))
            self.description.text = self.descriptionText
            self.description.draw(screen)
        elif self.buyButton.state != Button.ButtonStates.Idle and not self.canBuy:
            pygame.draw.rect(screen, (255, 255, 255), (0, 475, 550, 550))
            self.description.text = "Not enough moneeeyyyyyy"
            self.description.draw(screen)

    def update(self, price, points, buffLevel):
        self.canBuy = price < points
        if not self.isToggled: return

        self.buyButton.handleEvents(None)

    def toggle(self):
        self.isToggled = not self.isToggled

        self.buyButton.isActive = self.isToggled
        self.description.isActive = self.isToggled
