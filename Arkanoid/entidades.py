import pygame as pg
from Arkanoid import GAME_DIMENSIONS, FPS, DIMENSIONES_LADRILLO

import random
import sys

pg.init()

class Ladrillo(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.imagen = pg.Surface (DIMENSIONES_LADRILLO)
        self.rect = self.imagen.get_rect(x=x, y=y)
        self.imagen.fill((0,0,0))
        pg.draw.rect(self.imagen, (205,237,253), ((2,2), (self.rect.w-4, self.rect.h-4)))




class Raqueta(pg.sprite.Sprite):
    def __init__(self, x, y, vx):
        pg.sprite.Sprite.__init__(self)
        self.vx =vx

        self.imagen = pg.image.load("resources/images/regular_racket.png")
        self.rect = self.imagen.get_rect(x=x, y=y)
        

    def update(self, dt):
        self.rect.x += self.vx
        if self.rect.x + 128 >= GAME_DIMENSIONS[0]:
            self.rect.x = GAME_DIMENSIONS[0] - 128
        if self.rect.x <= 0:
            self.rect.x = 0

    def manejar_eventos(self):
        '''
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    self.x += 10
                    if self.x +128 >= GAME_DIMENSIONS[0]:
                        self.x = GAME_DIMENSIONS[0] - 128
                    
                    
                if event.key == pg.K_LEFT:
                    self.x -= 10
                    if self.x <= 0:
                        self.x = 
                        '''
                    
        teclas_pulsadas = pg.key.get_pressed()
        if teclas_pulsadas[pg.K_RIGHT]:
            self.vx = 10
        elif teclas_pulsadas [pg.K_LEFT]:
            self.vx = -10
        else:
            self.vx = 0



class Pelota(pg.sprite.Sprite):
    imagenes_files = ['brown_ball.png', 'blue_ball.png', 'red_ball.png', 'green_ball.png']
    num_imgs_explosion = 8
    retardo_animaciones = 5

    def __init__(self, x, y, vx, vy):
        pg.sprite.Sprite.__init__(self)
        
        self.vx = vx
        self.vy = vy
        self.imagenes = self.cargaImagenes()
        self.imagenes_explosion = self.cargaExplosion()
        self.imagen_act = 0
        self.ix_explosion = 0
        self.retardo_animaciones = 5
        self.ciclos_tras_refresco = 0
        self.ticks_acumulados = 0
        self.ticks_por_frame_de_animacion = 1000//FPS*self.retardo_animaciones
        self.muriendo = False
        self.imagen = self.imagenes[self.imagen_act]
        self.rect = self.imagen.get_rect(x=x, y=y)

    def cargaExplosion(self):
        
        return [pg.image.load(f"resources/images/explosion0{i}.png") for i in range(self.num_imgs_explosion)]
        '''
        lista_imagenes = []
        for i in range self.num_imgs_explosion:
            lista_imagenes.append(pg.image.load(f"resources/images/explosion0{i}.png"))
        return lista_imagenes
        '''

    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"resources/images/{img}"))
        return lista_imagenes

    def actualizar_posicion(self):
        if self.muriendo:
            return
        '''
        Gestionar posición de pelota
        '''
        if self.rect.left <=0 or self.rect.right >= GAME_DIMENSIONS[0]:
            self.vx = -self.vx
            

        if self.rect.top <=0:
            self.vy = -self.vy
            

        if self.rect.bottom >= GAME_DIMENSIONS[1]:
            self.muriendo = True
            self.ciclos_tras_refresco = 0
            return
            
            
        self.rect.x += self.vx
        self.rect.y += self.vy

    def actualizar_disfraz(self):
        '''
        Gestionar imagen activa (disfraz) de pelota
        '''
        self.ciclos_tras_refresco += 1
        
        if self.ciclos_tras_refresco % self.retardo_animaciones == 0:
            self.imagen_act += 1
            if self.imagen_act >= len(self.imagenes):
                self.imagen_act = 0
        
        self.imagen = self.imagenes[self.imagen_act]
        

    def update(self, dt):
        self.actualizar_posicion()

        if self.muriendo:
            return self.explosion(dt)
        else:
            self.actualizar_disfraz()

        
    def explosion(self, dt):
        if self.ix_explosion >= len(self.imagenes_explosion):
            return True
            
        self.imagen = self.imagenes_explosion[self.ix_explosion]

        self.ciclos_tras_refresco += 1

        self.ticks_acumulados += dt
        if self.ticks_acumulados >= self.ticks_por_frame_de_animacion:
            self.ix_explosion += 1
            self.ticks_acumulados = 0
        return False

    def comprobar_colision(self, algo):
        if self.rect.colliderect(algo.rect):
            self.vy *= -1
            return True
            


class Game:
    def __init__(self):
        self.pantalla = pg.display.set_mode(GAME_DIMENSIONS)
        pg.display.set_caption("Futuro Arkanoid")

        self.pelota = Pelota(400, 300, random.randint(2,5)*random.choice([1,-1]), random.randint(2,5)*random.choice([1,-1]))
        self.raqueta = Raqueta(336, 550, 0)

        self.jugadores = pg.sprite.Group(self.raqueta)
        self.ladrillos = self.crea_ladrillos()
        self.pelotas = pg.sprite.Group(self.pelota)
        self.todos = pg.sprite.Group(self.ladrillos, self.jugadores, self.pelotas)
        
        
        self.clock = pg.time.Clock()

    def crea_ladrillos(self):
        ladrillos = pg.sprite.Group()
        xo = 16
        yo = 16
        for c in range(12):
            for f in range(5):
                l = Ladrillo(xo + c * DIMENSIONES_LADRILLO[0], yo + f * DIMENSIONES_LADRILLO[1])
                ladrillos.add(l)
        return ladrillos

    def bucle_principal(self):
        game_over = False
        ladrillos_rotos = 0
        while not game_over:
            dt = self.clock.tick(FPS)
            '''
            Gestion de eventos
            '''
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.raqueta.manejar_eventos()
            
            '''
            Actualizacion de elementos del juego
            '''
            
            self.todos.update(dt)

            self.pelota.comprobar_colision(self.raqueta)
            for ladrillo in self.ladrillos:
                if self.pelota.comprobar_colision(ladrillo):
                    self.ladrillos.remove(ladrillo)
                    ladrillos_rotos += 1
            

            self.pantalla.fill((222,197,227))
            
            self.pantalla.blit(self.pelota.imagen, (self.pelota.rect.x, self.pelota.rect.y))
            self.pantalla.blit(self.raqueta.imagen, (self.raqueta.rect.x, self.raqueta.rect.y))
            
            for ladrillo in self.ladrillos:
                self.pantalla.blit(ladrillo.imagen, (ladrillo.rect.x, ladrillo.rect.y))

            if len(self.ladrillos) == 0:
                self.pantalla.fill(255, 255, 255)
            
            '''
            Refrescar pantalla
            '''
            pg.display.flip()

