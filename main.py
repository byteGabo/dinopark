import random
import pygame
from pygame.constants import K_LEFT, K_RIGHT
from objects import Background, Jugador, Enemigos, Disparo, Boton

pygame.init()
PANTALLA = WIDTH, HEIGHT = (288,512)

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
    pan = pygame.display.set_mode(PANTALLA)
else:
    pan = pygame.display.set_mode(PANTALLA, pygame.SCALED | pygame.FULLSCREEN)

clock= pygame.time.Clock()
FPS = 25

#Variables
SPEED = 1
   
#Colores 
BLANCO =(255,255,255)
NEGRO = (0,0,0)
GRIS =(60,60,60)

#FONDO
bg = Background(pan)
#JUGADOR
j = Jugador(144,HEIGHT - 80)
izquierda = False
derecha = False 
#ENEMIGOS
enemigos_group = pygame.sprite.Group()
jugador_disparo_group = pygame.sprite.Group()
enemigos_disparo_group = pygame.sprite.Group()
#IMAGENES
logo_img=pygame.image.load('Assets/logo.png')
dino_img=pygame.image.load('Assets/dino1.png')
#BOTONES
play_img=pygame.image.load('Assets/play.png')
close_img=pygame.image.load('Assets/close.png')
play_btn= Boton(play_img, (24,24), WIDTH//4-18, HEIGHT//2 + 120)
close_btn= Boton(close_img, (24,24), WIDTH//2-18, HEIGHT//2 + 115)


level=1
enemigos_frequency = 4500
start_time = pygame.time.get_ticks()

home_page = True 
game_page = False
score_page = False
    
run = True
while run:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        #Mover Al Jugador        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                izquierda = True
            if event.key == pygame.K_RIGHT:
                derecha = True
            #Disparar
            if event.key == pygame.K_SPACE:
                x, y = j.rect.center[0], j.rect.y
                h = Disparo(x, y, 2)
                jugador_disparo_group.add(h)
                    
        #Mover al Jugador con el click del Mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            x= event.pos[0]
            if x <= WIDTH // 2:
                izquierda = True
            if x >= WIDTH // 2:
                derecha = True
                        
        if event.type == pygame.KEYUP:
            izquierda = False
            derecha = False
            
        if event.type == pygame.MOUSEBUTTONUP:
            izquierda = False
            derecha = False
    
    if home_page:
        pan.fill(NEGRO)
        pan.blit(logo_img,(30,80))
        pan.blit(dino_img,(WIDTH//2 - 50, HEIGHT//2))
        
        if play_btn.draw(pan):
            game_page = True
            home_page = False
      
        
    
    if game_page:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - start_time
        if delta_time >= enemigos_frequency:
            x= random.randint(10,WIDTH-72 )
            e=Enemigos(x,-150,1)
            enemigos_group.add(e)
            start_time = current_time
            
        bg.update(SPEED)
        
        j.update(izquierda,derecha)
        j.draw(pan)
        
        jugador_disparo_group.update()
        jugador_disparo_group.draw(pan)
        
        enemigos_disparo_group.update()
        enemigos_disparo_group.draw(pan)
    
        
        enemigos_group.update(enemigos_disparo_group)
        enemigos_group.draw(pan)
        
        jugador_hit = pygame.sprite.spritecollide(j, enemigos_disparo_group, False)
        
        for shot in jugador_hit:
            j.health -= shot.damage
            print(j.health)
            shot.kill()
        for shot in jugador_disparo_group:
            cactus_hit = pygame.sprite.spritecollide(shot, enemigos_group, False) 
            for cactus in cactus_hit:
                cactus.health -= shot.damage
                cactus.kill()
    
    pygame.draw.rect(pan, NEGRO, (0,0,WIDTH,HEIGHT), 5, border_radius=4)
    clock.tick(FPS)         
    pygame.display.update()
pygame.quit()