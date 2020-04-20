import pygame
import numpy as np
import time

WIDTH, HEIGHT = 750, 750
nX, nY = 50, 50
xSize = WIDTH/nX
ySize = HEIGHT/nY

pygame.init() # Initialize PyGame

screen = pygame.display.set_mode([WIDTH,HEIGHT]) # Set size of screen

BG_COLOR = (0,0,0) # Define background color
LIVE_COLOR = (255,255,255)
DEAD_COLOR = (128,128,128)

status = np.zeros((nX,nY)) # Intialize status of cells

pauseRun = False

running = True
while running:

    newStatus = np.copy(status) # Copy status
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            pauseRun = not pauseRun
            
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            x, y = int(np.floor(posX/xSize)), int(np.floor(posY/ySize))
            newStatus[x,y] = np.abs(newStatus[x,y]-1)
    
    screen.fill(BG_COLOR) # Clean background
    
    for x in range(0,nX):
        for y in range(0,nY):
            
            if not pauseRun:
                
                # Number of Neighbors
                nNeigh = newStatus[(x-1)%nX,(y-1)%nY] + newStatus[(x)%nX,(y-1)%nY] + \
                        newStatus[(x+1)%nX,(y-1)%nY] + newStatus[(x-1)%nX,(y)%nY] + \
                        newStatus[(x+1)%nX,(y)%nY] + newStatus[(x-1)%nX,(y+1)%nY] + \
                         newStatus[(x)%nX,(y+1)%nY] + newStatus[(x+1)%nX,(y+1)%nY]
                
                # Rule 1: Dead cell with 3 Negihbors comes to live
                if newStatus[x,y] == 0 and nNeigh==3:
                    newStatus[x,y] = 1
                    
                # Rule 2: Live cell with less than 2 or more than 3 neighbors dies
                elif newStatus[x,y] == 1 and (nNeigh < 2 or nNeigh > 3):
                    newStatus[x,y] = 0                   
                                  
            poly = [(x*xSize,y*ySize),
                    ((x+1)*xSize,y*ySize),
                    ((x+1)*xSize,(y+1)*ySize),
                    (x*xSize,(y+1)*ySize)]
            
            if newStatus[x,y] == 1:
                pygame.draw.polygon(screen,LIVE_COLOR,poly,0)
            else:
                pygame.draw.polygon(screen,DEAD_COLOR,poly,1)
                  
    status = np.copy(newStatus)
    time.sleep(0.1)
    pygame.display.flip()
            
        
        
pygame.quit()
    
    

    