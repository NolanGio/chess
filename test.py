import pygame, sys
pygame.init()

# set up the window
width, height =  530, 530
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chess Game")

# set up the board
board = pygame.image.load("board.png")
run = True

# main loop
while run:
    # Event poll
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False    
    
    # Draw
    screen.fill("#5F5F5F")
    screen.blit(board, (0, 0))

    # Show
    pygame.display.flip()

pygame.quit()
sys.exit()