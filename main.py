from utils import Vector2, Text, ShopItem #SplashText, Text, Button

import pygame
import json, os, random
from dataclasses import dataclass
from typing import List

# for json encryption
from cryptography.fernet import InvalidToken
from cryptography.fernet import Fernet

saveData: dict = {}

# make a load data funciton, which uses the cryptography.fernet libarary.
# it should check wether there is a key.key data file or not and create one if needed.

def fetchDataKey():
    """Returns a dataKey. If it is new, than it will return False as the last argument in the tuple."""
    key = None
    keyDataFilePath = os.path.join("data", "key.key")

    # if key file exists
    if os.path.exists(keyDataFilePath):
        with open(keyDataFilePath, 'rb') as f:
            key = f.read()

        return (key, True)

    else:
        # if key doesnt exist
        key = Fernet.generate_key()
        with open(keyDataFilePath, "wb") as f:
            f.write(key)
        
        return (key, False)

def saveDate():
    # {"points": 1, "buffInfo": {"cooldown": 1, "mergePointsMultiplyer": 1}, "mergeItems": [{"mergeLevel": 0, "pos": [250, 250]}, {"mergeLevel": 0, "pos": [100, 250]}]}
    
    key, isOld = fetchDataKey()
    fernet = Fernet(key)

    saveData["points"] = points
    saveData["buffInfo"] = buffInfo.__dict__

    l = []
    for m in mergeItems:
        l.append(m.info.__dict__)
    saveData["mergeItems"] = l


    encryptedData = fernet.encrypt(json.dumps(saveData).encode("utf-8"))
    

    with open(os.path.join("data", "save.json"), 'wb') as f:
        f.write(encryptedData)

def loadData():
    """Will load the decrypted data into the save data dict."""
    key, isOld = fetchDataKey()
    fernet = Fernet(key)
    try:
        if not isOld:
            print('New key. Progress was lost')
            return {}

        with open(os.path.join("data", "save.json"), "rb") as f:
            x = fernet.decrypt(f.read())
            x = json.loads(x)
            print(x)
            return x

    except InvalidToken:
        # save the data, to convert.
        print("Some Error")
        return {}

x = loadData()
saveData = x if x != {} else {"points": 2, "buffInfo": {"cooldown": 0.98, "mergePointsMultiplyer": 1}, "mergeItems": [{"mergeLevel": 2, "pos": [300, 150]}, {"mergeLevel": 1, "pos": [250, 150]}, {"mergeLevel": 0, "pos": [250, 100]}]}



pygame.init()

OFFSET = Vector2(100, 100)
CELLSIZE = 50
GRIDSIZE = Vector2(7, 7)

screenX, screenY = (CELLSIZE*GRIDSIZE.x + OFFSET.x*2, CELLSIZE*GRIDSIZE.y + OFFSET.y*2)
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Merge.nigger")
clock = pygame.time.Clock()

pointsText = Text(Vector2(25, 25), (0, 0, 0))

# normaly you will have to press space to make load a new merge. progress bar fill in steps if full spawn a new mergeitem. (decrease wait time with buff ?) -> menu
# use points to manually "deliver" a new mergeitem

# score system based on merges. higher level merges give more points.
# when the "delivery" button is pressed a new merg item will appear (animation, fly-in from above)
points = int(saveData["points"])

@dataclass
class BuffInfo:
    cooldown: float # 1
    mergePointsMultiplyer: float

buffInfo = BuffInfo(saveData["buffInfo"]["cooldown"], saveData["buffInfo"]["mergePointsMultiplyer"])

@dataclass
class MergeItemInfo:
    mergeLevel:  int
    pos:    tuple

@dataclass
class Pricing:
    cooldown: int
    pointsMultiplyer: int

class Shop:
    def __init__(self):
        self.isToggled = True

        self.testItem = ShopItem(Vector2(25, 100), "Decrease Cooldown", "Decreases cooldown between clicks", self.cooldownBuy)
        
        self.itemList = [self.testItem]

        self.pricing = Pricing(
            1 + (2-buffInfo.cooldown),
            2 + (buffInfo.mergePointsMultiplyer)
        )

        self.toggle()

    #region buyFulfullment methods
    def cooldownBuy(self, b):
        global points
        if points < self.pricing.cooldown:
            return

        points = round(points-self.pricing.cooldown, 1)
        buffInfo.cooldown = round(buffInfo.cooldown - 0.01, 2)
    
    #endregion

    def draw(self):
        pygame.draw.rect(screen, (38, 41, 84), (0, 0, screenX, screenY))
        self.testItem.draw(screen)

    def update(self):
        for i, item in enumerate(self.itemList):
            # the dataclasses have to be in the same order
            price = getattr(self.pricing, list(self.pricing.__dataclass_fields__)[i])
            buffLevel = getattr(buffInfo, list(buffInfo.__dataclass_fields__)[i])
            item.update(price, points, buffLevel)

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
            print(self.info.mergeLevel)
            points += (self.info.mergeLevel+1)*buffInfo.mergePointsMultiplyer
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
#MergeItem(MergeItemInfo(0, (100, 100)))

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
    global points
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

                #debug
                elif event.key == pygame.K_MINUS:
                    points -= 1
                elif event.key == pygame.K_PLUS:
                    points += 1

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
            pointsText.color = (0, 0, 0)
        else:
            pointsText.color = (255, 255, 255)
            shop.update()
            shop.draw()

        pointsText.changeText(str(points))
        pointsText.draw(screen)

        pygame.display.update()

main()

saveDate()