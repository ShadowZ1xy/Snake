import pygame
from random import randint
pygame.init()

canvas_color = (128,128,128)
gamemode_change = False
score_player1 = 0
score_player2 = 0
player_add = True
frame_count = 0
screen_width = 700
screen_height = 600
grid_show = False
reload_var = False
time = pygame.time.Clock()
canvas = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")
font_name = pygame.font.match_font('arial')
    
class Snake(object):
    """Snake body class"""
    def __init__(self, x,y, size, body_color, head_color):
        self.x = [x, x+size, x+size*2]
        self.y = [y,y,y]
        self.size = size
        self.bc = body_color
        self.hc = head_color
        self.last_move = None
        self.frame_permove = 6 #Start speed (bigger = slower)
   
    def keypress(self, up, down, right, left):
        '''Snake control'''
        key = pygame.key.get_pressed()
        if (key[pygame.K_DOWN] == 0 and key[pygame.K_UP] == 1 and key[pygame.K_LEFT] == 0 and key[pygame.K_RIGHT] == 0) or (key[pygame.K_s] == 0 and key[pygame.K_w] == 1 and key[pygame.K_a] == 0 and key[pygame.K_d] == 0):
            if self.last_move != 2:
                if key[up] and self.x[-1] >= 0 and self.x[-1] < screen_width:
                    self.last_move = 1

        if (key[pygame.K_DOWN] == 1 and key[pygame.K_UP] == 0 and key[pygame.K_LEFT] == 0 and key[pygame.K_RIGHT] == 0) or (key[pygame.K_s] == 1 and key[pygame.K_w] == 0 and key[pygame.K_a] == 0 and key[pygame.K_d] == 0):
            if self.last_move != 1:
                if key[down] and self.x[-1] >= 0 and self.x[-1] < screen_width:
                    self.last_move = 2

        if (key[pygame.K_DOWN] == 0 and key[pygame.K_UP] == 0 and key[pygame.K_LEFT] == 1 and key[pygame.K_RIGHT] == 0) or (key[pygame.K_s] == 0 and key[pygame.K_w] == 0 and key[pygame.K_a] == 1 and key[pygame.K_d] == 0):
            if self.last_move != 4 and self.last_move != None:
                if key[left] and self.y[-1] >= 0 and self.y[-1] < screen_height:
                    self.last_move = 3

        if (key[pygame.K_DOWN] == 0 and key[pygame.K_UP] == 0 and key[pygame.K_LEFT] == 0 and key[pygame.K_RIGHT] == 1) or (key[pygame.K_s] == 0 and key[pygame.K_w] == 0 and key[pygame.K_a] == 0 and key[pygame.K_d] == 1):
            if self.last_move != 3:
                if key[right] and self.y[-1] >= 0 and self.y[-1] < screen_height:
                    self.last_move = 4

        # Changing snake speed
        if key[pygame.K_1]:self.frame_permove = 1 #fastest
        if key[pygame.K_2]:self.frame_permove = 2
        if key[pygame.K_3]:self.frame_permove = 5
        if key[pygame.K_4]:self.frame_permove = 6
        if key[pygame.K_5]:self.frame_permove = 10 #slowest


    def move(self):
        global reload_var
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
        if gamemode_change is False:
            if self.x[-1] == screen_width + self.size:
                self.x[-1] = 0
            if self.x[-1] < 0:
                self.x[-1] = screen_width
            if self.y[-1] == screen_height + self.size:
                self.y[-1] = 40
            if self.y[-1] < 40:
                self.y[-1] = screen_height
        else:
            if self.x[-1] == screen_width + self.size:
                reload_var = True
            elif self.x[-1] < 0:
                reload_var = True
            if self.y[-1] == screen_height + self.size:
                reload_var = True
            elif self.y[-1] < 40:
                reload_var = True

    def check_end(self): #check snake destroy himself
        global reload_var
        global player_add
        for i in range(0, len(self.x)-1):
            if self.x[-1] == self.x[i] and self.y[-1] == self.y[i]:
                reload_var = True
        if player_add is True:
            for j in range(0, len(self.x)-1):
                if Player1.x[-1] in Player2.x and Player1.y[-1] in Player2.y:
                    reload_var = True
                if Player2.x[-1] in Player1.x and Player2.y[-1] in Player1.y:
                    reload_var = True

    def draw(self): # snake body draw
        for i in range(len(self.x)-1):
            pygame.draw.rect(canvas, self.bc, 
                (self.x[i]+1, self.y[i]+1, self.size-2, self.size-2))

        pygame.draw.rect(canvas, self.hc,
                (self.x[-1], self.y[-1], self.size, self.size))



