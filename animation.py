import pygame

pygame.init() 

WIDTH = 600 # screen width
HEIGHT = 500 # screen height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pygame animation")

FONT = pygame.font.SysFont("Times New Roman", 20)
pygame_icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(pygame_icon)

# colours
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOUR = BLACK # you can adjust this

screen.fill(BG_COLOUR) 

MOVE_RATE = 1.5 # movement rate per frame
DELAY = 5 # time of frame in ms
size = 100 # radius of pacman
close = 0 # close of pacmans mouth
close_rate = 3 # rate of closing mouth per frame

# food position, eaten, and respawn postion
food1_x = 200
eaten1 = False 
respawn1 = 400

food2_x = 400
eaten2 = False 
respawn2 = WIDTH + size*1.1

running = True # play animation
paused = False # paused

# coordinate of center
x = -size
y = 300

# instruction text
instruction_text = ["Click to toggle animation,", "Press space change size."]
text_x = 20
text_y = 20

# draw text
def drawText(display_text, font, text_col, x, y):
  display_text = font.render(display_text, True, text_col)
  screen.blit(display_text, (x,y))

# print animation
def printAnimation(text, font, start_y, start_x, text_colour):
  for line in range(len(text)): # for each line in the instructions
    y = start_y + (line*40)
    x = start_x

    output = ""

    for letter in text[line]: # prints each letter in a line one by one
      screen.fill(pygame.Color("black"))
  
      for previous_line in range(line): # prints previous lines
        previous_y = start_y + (previous_line*40)
        drawText(text[previous_line], font, (255, 255, 255), x, previous_y)

      output += letter # appends new letters to the line being outputted
      drawText(output, font, text_colour, x, y)

      for event in pygame.event.get(): # allows user to skip animation or quit the program
        if event.type == pygame.MOUSEBUTTONDOWN:
          return True
        elif event.type == pygame.QUIT:
          return False
      
      pygame.time.wait(50)
      pygame.display.flip()
  
  return True # dosen't quit the program immediately to allow pygame to end it processes by itself


# instruction animation

running = printAnimation(instruction_text, FONT, text_x, text_y, (255, 255, 255))


# main loop

while running:
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN: # check if mouse clicked to pause or unpause
      paused = not paused

    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # check if e key pressed to change size
      if size == 100:
        size /= 2 
        close //= 2
      else:
        size *= 2
        close //= 2

    elif event.type == pygame.QUIT:
      running = False
    
  if paused:
    continue
  x += MOVE_RATE
  
  screen.fill(BG_COLOUR)

  # draw instructions for program

  for line in range(len(instruction_text)):
    drawText(instruction_text[line], FONT, WHITE, text_x, (text_y+(line*40)))
    
  
  # draw pacman
  pygame.draw.circle(screen, YELLOW, (x, y), size)
  pygame.draw.circle(screen, BLACK, (x, y - (size/3)), (size/10))
  pygame.draw.polygon(screen, BG_COLOUR, [(x, y), (x + size, y - size + close), (x + size, y + size - close)])

  # draw food
  if not eaten1:
    pygame.draw.circle(screen, WHITE, (food1_x, y), (size/10))
  if not eaten2:
    pygame.draw.circle(screen, WHITE, (food2_x, y), (size/10))
  
  # display frame
  pygame.display.flip()
  pygame.time.wait(DELAY)

  # checks if pacman makes contact with food
  if (x + size) > food1_x and (size - close) < (size/10):
    eaten1 = True
  if (x + size) > food2_x and (size - close) < (size/10):
    eaten2 = True

  # checks whether to respawn food in frame
  if x > respawn1:
    eaten1 = False
  if x > WIDTH + size:
    eaten2 = False

  # checks if mouth is fully open or closed and changes direction of mouth
  if close < 0:
    close_rate = -close_rate
  elif close > size:
    close_rate = -close_rate
    
  close += close_rate

  # checks the pacman is still within the frame or resets his position
  if x > respawn2:
    x = -size

pygame.quit()