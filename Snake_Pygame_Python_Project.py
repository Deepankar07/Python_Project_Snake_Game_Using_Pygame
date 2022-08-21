from turtle import color
import pygame
import random
import os
pygame.mixer.init()                                                                     #--> Initializes mixer for music


x=pygame.init()                                                                         #---> Initializes all the modules in pygame

# Colours
white = (255,255,255)
red = (255,0,0)
green = (124,252,0)
black = (0,0,0)
blue=(0,0,255)

# Creating Game Display Window
screen_width=1000
screen_height=500
game_window = pygame.display.set_mode((screen_width,screen_height))                     #--> Set_mode takes tuple input as size i.e (width,height)
# Background Image
img = pygame.image.load("bcgimg.jpg")
img = pygame.transform.scale(img, (screen_width,screen_height)).convert_alpha()         #--> convert_alpha() func. maintains the speed of game when we keep on blit this image in gameloop


# GameTitle
pygame.display.set_caption("Snakes")                                                    #--> Set caption/Title of the game
pygame.display.update()
# Creating clock to update game frame according to anytime (FPS_Frame per Seconds)
clock = pygame.time.Clock()
font=pygame.font.SysFont(None,30)                                                       #--> Creating global font variable for screen_score in game


def screen_score(text,colour,x,y):
    screen_text=font.render(text,True,colour)                                           #--> font.render is a function of pygame
    game_window.blit(screen_text,[x,y])                                                 #--> blit function updates the screen


def  plot_snake(game_window, colour, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.ellipse(game_window, colour, [x, y, snake_size, snake_size])        #--> Drawing Snake_Head (position,colour,size)


# Creating Welcome Screen on Starting the Game
def welcome():
    exit_game = False
    while not exit_game:
        game_window.fill((235,230,230))
        screen_score("Welcome to Snakes Game !", black, 360, 200)
        screen_score("Press Space Key to Play", black, 372, 240)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("Background Music.mp3")                     #--> Loads The Music
                    pygame.mixer.music.play(-1)                                         #--> (-1) Plays The Music continuously on loop
                    gameloop()    
        pygame.display.update()
        clock.tick(60)        

# Creating Game Loop (Loop will run till game is running)
def gameloop():
    # Creating specific variables for the Game in loop so that it can be updated with new copy
    exit_game=False
    game_over=False
    snake_x=50
    snake_y=40
    velocity_x=0
    velocity_y=0
    snk_list=[]
    snk_length=1
    food_x=random.randint(10,screen_width/2)
    food_y=random.randint(10,screen_height/2)
    score=0
    init_velocity=2
    snake_size=12
    fps=60
    
    # Check if HighScore file exist
    if(not os.path.exists("HighScore.txt")):
        with open("HighScore.txt","w") as f:
            f.write("0")

    with open("HighScore.txt","r") as f:
        HighScore = f.read()

    while not exit_game:
        if game_over:
            with open("HighScore.txt","w") as f:
                f.write(str(HighScore))
            game_window.fill(white)
            screen_score("Game Over! Press Enter to Continue", black, 310, 210)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:                                            #--> Event Types and handling
                    exit_game = True      

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                                            #--> Event Types and handling
                    exit_game = True                                        

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity  
                        velocity_x = 0    
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0  

                    if event.key == pygame.K_w:
                        score+=10                                                         #--> Cheat Code for Increasing score press "w"

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<8 and abs(snake_y - food_y)<8:
                score+=10
                food_x=random.randint(10,1000/2)
                food_y=random.randint(10,500/2)
                snk_length +=5
                eat_sound=pygame.mixer.Sound("Eating sound.wav")
                eat_sound.play()
                if score>int(HighScore):
                    HighScore=score


            game_window.fill(white) 
            game_window.blit(img, (0,0))                                                   #--> blit the img
            screen_score("Score: " + str(score)+  "  HighScore: " + str(HighScore), green, 5,5)
            pygame.draw.circle(game_window, red, (food_x, food_y), 8)                      #--> (food_x,food_y) is centre and radius is 8

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:                                                       #--> Including all elements of snk_list except last one i.e [:-1]
                game_over = True
                pygame.mixer.music.load("Game Over.wav")                                    
                pygame.mixer.music.play()                                                   
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over=True
                pygame.mixer.music.load("Game Over.wav")                                    
                pygame.mixer.music.play()                                                   
            plot_snake(game_window, green, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)                                                                     #--> To run fps
            

    pygame.quit()
    quit()
welcome()    
