import pygame as pg
import sys
import random
import entidades

class Game:
    def __init__(self):
        self.pantalla = pg.display.set_mode((800,600))
        pg.display.set_caption("Futuro Arkanoid")
        self.pelota = entidades.Pelota(400, 300, 5, 5, (251,202,239), 15)

    def bucle_principal(self):
        game_over = False
        while not game_over:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()


            if self.pelota.left <=0 or self.pelota.right >= 800:
                self.pelota.vx = -self.pelota.vx
                
            if self.pelota.top <=0 or self.pelota.bottom >= 600:
                self.pelota.vy = -self.pelota.vy
            

            self.pelota.x += self.pelota.vx
            self.pelota.y += self.pelota.vy

            self.pantalla.fill((150,10,150))
            self.pantalla.blit(self.pelota.imagen, (self.pelota.x, self.pelota.y))
            

            pg.display.flip()



if __name__== '__main__':
    pg.init()
    game = Game()
    game.bucle_principal()