from utils import Vector2, Text, ShopItem #SplashText, Text, Button

import pygame
import json, os, random
from dataclasses import dataclass
from typing import List

saveData: dict = {}
with open('save.json') as data_file:
    saveData = json.load(data_file)

pygame.init()

OFFSET = Vector2(100, 100)
CELLSIZE = 50
GRIDSIZE = Vector2(7, 7)

screenX, screenY = (CELLSIZE*GRIDSIZE.x + OFFSET.x*2, CELLSIZE*GRIDSIZE.y + OFFSET.y*2)
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Merge.nigger")
clock = pygame.time.Clock()

debug = Text(Vector2(25, 25), (0, 0, 0))


# normaly you will have to press space to make load a new merge. progress bar fill in steps if full spawn a new mergeitem. (decrease wait time with buff ?) -> menu
# use points to manually "deliver" a new mergeitem

# score system based on merges. higher level merges give more points.
# when the "delivery" button is pressed a new merg item will appear (animation, fly-in from above)
points = saveData["points"]

@dataclass
class BuffInfo:
    cooldown: int
    mergePointsMultiplyer: float

buffInfo = BuffInfo(saveData["buffInfo"]["cooldown"], saveData["buffInfo"]["mergePointsMultiplyer"])

def saveState():
    # {"points": 1, "buffInfo": {"cooldown": 1, "mergePointsMultiplyer": 1}, "mergeItems": [{"mergeLevel": 0, "pos": [250, 250]}, {"mergeLevel": 0, "pos": [100, 250]}]}

    saveData["points"] = points
    saveData["buffInfo"] = buffInfo.__dict__

    l = []
    for m in mergeItems:
        l.append(m.info.__dict__)
    saveData["mergeItems"] = l

    with open('save.json', 'w') as outfile:
        json.dump(saveData, outfile)

@dataclass
class MergeItemInfo:
    mergeLevel:  int
    pos:    tuple


class Shop:
    def __init__(self):
        self.isToggled = True

        self.testItem = ShopItem(Vector2(100, 100), "SIUUUUUUU", "I have a massive cock", self.a)

        #self.background = pygame.draw.rect(screen, (38, 41, 84), (0, 0, screenX, screenY))

    def a(self, b):
        self.toggle()

    def draw(self):
        pygame.draw.rect(screen, (38, 41, 84), (0, 0, screenX, screenY))
        self.testItem.draw(screen)

    def update(self):
        self.testItem.update()

    def toggle(self):
        self.isToggled = not self.isToggled
        
        self.testItem.toggle()

shop = Shop()

class MergeItem:
    def __init__(self, mInfo: MergeItemInfo):
        mergeItems.append(self)
        self.info = mInfo

        if self.info.pos != (-1, -1):
            self.pos = Vector2(self.info.pos[0], self.info.pos[1])
            self.info.pos = (self.pos.x, self.pos.y)
        else:
            self.randomPos()

        self.oldPos = Vector2(CELLSIZE, CELLSIZE) # if a merge or a pos is not valid
        
        self.sprite = self.loadSprite()
        self.rect = self.sprite.get_rect(topleft=(self.pos.x, self.pos.y))

    def randomPos(self):
        # improvements could be made
        others: List[Vector2] = []
        for m in mergeItems:
            if m == self: 
                continue
            others.append(m.pos)

        while True:
            self.pos = Vector2(
                int(random.randint(OFFSET.x, CELLSIZE*GRIDSIZE.x)/CELLSIZE)*CELLSIZE,
                int(random.randint(OFFSET.y, CELLSIZE*GRIDSIZE.y)/CELLSIZE)*CELLSIZE
            )
            if self.pos not in others:
                self.info.pos = (self.pos.x, self.pos.y)
                break
   

    def loadSprite(self):
        # load sprite depending on level
        # make a statement which clamps the level to the max merge level
        return pygame.image.load(os.path.join('src', f'{self.info.mergeLevel}.png'))

    def draw(self):
        self.rect = self.sprite.get_rect(topleft=(self.pos.x, self.pos.y))
        screen.blit(self.sprite, self.rect)

    def destroy(self):
        try:
            mergeItems.remove(self)
            del self
        except ValueError:
            return False
        return True

    def merge(self, other):
        global points
        other: MergeItem = other
        
        if other.info.mergeLevel != self.info.mergeLevel:
            other.pos = Vector2(other.oldPos.x, other.oldPos.y)
            print("not mergeable")
            return False

        if other.destroy():
            points += self.info.mergeLevel
            self.info.mergeLevel += 1
            self.sprite = self.loadSprite()
        else:
            other.pos = Vector2(other.oldPos.x, other.oldPos.y)
            print("did not merge")
            return False

        return True

mergeItems: List[MergeItem] = []

for x in saveData["mergeItems"]:
    MergeItem(MergeItemInfo(x["mergeLevel"], x["pos"]))



def drawGrid():
    for y in range(0, GRIDSIZE.y):
        for x in range(0, GRIDSIZE.x):
            r = pygame.Rect((x*CELLSIZE + OFFSET.x, y*CELLSIZE + OFFSET.y), (CELLSIZE, CELLSIZE))

            if (x+y) % 2 == 0:
                pygame.draw.rect(screen, (170, 215, 81), r)
            else:
                pygame.draw.rect(screen, (155, 200, 73), r)

def drawMergeObjects(selectedObject: MergeItem):
    for m in mergeItems:
        if m == selectedObject: continue
        m.draw()
    
    if selectedObject != None: selectedObject.draw()
    

def main():
    isRunning = True
    currentSelection = None

    while isRunning:
        clock.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    MergeItem(MergeItemInfo(0, Vector2(-1, -1)))
                    # instantiate a new one, will replace a button
                elif event.key == pygame.K_ESCAPE:
                    # call the menu
                    shop.toggle()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if currentSelection != None: continue

                    for i, m in enumerate(mergeItems):
                        if m.rect.collidepoint(event.pos):
                            currentSelection = i
                            m.oldPos = Vector2(m.pos.x, m.pos.y)
                            break
                            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if currentSelection == None: continue

                    currentObj: MergeItem = mergeItems[currentSelection]
                    currentObj.info.pos = (currentObj.pos.x, currentObj.pos.y)
        
                    for other in mergeItems:
                        if other == currentObj: continue
                        
                        if other.pos.x == currentObj.pos.x and other.pos.y == currentObj.pos.y:
                            other.merge(currentObj)

                    currentSelection = None

            elif event.type == pygame.MOUSEMOTION:
                if currentSelection is not None:
                    # set the boundries of the motion
                    mergeItems[currentSelection].pos.x = max(min(int(event.pos[0]/CELLSIZE), GRIDSIZE.x+1), int(OFFSET.x/CELLSIZE)) * CELLSIZE
                    mergeItems[currentSelection].pos.y = max(min(int(event.pos[1]/CELLSIZE), GRIDSIZE.y+1), int(OFFSET.y/CELLSIZE)) * CELLSIZE
        


        # drawing and updating
        if not shop.isToggled:
            screen.fill((131, 201, 190))
            drawGrid()
            drawMergeObjects(None if currentSelection == None else mergeItems[currentSelection])

            debug.changeText(str(len(mergeItems)))
            debug.draw(screen)
        else:
            shop.update()
            shop.draw()

        pygame.display.update()

main()

saveState()