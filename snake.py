import pygame
from random import randint
pygame.init()

canvas_color = (128,128,128)
gamemode_change = False
score = 0
reload_var = 0
frame_count = 0
screen_width = 600
screen_height = 500
grid_show = False
time = pygame.time.Clock()
canvas = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")
font_name = pygame.font.match_font('arial')


class Snake_class:
   def __init__(self):
      self.x = [40,60,80]
      self.y = [40,40,40]
      self.size = 20
      self.color = (102,0,102)
      self.head_color = (52,0,102)
      self.last_move = None
      self.frame_permove = 6 #Start speed (bigger = slower)

   def keypress(self):
      global grid_show
      global gamemode_change
      key = pygame.key.get_pressed()
      if self.last_move != 2:
         if key[pygame.K_UP] or key[pygame.K_w] and self.x[-1] >= 0 and self.x[-1] < screen_width:
            self.last_move = 1
      if self.last_move != 1:
         if key[pygame.K_DOWN] or key[pygame.K_s] and self.x[-1] >= 0 and self.x[-1] < screen_width:
            self.last_move = 2
      if self.last_move != 4 and self.last_move != None:
         if key[pygame.K_LEFT] or key[pygame.K_a] and self.y[-1] >= 0 and self.y[-1] < screen_height:
            self.last_move = 3
      if self.last_move != 3:
         if key[pygame.K_RIGHT] or key[pygame.K_d] and self.y[-1] >= 0 and self.y[-1] < screen_height:
            self.last_move = 4

      if key[pygame.K_g]:
         grid_show = True
      if key[pygame.K_h]:
         grid_show = False


      if key[pygame.K_n] and self.last_move == None:
         gamemode_change = False
      if key[pygame.K_m] and self.last_move == None:
         gamemode_change = True

      # Changing snake speed
      if key[pygame.K_1]:self.frame_permove = 1 #fastest
      if key[pygame.K_2]:self.frame_permove = 2
      if key[pygame.K_3]:self.frame_permove = 5
      if key[pygame.K_4]:self.frame_permove = 6
      if key[pygame.K_5]:self.frame_permove = 10 #slowest


   def move(self):
      if self.last_move != None:
         if frame_count % self.frame_permove == 0:
            if self.last_move == 1:
               self.y.append(self.y[-1] - self.size)
               self.x.append(self.x[-1])
            elif self.last_move == 2:
               self.y.append(self.y[-1] + self.size)
               self.x.append(self.x[-1])
            elif self.last_move == 3:
               self.x.append(self.x[-1] - self.size)
               self.y.append(self.y[-1])
            elif self.last_move == 4:
               self.x.append(self.x[-1] + self.size)
               self.y.append(self.y[-1])
            self.y.pop(0)
            self.x.pop(0)

      #game mod change mechanics
      if gamemode_change == False: 
         if self.x[-1] == screen_width + self.size:
            self.x[-1] = 0
         if self.x[-1] < 0:
            self.x[-1] = screen_width

         if self.y[-1] == screen_height + self.size:
            self.y[-1] = 0
         if self.y[-1] < 0:
            self.y[-1] = screen_height
      else:
         if self.x[-1] == screen_width + self.size:
            self.restart(True)
         elif self.x[-1] < 0:
            self.restart(True)
         if self.y[-1] == screen_height + self.size:
            self.restart(True)
         elif self.y[-1] < 0:
            self.restart(True)


      


   def check_end(self): #check snake destroy himself
      global reload_var
      for i in range(0, len(self.x)-1):
         if self.x[-1] == self.x[i] and self.y[-1] == self.y[i]:
            reload_var = True
            return reload_var

   def restart(self, check): #game restart
      global reload_var
      global score
      global gamemode_change
      if check == True:
         self.x = [40,60,80]
         self.y = [40,40,40]
         self.last_move = None
         reload_var = False
         score = 0
         gamemode_change = False
         Food.change_location()

   def draw(self): # snake body draw
      for i in range(len(self.x)-1):
         pygame.draw.rect(canvas, self.color,
           (self.x[i], self.y[i], self.size, self.size))
      pygame.draw.rect(canvas, self.head_color,
           (self.x[-1], self.y[-1], self.size, self.size))


class Food_class:
   def __init__(self):
      self.size = 20
      self.color = (255, 0, 0)
      self.x = randint(1, (screen_width / 10 / 2 - 1)) * self.size #Food random position X
      self.y = randint(1, (screen_height / 10 / 2 - 1)) * self.size #Food random position Y
      while self.x in Snake.x and self.y in Snake.y: #if food spawn in snake body, respawn it
         self.change_location()


   def draw(self):
      global score
      if self.x == Snake.x[-1] and self.y == Snake.y[-1]: #Snake eat food
         score += 100
         self.change_location()
         while self.x in Snake.x and self.y in Snake.y: #if food spawn in snake body, respawn it
            self.change_location()

         Snake.x.insert(0,Snake.x[0]) # add snake length
         Snake.y.insert(0,Snake.y[0]) # add snake length
      pygame.draw.rect(canvas, self.color,
        (self.x, self.y, self.size, self.size))

   def change_location(self):
      self.x = randint(1, (screen_width / 10 / 2 - 1)) * self.size #Food random position X
      self.y = randint(1, (screen_height / 10 / 2 - 1)) * self.size #Food random position Y


class Interface:
   def __init__(self):
      self.width = 1
      self.space = 20
      self.color = (155,2,155)
      self.border_color = (255,50,150)
      self.border_with = 4

   def draw(self):
      for i in range(1, screen_width // 10 + 1):
         pygame.draw.line(canvas, self.color,
            (i * self.space, 0),
            (i * self.space, screen_height), self.width)
      for j in range(1, screen_height // 10 + 1):
         pygame.draw.line(canvas, self.color,
            (0, j * self.space),
            (screen_width, j * self.space), self.width)

   def draw_text(surf, text, size, x, y):
      font = pygame.font.Font(font_name, size)
      text_surface = font.render(text, True, (0,255,0))
      text_rect = text_surface.get_rect()
      text_rect.midtop = (x, y)
      surf.blit(text_surface, text_rect)

   def game_mode_border(self):
      global gamemode_change
      if gamemode_change == True:
         pygame.draw.line(canvas, self.border_color, # top border
            (0, 0),
            (0, screen_height), self.border_with)
         pygame.draw.line(canvas, self.border_color, # left border
            (0, 0),
            (screen_width, 0), self.border_with)
         pygame.draw.line(canvas, self.border_color, # right border
            (screen_width-2, 0),
            (screen_width-2, screen_height), self.border_with)
         pygame.draw.line(canvas, self.border_color, # bottom border
            (0, screen_height-2),
            (screen_width, screen_height-2), self.border_with)


Grid = Interface()
Snake = Snake_class()
Food = Food_class()


def screen_update():
   global frame_count
   global grid_show
   frame_count += 1
   if frame_count >= 30:
      frame_count = 0
   canvas.fill(canvas_color)

   if grid_show == True:
      Grid.draw()
   Food.draw()
   Grid.game_mode_border()
   Snake.draw()

   Interface.draw_text(canvas, str(score), 20, screen_width / 2, 50)
   pygame.display.update()


run = True
while run:
   time.tick(30)

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         run = False

   Snake.keypress()
   Snake.move()
   Snake.restart(Snake.check_end())
   screen_update()


pygame.quit()