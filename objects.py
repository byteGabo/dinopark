from math import trunc
import pygame

PANTALLA = WIDTH, HEIGHT = (288,512)

class Background():
    def __init__(self, pan):
        self.pan = pan
        
        #Fondo
        self.image = pygame.image.load('Assets/bg.png')
        self.image = pygame.transform.scale(self.image,(WIDTH,HEIGHT))
        self.rect = self.image.get_rect()
        
        self.reset()
        self.move = True
        
    def update(self, speed):
        if self.move:
            self.y1 += speed
            self.y2 += speed
            
            if self.y1 >= HEIGHT:
                self.y1 = -HEIGHT
            if self.y2 >= HEIGHT:
                self.y2 = -HEIGHT
                    
        self.pan.blit(self.image,(self.x,self.y1)) 
        self.pan.blit(self.image,(self.x,self.y2))       
        
    def reset(self):
        self.x = 0 
        self.y1 = 0
        self.y2 = -HEIGHT
        
        
class Jugador:
    def __init__(self, x, y):
        self.image_list = []
        for i in range(2):
            img = pygame.image.load(f'Assets/dino{i+1}.png')
            img = pygame.transform.scale(img,(72,72))
            self.image_list.append(img)
            
        self.index = 0
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(center=(x,y))
        
        self.counter = 0
        self.speed = 3
        self.health = 100
        self.width = self.image.get_width()
    
    def update(self,izquierda,derecha):
        if izquierda and self.rect.x > 2:
            self.rect.x -= self.speed
        if derecha and self.rect.x < WIDTH - self.width:
            self.rect.x += self.speed    
        
        self.counter += 1
        if self.counter >= 2:
            self.index = (self.index + 1) % len(self.image_list)
            self.image = self.image_list[self.index]
            self.counter = 0
          
    
    def draw(self,pan):
        pan.blit(self.image,self.rect)    
        
        
class Enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y, type_):
        super(Enemigos,self).__init__()
        
        self.type = type_
        self.image_list = []
        for i in range(2):
            if type_ == 1:
                img = pygame.image.load(f'Assets/cactus/cactus1-{i+1}.png')
            if type_ == 2:
                img = pygame.image.load(f'Assets/cuervo/cuervo1-{i+1}.png')    
            w,h = img.get_width(),img.get_height()
            height= (72*h)//w
            img = pygame.transform.scale(img,(72,height))
            self.image_list.append(img)
            
        self.index = 0
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y = y
        
        self.frame_dict={1:3,2:3,3:3,4:5,5:4}
        self.frame_fps = self.frame_dict[type_]
        
        self.counter = 0
        self.speed = 1
        self.health = 100
        self.disparo_counter = 0
    
    def shoot(self, enemigos_disparo_group):
        if self.type in (1, 2):
          x, y = self.rect.center
          h = Disparo(x,y,self.type)
          enemigos_disparo_group.add(h)
        
    
    def update(self, enemigos_disparo_group):
        self.rect.y  += self.speed 
        if self.rect.top >= HEIGHT:
           self.kill() 
        
        if self.health <= 0:
            self.kill

        self.disparo_counter += 1
        
        if self.disparo_counter >= 60:
            self.shoot(enemigos_disparo_group)
            self.disparo_counter = 0
        
        self.counter += 1
        if self.counter >= self.frame_fps:
            self.index = (self.index + 1) % len(self.image_list)
            self.image = self.image_list[self.index]
            self.counter = 0
             
    
    def draw(self,pan):
        pan.blit(self.image,self.rect)  
        
class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y, type_):
        super(Disparo,self).__init__()        
        if type_ == 1 :
            self.image = pygame.image.load('Assets/disparo/3.png')
            self.image = pygame.transform.scale(self.image, (15,30))
        if type_ == 2 :
            self.image = pygame.image.load('Assets/disparo/1.png')
            self.image = pygame.transform.scale(self.image, (15,30))   
             
        self.rect = self.image.get_rect(center=(x,y))
        if type_ == 2:
            self.speed = -3
        else:
            self.speed = 3    
       
        self.damage_dicc = {1:10, 2:20}
        self.damage = self.damage_dicc[type_]
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom <=0:
            self.kill()
        if self.rect.top >=HEIGHT:
            self.kill()
    
    def draw(pan):
        pan.blit(self.image,self.rect) 

class Boton(pygame.sprite.Sprite):
    def __init__(self,img, scale, x, y):
        super(Boton,self).__init__()
        
        self.scale = scale
        self.image = pygame.transform.scale(img,self.scale)
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y 
        
        self.clicked = False
        
    def update_image(self,img):
        self.image = pygame.transform.scale(img, self.scale)
        
    def draw(self, pan):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True
                
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        
        pan.blit(self.image, self.rect)
        return action
        