"""
Asteroides_war - Version 1.0

Licence Apache version 2.0, janvier 2004
http://www.apache.org/licenses/

Copyright © Gaëtan Sencie 2023

"""

import pygame
import random
import sys
import os
import pygame.mixer

# Fonction pour obtenir le chemin correct des ressources
def chemin_relatif(chemin_relatif):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, chemin_relatif)
    return os.path.join(os.path.abspath("."), chemin_relatif)

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Paramètres de la fenêtre
largeur, hauteur = 1000, 800
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu spatial")

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Chargement de l'image du vaisseau et redimensionnement
vaisseau_img = pygame.image.load(chemin_relatif("vaisseau.png"))
vaisseau_img = pygame.transform.scale(vaisseau_img, (50, 50))

# Chargement de l'image de l'astéroïde et redimensionnement
astéroide_img = pygame.image.load(chemin_relatif("asteroide.png"))
astéroide_img = pygame.transform.scale(astéroide_img, (50, 50))

# Chargement du son du Game Over
son_game_over = pygame.mixer.Sound(chemin_relatif("game-over-sound.mp3"))

# Chargement de l'image du laser et redimensionnement
laser_img = pygame.Surface((2, 10))
laser_img.fill((255, 0, 0))

# Définition de la classe Vaisseau
class Vaisseau(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = vaisseau_img
        self.rect = self.image.get_rect()
        self.rect.centerx = largeur // 2
        self.rect.bottom = hauteur - 10
        self.vitesse_x = 2
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 100  # Limite de tir en millisecondes

    def update(self):
        self.vitesse_x = 0
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:
            self.vitesse_x = -2
        if touches[pygame.K_RIGHT]:
            self.vitesse_x = 2
        self.rect.x += self.vitesse_x

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largeur:
            self.rect.right = largeur

    def tirer_laser(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            laser = Laser(self.rect.centerx, self.rect.top)
            lasers.add(laser)
            all_sprites.add(laser)

# Définition de la classe Astéroide
class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = astéroide_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(largeur - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.vitesse_y = 0.7  # Vitesse réduite

    def update(self):
        self.rect.y += self.vitesse_y
        if self.rect.top > hauteur:
            self.rect.x = random.randrange(largeur - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

# Définition de la classe Laser
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 10))  # Modification de la largeur à 10 pixels
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.vitesse_y = -10

    def update(self):
        self.rect.y += self.vitesse_y
        if self.rect.bottom < 0:
            self.kill()

# Groupes de sprites
all_sprites = pygame.sprite.Group()
astéroides = pygame.sprite.Group()
lasers = pygame.sprite.Group()

# Création du vaisseau
vaisseau = Vaisseau()
all_sprites.add(vaisseau)

# Création des astéroïdes
for _ in range(8):
    asteroide = Asteroide()
    all_sprites.add(asteroide)
    astéroides.add(asteroide)

# Boucle principale du jeu
running = True
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                vaisseau.tirer_laser()

    all_sprites.update()

    # Vérification des collisions
    hits = pygame.sprite.groupcollide(astéroides, lasers, True, True)
    for hit in hits:
        asteroide = Asteroide()
        all_sprites.add(asteroide)
        astéroides.add(asteroide)
        score += 1

    hits = pygame.sprite.spritecollide(vaisseau, astéroides, False)
    if hits:
        running = False

    # Dessin de l'arrière-plan
    fenetre.fill(noir)

    # Dessin des sprites
    all_sprites.draw(fenetre)

    # Affichage du score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, blanc)
    fenetre.blit(score_text, (10, 10))

    pygame.display.flip()

# Game Over
font = pygame.font.Font(None, 72)
game_over_text = font.render("Game Over", True, blanc)
fenetre.blit(game_over_text, (largeur // 2 - 150, hauteur // 2 - 50))
pygame.display.flip()

son_game_over.play()  # Jouez le son du Game Over

pygame.time.wait(4100)

pygame.quit()
sys.exit()

