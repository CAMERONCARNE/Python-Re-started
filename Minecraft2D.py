#----------------------------
# /\/\/\/\/\/\/\/\/\/\/\/\/\/
# Make this game yourself at
# usingpython.com/pygame
# \/\/\/\/\/\/\/\/\/\/\/\/\/\
#----------------------------

import pygame, sys, random
from pygame.locals import *

fpsClock = pygame.time.Clock()

#constants representing colours
BLACK = (0,   0,   0  )
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
WHITE = (255, 255, 255)

#cloud position
cloudx = -200
cloudy = 0

#constants representing the different resources
DIRT    = 0
GRASS   = 1
WATER   = 2
COAL    = 3
WOOD    = 4
FIRE    = 5
SAND    = 6
GLASS   = 7
ROCK    = 8
STONE   = 9
BRICK   = 10
DIAMOND = 11
CLOUD   = 12

#a dictionary linking resources to textures
textures =   {
                DIRT    : pygame.image.load('dirt.png'),
                GRASS   : pygame.image.load('grass.png'),
                WATER   : pygame.image.load('water.png'),
                COAL    : pygame.image.load('coal.png'),
                CLOUD   : pygame.image.load('cloud.png'),
                WOOD    : pygame.image.load('wood.png'),
                FIRE    : pygame.image.load('fire.png'),
                SAND    : pygame.image.load('sand.png'),
                GLASS   : pygame.image.load('glass.png'),
                ROCK    : pygame.image.load('rock.png'),
                STONE   : pygame.image.load('stone.png'),
                BRICK   : pygame.image.load('brick.png'),
                DIAMOND : pygame.image.load('diamond.png')
             }

#the number of each resource that we have
inventory =   {
                DIRT    : 0,
                GRASS   : 0,
                WATER   : 0,
                COAL    : 0,
                WOOD    : 0,
                FIRE    : 0,
                SAND    : 0,
                GLASS   : 0,
                ROCK    : 0,
                STONE   : 0,
                BRICK   : 0,
                DIAMOND : 0
            }

#maps each resource to the EVENT key used to place/craft it
controls = {
                DIRT    : 49,
                GRASS   : 50,
                WATER   : 51,
                COAL    : 52,
                WOOD    : 53,
                FIRE    : 54,
                SAND    : 55,
                GLASS   : 56,
                ROCK    : 57,
                STONE   : 48,
                BRICK   : 45,
                DIAMOND : 61
            }

#maps each resource to the KEYBAORD key used to place/craft it
invKeys = {
                DIRT    : '1',
                GRASS   : '2',
                WATER   : '3',
                COAL    : '4',
                WOOD    : '5',
                FIRE    : '6',
                SAND    : '7',
                GLASS   : '8',
                ROCK    : '9',
                STONE   : '0',
                BRICK   : '-',
                DIAMOND : '='
            }

#rules to make new objects
craft = {
            FIRE    : { WOOD : 2, ROCK : 2 },
            STONE   : { ROCK : 2 },
            GLASS   : { FIRE : 1, SAND : 2},
            DIAMOND : { WOOD: 2, COAL : 3},
            BRICK   : { ROCK : 2, FIRE : 1},
            SAND    : { ROCK : 2}
        }

#useful game dimensions
TILESIZE  = 20
MAPWIDTH  = 30
MAPHEIGHT = 20

#the player image
PLAYER = pygame.image.load('player.png')
#the position of the player [x,y]
playerPos = [0,0]


#a list of resources
resources = [DIRT,GRASS,WATER,COAL,WOOD,FIRE,SAND,GLASS,ROCK,STONE,BRICK,DIAMOND]
#use list comprehension to create our tilemap
tilemap = [ [DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT) ] 

#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE + 400, MAPHEIGHT*TILESIZE + 70))

pygame.display.set_caption('M I N E C R A F T -- 2 D')
pygame.display.set_icon(pygame.image.load('PLAYER.png'))

#add a font for our inventory
INVFONT = pygame.font.Font('FreeSansBold.ttf', 12)

#loop through each row
for rw in range(MAPHEIGHT):
    #loop through each column in that row
    for cl in range(MAPWIDTH):
        #pick a random number between 0 and 20
        randomNumber = random.randint(0,20)
        #if a zero, then the tile is coal
        if randomNumber == 0:
            tile = COAL
        #water if the random number is a 1 or a 2
        elif randomNumber in [1,2]:
            tile = WATER
        elif randomNumber in [3,4,5,6,7]:
            tile = GRASS
        elif randomNumber in [8,9,10]:
            tile = WOOD
        elif randomNumber in [11,12]:
            tile = ROCK
        else:
            tile = DIRT
        #set the position in the tilemap to the randomly chosen tile
        tilemap[rw][cl] = tile

