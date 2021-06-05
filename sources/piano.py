import pygame
import time
import random
import RPi.GPIO as GPIO
from pygame.locals import*
from oled import OLED
from oled import Font
from oled import Graphics

ledPin = 7
GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)
GPIO.setup(ledPin,GPIO.OUT)

# Connect to the OLED display on /dev/i2c-0
dis = OLED(1)

# Start communication
dis.begin()

# Start basic initialization
dis.initialize()

# Do additional configuration
dis.set_memory_addressing_mode(0)
dis.set_column_address(0, 127)
dis.set_page_address(0, 7)

# Clear display
dis.clear()

# Set font scale x2
f = Font(2)

# Se definenen los colores --------------------------
tile_color = (112, 231, 255)
border_color = (255, 255, 255)
push_tile_color = (253, 202, 64)
background_color = (14, 36, 68)
title_color = (226, 132, 19)
txt_color = (216 , 231, 233)

# Se agregan las canciones a la playlist
playList = ["Naruto - Sadness and Sorrow.mp3",
            "Black Catcher - Vickeblanka.mp3",
            "Tokyo Ghoul OP - Unravel.mp3",
            "Fire ForceEnen no Shouboutai OP - Inferno.mp3"]

clock = pygame.time.Clock()
score = 0

# Se crea el objeto Tile
class Tile:
    #Constructor
    def __init__(self, pos_x1, pos_y1, pos_x2, pos_y2, bck_color, speed, id_value , disp):
        
        self.pos_x1 = pos_x1
        self.pos_y1 = pos_y1
        
        self.pos_x2 = pos_x2
        self.pos_y2 = pos_y2
        
        self.bck_color = bck_color
        
        self.speed = speed
        
        self.id_value = id_value
        
        self.disp = disp
        
        self.tile = Rect(self.pos_x1, self.pos_y1, self.pos_x2, self.pos_y2)
    
    
    # Metodo para desplegar en pantalla
    def create(self):
        
        pygame.draw.rect(self.disp, self.bck_color, self.tile)
    
    # Si se presiona correctamente, cambia color y suma puntos
    def press(self):
        
        global score
        
        self.bck_color = push_tile_color
        score = score + 2
    
    # No se presiono, se mantiene igual
    def not_pressed(self):
        
        self.bck_color = tile_color
    
    # Actualiza cada Tile
    def upd(self):
        
        self.tile.update(self.pos_x1, 0, self.pos_x2, 180)
        
        pygame.draw.rect(self.disp, self.bck_color, self.tile)
        
        self.not_pressed()
    
    # Desplazamiento de cada Tile en su respectiva columna
    def shift(self):
        
        h = self.disp.get_height()
        
        # Se desplazan mientras no sobrepasen el borde inferior del juego
        while(self.tile.top <= h):
            
            # El LED parpadea dependiendo de la velocidad de cada Tile
            GPIO.output(ledPin, GPIO.HIGH) #LED ON
            
            self.disp.fill(background_color)
            
            pygame.draw.line(self.disp, border_color,(100,0),(100,500))
            pygame.draw.line(self.disp, border_color,(200,0),(200,500))
            pygame.draw.line(self.disp, border_color,(300,0),(300,500))
            pygame.draw.line(self.disp, border_color,(400,0),(400,500))
            
            self.tile.move_ip(0, self.speed)
            
            pygame.draw.rect(self.disp, self.bck_color, self.tile)
            
            # Compara las teclas presionadas con los Tiles y sus columnas (ID)
            for Event in pygame.event.get():
            
                if(Event.type == pygame.KEYDOWN):
                
                    if(Event.key == pygame.K_a and self.id_value == "a"):
                        
                        self.press()
                    
                    elif(Event.key == pygame.K_a and not(self.id_value == "a")):
                        
                        game_over()
                        
                    if(Event.key == pygame.K_s and self.id_value == "s"):

                        self.press()
                    
                    elif(Event.key == pygame.K_s and not(self.id_value == "s")):
                        
                        game_over()
                        
                    if(Event.key == pygame.K_d and self.id_value == "d"):

                        self.press()
                        
                    elif(Event.key == pygame.K_d and not(self.id_value == "d")):
                        
                        game_over()
                        
                    if(Event.key == pygame.K_f and self.id_value == "f"):

                        self.press()
                        
                    elif(Event.key == pygame.K_f and not(self.id_value == "f")):
                        
                        game_over()
                        
                if(Event.type == pygame.KEYUP):
                
                    if(Event.key == pygame.K_a):
                    
                        self.not_pressed()
                        
                    if(Event.key == pygame.K_s):
                    
                        self.not_pressed()
                        
                    if(Event.key == pygame.K_d):
                    
                        self.not_pressed()
                        
                    if(Event.key == pygame.K_f):
                    
                        self.not_pressed()
                        
            pygame.display.flip()
            clock.tick(60)
        
        self.upd()
        GPIO.output(ledPin, GPIO.LOW) #LED OF

