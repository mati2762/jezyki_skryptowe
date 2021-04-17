import pygame
from GameObjects.Player import Player
from GameObjects.Ball import Ball
from GameObjects.LevelGenerator import LevelGenerator
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from pygame.locals import KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, K_SPACE

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

uruchomiona = True

score = 0
lives = 3
pygame.display.set_caption("Arkanoid UJ")

player = Player(SCREEN_WIDTH/2 , 450)
ball = Ball(SCREEN_WIDTH/2 , 440)

klocki = LevelGenerator.generate_level()

pygame.mixer.music.load("sounds/intro.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

while uruchomiona:

    # Eventy , Klawiatura
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            uruchomiona = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                uruchomiona = False
            if event.key == K_SPACE:
                ball.run_ball()

    # Aktualizaja obiektów
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    ball.update()
    screen.fill((0, 0, 0))

    # Rysowanie spritów
    for klocek in klocki:
        screen.blit(klocek.surf, klocek.rect)
    screen.blit(player.surf, player.rect)
    screen.blit(ball.surf, ball.rect)

    #Kolizja z klockami
    if pygame.sprite.spritecollideany(ball, klocki):
        score+=1
        delete_klocek = pygame.sprite.spritecollideany(ball, klocki)
        delete_klocek.kill()
        ball.bounce()
        # usuniecie klocka

    # Kolizja z graczem
    if pygame.sprite.collide_rect(ball, player):
        ball.velocity[0] = -ball.velocity[0]
        ball.bounce()
        print("kolizja")

    # Restart Gry
    if ball.rect.y > SCREEN_HEIGHT - ball.height:
        ball = Ball(SCREEN_WIDTH/2 + 20, 440)
        player = Player(305, 450)
        lives -=1
        score = 0
        klocki = LevelGenerator.generate_level()


    # Rysowanie punktów i życia
    font = pygame.font.Font(None, 24)
    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    screen.blit(text, (10, SCREEN_HEIGHT - 20))
    text = font.render("Lives: " + str(lives), 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 70 , SCREEN_HEIGHT - 20))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()