while True:

    DISPLAYSURF.fill(BLACK)

    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #and the game and close the window
            pygame.quit()
            sys.exit()
        #if a key is pressed
        elif event.type == KEYDOWN:
            #if the right arrow is pressed
            if event.key == K_RIGHT and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                playerPos[0] += 1
            if event.key == K_LEFT and playerPos[0] > 0:
                #change the player's x position
                playerPos[0] -= 1
            if event.key == K_UP and playerPos[1] > 0:
                #change the player's x position
                playerPos[1] -= 1
            if event.key == K_DOWN and playerPos[1] < MAPHEIGHT -1:
                #change the player's x position
                playerPos[1] += 1
            if event.key == K_SPACE:
                #what resource is the player standing on?
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                #player now has 1 more of this resource
                inventory[currentTile] += 1
                #the player is now standing on dirt
                tilemap[playerPos[1]][playerPos[0]] = DIRT

            for key in controls:

                #if this key was pressed
                if (event.key == controls[key]):

                    #CRAFT if the mouse is also pressed
                    if pygame.mouse.get_pressed()[0]:

                        #if the item can be crafted
                        if key in craft:

                            #keeps track of whether we have the resources
                            #to craft this item
                            canBeMade = True
                            #for each item needed to craft...
                            for i in craft[key]:
                                #...if we don't have enough...
                                if craft[key][i] > inventory[i]:
                                    #...we can't craft it!
                                    canBeMade = False
                                    break
                            #if we can craft it (we have all needed resources)
                            if canBeMade == True:
                                #take each item from the inventory
                                for i in craft[key]:
                                    inventory[i] -= craft[key][i]
                                #add the crafted item to the inventory
                                inventory[key] += 1
                                
                    #PLACE if the mouse wasn't pressed
                    else:

                        #get the tile the player is standing on
                        currentTile = tilemap[playerPos[1]][playerPos[0]]
                        #if we have the item to place
                        if inventory[key] > 0:
                            #take it from the inventory
                            inventory[key] -= 1
                            #swap it with the tile we are standing on
                            inventory[currentTile] += 1
                            #place the item
                            tilemap[playerPos[1]][playerPos[0]] = key
                    
    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct image
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE,row*TILESIZE))
        
    #display the player at the correct position 
    DISPLAYSURF.blit(PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))

    #display the cloud
    DISPLAYSURF.blit(textures[CLOUD].convert_alpha(),(cloudx,cloudy))
    #move the cloud to the left slightly
    cloudx+=1
    #if the cloud has moved past the map
    if cloudx > MAPWIDTH*TILESIZE:
        #pick a new position to place the cloud
        cloudy = random.randint(0,(MAPHEIGHT*TILESIZE) - 150)
        cloudx = -200


    #draw a rectangle behind the instructions
    pygame.draw.rect(DISPLAYSURF, BLACK, (MAPWIDTH*TILESIZE,0,200,MAPHEIGHT*TILESIZE))

    #display the inventory, starting 10 pixels in
    xPosition = 10
    
    for item in resources:
        #add the image
        DISPLAYSURF.blit(textures[item],(xPosition,MAPHEIGHT*TILESIZE+20))
        xPosition += 30
        #add the text showing the amount in the inventory
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj,(xPosition,MAPHEIGHT*TILESIZE+20))

        #display the key
        textObj = INVFONT.render("Key : " + invKeys[item], True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj,(xPosition-TILESIZE,MAPHEIGHT*TILESIZE+20+TILESIZE))

        #move along to place the next inventory item
        xPosition += 50
   
    #add the text showing the instructions
    craftText = INVFONT.render("Minecraft 2D", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,10)) 
    craftText = INVFONT.render("SPACE = Pick up tile", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,40))
    craftText = INVFONT.render("Number keys = Place tile", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,60))
    craftText = INVFONT.render("Mouse + Number keys = Craft tile", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,80))
    craftText = INVFONT.render("Crafting Rules", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,120))
    craftText = INVFONT.render("fire = 2x rock + 2x wood", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,140))
    craftText = INVFONT.render("stone = 2x rock", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,160))
    craftText = INVFONT.render("glass = 2x fire + 1x sand", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,180))
    craftText = INVFONT.render("diamond = 2x wood + 3x coal", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,200))
    craftText = INVFONT.render("brick = 2x rock + 2x fire", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,220))
    craftText = INVFONT.render("sand = 2xrock", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,240))
    craftText = INVFONT.render("Make this game at usingpython.com/pygame", True, WHITE, BLACK)
    DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,280))

    #update the display
    pygame.display.update()
    #create a short delay
    fpsClock.tick(24)