# def blinkLED(speedL):
#     GPIO.output(ledPin, GPIO.HIGH) #LED ON
#     time.sleep(speedL)
#     GPIO.output(ledPin, GPIO.LOW) #LED OF
#     time.sleep(speedL)
    

# Inicializa el juego
def start_game():
    
    global score
    currScore, prevScore = 0, 0
    
    # Pantalla principal e inicializacion de variables
    width = 400
    height = 500
    
    level = -1
    
    pygame.init()
    pygame.mixer.init()
    
    mp3 = pygame.mixer.music
    
    disp = pygame.display.set_mode((width,height))
    disp.fill(background_color)
    pygame.display.set_caption("Piano Tiles.py")
    
    title_font = pygame.font.SysFont("arial", 50)
    txt_font = pygame.font.SysFont("arial", 25)
    
    title = title_font.render("Piano Tiles.py",True, title_color)
    info = txt_font.render("Select the level with the keyboard: ",True, txt_color)
    lv_1 = txt_font.render("1 >> Easy ",True, txt_color)
    lv_2 = txt_font.render("2 >> Normal ",True, txt_color)
    lv_3 = txt_font.render("3 >> Hard ",True, txt_color)
    lv_4 = txt_font.render("4 >> Imposible ",True, txt_color)
    
    while(level == -1):
        
        disp.blit(title, (50, 100))
        disp.blit(info, (25, 185))
        disp.blit(lv_1, (100, 250))
        disp.blit(lv_2, (100, 300))
        disp.blit(lv_3, (100, 350))
        disp.blit(lv_4, (100, 400))
        
        pygame.display.flip()
        clock.tick(60)
        
        for Event in pygame.event.get():
            
                if(Event.type == pygame.KEYDOWN):
               
                    if(Event.key == pygame.K_1):
                        
                        level = 0
                        
                    elif(Event.key == pygame.K_2):
                        
                        level = 1
                        
                    if(Event.key == pygame.K_3):
                        
                        level = 2
                        
                    if(Event.key == pygame.K_4):
                        
                        level = 3
    
    # carga la cancion dependiendo del nivel
    mp3.load(playList[level])
#     song = MP3(playList[level])
#     songLength = sonf.info.length
    a = pygame.mixer.Sound(playList[level])
    print(a.get_length())
    
    # Se selecciona el nivel
    if(level == 0):
        
        speed = 10
        
    elif(level == 1):
        
        speed = 15
        
    elif(level == 2):
        
        speed = 20
        
    else:
        
        speed = 25
        
    # Se crean 4 objetod de tipo Tile para las 4 columnas
    t1 = Tile(  0, 0, 100, 180, tile_color, speed, "a", disp)
    t2 = Tile(100, 0, 100, 180, tile_color, speed, "s", disp)
    t3 = Tile(200, 0, 100, 180, tile_color, speed, "d", disp)
    t4 = Tile(300, 0, 100, 180, tile_color, speed, "f", disp)
    
    # Se crea una lista de tipo Tile
    tile_list = [t1, t2, t3, t4]
    
    for t in tile_list:          
        t.create()
    
    # Se reproduce la cancion
    mp3.play()
    status = mp3.get_busy()
    
    time.sleep(2)
    
    # Se agregan Tiles de manera aleatoria al juego
    while status:
                
        # Despliega el puntaje en la OLED
        f.print_string(60, 15, str(score))
        dis.update()
        
        # Agrega Tiles aleatoreamente
        t = random.choice(tile_list)
        t.shift()
        status = mp3.get_busy()
        # Limpia la OLED
        dis.clear()
        
# Fin del juego e imprime el puntaje final 
def game_over():
    
    global score
    
    print(score)
    pygame.quit()
    

start_game()
game_over()

