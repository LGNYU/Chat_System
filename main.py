# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from sys import exit
import random


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
import codecs



class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []  
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]  
        self.rect.topleft = init_pos 
        self.speed = 8  
        self.bullets = pygame.sprite.Group() 
        self.img_index = 0 
        self.is_hit = False 

   
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

   
    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    
    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    
    def move(self):
        self.rect.top += self.speed



def write_txt(content, strim, path):
    f = codecs.open(path, strim, 'utf8')
    f.write(str(content))
    f.close()

def read_txt(path):
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    return lines


def startGame():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Air war')
    ic_launcher = pygame.image.load('foo/resources/image/ic_launcher.png').convert_alpha()
    pygame.display.set_icon(ic_launcher)
    background = pygame.image.load('foo/resources/image/background.png').convert()
    game_over = pygame.image.load('foo/resources/image/gameover.png')
    plane_img = pygame.image.load('foo/resources/image/shoot.png')
    # Rank
    def gameRanking():
        screen2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen2.fill(0)
        screen2.blit(background, (0, 0))
        xtfont = pygame.font.SysFont('SimHei', 30)
        textstart = xtfont.render('Ranking ', True, (255, 0, 0))
        text_rect = textstart.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = 50
        screen.blit(textstart, text_rect)
        xtfont = pygame.font.SysFont('SimHei', 30)
        textstart = xtfont.render('Restart ', True, (255, 0, 0))
        text_rect = textstart.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 120
        screen2.blit(textstart, text_rect)
        arrayscore = read_txt(r'score.txt')[0].split('mr')
        for i in range(0, len(arrayscore)):
            font = pygame.font.Font(None, 48)
            k=i+1
            text = font.render(str(k) +"  " +arrayscore[i], True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.centerx = screen2.get_rect().centerx
            text_rect.centery = 80 + 30*k
            screen2.blit(text, text_rect)
    player_rect = []
    player_rect.append(pygame.Rect(0, 99, 102, 126))
    player_rect.append(pygame.Rect(165, 360, 102, 126))
    player_rect.append(pygame.Rect(165, 234, 102, 126))
    player_rect.append(pygame.Rect(330, 624, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(432, 624, 102, 126))
    player_pos = [200, 600]
    player = Player(plane_img, player_rect, player_pos)
    bullet_rect = pygame.Rect(69, 77, 10, 21)
    bullet_img = plane_img.subsurface(bullet_rect)
    enemy1_rect = pygame.Rect(534, 612, 57, 43)
    enemy1_img = plane_img.subsurface(enemy1_rect)
    enemy1_down_imgs = []
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))
    enemies1 = pygame.sprite.Group()
    enemies_down = pygame.sprite.Group()
    shoot_frequency = 0
    enemy_frequency = 0
    player_down_index = 16
    score = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(0)
        screen.blit(background, (0, 0))
        clock.tick(60)
        if not player.is_hit:
            if shoot_frequency % 15 == 0:
                player.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= 15:
                shoot_frequency = 0
        for bullet in player.bullets:
            
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        player.bullets.draw(screen)
        if enemy_frequency % 50 == 0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0
        for enemy in enemies1:
            enemy.move()
            if pygame.sprite.collide_circle(enemy, player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit = True
                break
            if enemy.rect.top < 0:
                enemies1.remove(enemy)
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down)
        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            player.img_index = shoot_frequency // 8
        else:
            player.img_index = player_down_index // 8
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 47:
                running = False
        for enemy_down in enemies_down:
            if enemy_down.down_index == 0:
                pass
            if enemy_down.down_index > 7:
                enemies_down.remove(enemy_down)
                score += 100
                continue
            screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
            enemy_down.down_index += 1

        enemies1.draw(screen)

        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()


    screen.blit(game_over, (0, 0))
    font = pygame.font.Font(None, 48)
    text = font.render('Score: ' + str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(text, text_rect)
    xtfont = pygame.font.SysFont('SimHei', 30)
    textstart = xtfont.render('Restart', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 120
    screen.blit(textstart, text_rect)
    textstart = xtfont.render('Ranking ', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 180
    screen.blit(textstart, text_rect)


    j = 0

    arrayscore = read_txt(r'score.txt')[0].split('mr')

    for i in range(0, len(arrayscore)):
        if score > int(arrayscore[i]):
            j = arrayscore[i]
            arrayscore[i] = str(score)
            score = 0
        if int(j) > int(arrayscore[i]):
            k = arrayscore[i]
            arrayscore[i] = str(j)
            j = k
    for i in range(0, len(arrayscore)):
        if i == 0:
            write_txt(arrayscore[i] + 'mr', 'w', r'score.txt')
        else:
            if (i == 9):
                write_txt(arrayscore[i], 'a', r'score.txt')
            else:
                write_txt(arrayscore[i] + 'mr', 'a', r'score.txt')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
            # Judge the scale of the mouse button
                if screen.get_rect().centerx - 70 <= event.pos[0] \
                    and event.pos[0] <= screen.get_rect().centerx + 50 \
                    and screen.get_rect().centery + 100 <= event.pos[1] \
                    and screen.get_rect().centery + 140 >= event.pos[1]:
                # Restart the game
                    startGame()
            # Click the ranking button?
                if screen.get_rect().centerx - 70 <= event.pos[0] \
                    and event.pos[0] <= screen.get_rect().centerx + 50 \
                    and screen.get_rect().centery + 160 <= event.pos[1] \
                    and screen.get_rect().centery + 200 >= event.pos[1]:
                    gameRanking()
        pygame.display.update()#refresh the screen

if __name__ == "__main__":
    pass