class Food(object):
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.x = randint(1, (screen_width / 10 / 2 - 1)) * self.size #Food random position X
        self.y = randint(2, (screen_height / 10 / 2 - 1)) * self.size #Food random position Y
        while self.x in Player1.x and self.y in Player1.y or self.x in Player2.x and self.y in Player2.y: #if food spawn in snake body, change spawn location
            self.change_location()

    def draw(self):
        global score_player1
        global score_player2
        if self.x == Player1.x[-1] and self.y == Player1.y[-1]: #Snake eat food
            score_player1 += 100
            self.change_location()
            while self.x in Player1.x and self.y in Player1.y: #if food spawn in snake body, change spawn location
                self.change_location()
            Player1.x.insert(0,Player1.x[0]) # add snake length
            Player1.y.insert(0,Player1.y[0]) # add snake length

        if self.x == Player2.x[-1] and self.y == Player2.y[-1]: #Snake eat food
            score_player2 += 100
            self.change_location()
            while self.x in Player2.x and self.y in Player2.y: #if food spawn in snake body, change spawn location
                self.change_location()
            Player2.x.insert(0,Player2.x[0]) # add snake length
            Player2.y.insert(0,Player2.y[0]) # add snake length

        pygame.draw.rect(canvas, self.color,
            (self.x, self.y, self.size, self.size))

    def change_location(self):
        self.x = randint(1, (screen_width / 10 / 2 - 1)) * self.size #Food random position X
        self.y = randint(2, (screen_height / 10 / 2 - 1)) * self.size #Food random position Y



class Interface(object):
    def __init__(self):
        self.width = 1
        self.space = 20
        self.color = (155,2,155)
        self.border_color = (255,50,150)
        self.border_with = 4
        self.score_color = (147,112,219)
        self.indent_score = 40
        self.first_player_score = (102,0,102)
        self.border_color = (255,50,150)
        self.border_with = 4

    def draw(self):
        for i in range(1, screen_width // 10 + 1):
            pygame.draw.line(canvas, self.color,
                (i * self.space, self.indent_score),
                (i * self.space, screen_height), self.width)
        for j in range(2, screen_height // 10 + 1):
            pygame.draw.line(canvas, self.color,
                (0, j * self.space),
                (screen_width, j * self.space), self.width)

    def score_draw(self):
        global player_add
        if player_add is True:
            pygame.draw.rect(canvas, self.first_player_score,
                (0, 0, screen_width/2, 40))
            pygame.draw.rect(canvas, (140,200,190),
                (screen_width/2, 0, screen_width, 40))
            Interface.draw_text(canvas, str(score_player1), 32, screen_width/2-screen_width/4, 2, (140,200,190))
            Interface.draw_text(canvas, str(score_player2), 32, screen_width/2+screen_width/4, 2, self.first_player_score)
        else:
            pygame.draw.rect(canvas, self.first_player_score,
                (0, 0, screen_width, 40))
            Interface.draw_text(canvas, str(score_player1), 32, screen_width/2, 2, (140,200,190))

    def draw_text(surf, text, size, x, y, color):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
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

    def control(self):
        global grid_show
        global gamemode_change
        global player_add
        key = pygame.key.get_pressed()
        if key[pygame.K_g]:
            grid_show = True
        if key[pygame.K_h]:
            grid_show = False


        if Player1.last_move == None and Player2.last_move == None:
            if key[pygame.K_n]:
                gamemode_change = False
            if key[pygame.K_m]:
                gamemode_change = True
            if key[pygame.K_r]:
                Food1.change_location()
                Food2.change_location()
            if key[pygame.K_i]:
                player_add = True
            if key[pygame.K_o]:
                player_add = False


    def game_mode_border(self):
        global gamemode_change
        if gamemode_change is True:
            pygame.draw.line(canvas, self.border_color, # top border
                (0, 0),
                (0, screen_height), self.border_with)
            pygame.draw.line(canvas, self.border_color, # left border
                (0, 40),
                (screen_width, 40), self.border_with)
            pygame.draw.line(canvas, self.border_color, # right border
                (screen_width-2, 0),
                (screen_width-2, screen_height), self.border_with)
            pygame.draw.line(canvas, self.border_color, # bottom border
                (0, screen_height-2),
                (screen_width, screen_height-2), self.border_with)
     




Player1 = Snake(40, 60, 20, (255,50,50), (50,255,50))
Player2 = Snake(40, 100, 20, (50,50,255), (255,50,50))

Food1 = Food(20, (255, 140, 0))
Food2 = Food(20, (255, 140, 0))

interface = Interface()

def restart():
    global reload_var
    if reload_var is True:
        global gamemode_change
        global score_player1
        global score_player2
        score_player1 = 0
        score_player2 = 0
        Player1.x = [40, 60, 80]
        Player1.y = [60, 60, 60]
        Player1.last_move = None

        Player2.x = [40, 60, 80]
        Player2.y = [100, 100, 100]
        Player2.last_move = None

        gamemode_change = False
        reload_var = False

def screen_update():
    global frame_count
    global gamemode_change
    global player_add
    frame_count += 1
    if frame_count >= 30:
        frame_count = 0
    if grid_show == True:
        interface.draw()
    interface.game_mode_border()
    interface.score_draw()
    Food1.draw()
    Player1.draw()
   

    if player_add is True:
        Food2.draw()
        Player2.draw()

    pygame.display.update()


run = True
while run:
    time.tick(30)
    canvas.fill(canvas_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    Player1.move()
    Player1.keypress(pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)
    interface.control()
    if player_add is True:
        Player2.move()
        Player2.keypress(pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
        Player2.check_end()

    Player1.check_end()
    restart()
    screen_update()
pygame.quit()