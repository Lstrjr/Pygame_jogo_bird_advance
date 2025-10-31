import pygame
from sys import exit
import random

pygame.init()

largura = 360 #largura da tela
altura = 640 #altura da tela

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Advance Bird')
atualizar_jogo = pygame.time.Clock()

# Cores
AZUL_CEU = (135, 206, 250)
AMARELO_PASSARO = (255, 255, 0)
VERDE_OBSTACULO = (34, 139, 34)

#passaro
passaro = pygame.Rect(50, altura // 2, 20, 20)

#fisica

gravidade = 0.4
velocidade = 0
forca_pulo = -10

#obstáculo
obstaculos = []
espaco_passagem = 220
velocidade_obstaculos = 3

def criar_obstaculo():
    altura_topo = random.randint(100, 400)
    obstaculo_topo = pygame.Rect(largura, 0, 60, altura_topo)
    obstaculo_base = pygame.Rect(largura, altura_topo + espaco_passagem, 60, altura - (altura_topo + espaco_passagem))
    return obstaculo_topo, obstaculo_base

#gerar_obstáculos
SPAWN = pygame.USEREVENT
pygame.time.set_timer(SPAWN, 1500)  # a cada 1,5s

#reiniciar_jogo
def resetar_jogo():
    """Reseta a posição do pássaro e limpa os obstáculos"""
    global passaro, velocidade, obstaculos
    passaro.x = 50
    passaro.y = altura // 2
    velocidade = 0
    obstaculos = []

#Loop do jogo

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

#teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocidade = forca_pulo

#repetiçao_obstaculo

        if event.type == SPAWN:
            obstaculos.extend(criar_obstaculo())

    #física_pássaro
    velocidade += gravidade
    passaro.y += velocidade

    if passaro.y + passaro.height > altura:
        passaro.y = altura - passaro.height
        velocidade = 0
    if passaro.y < 0:
        passaro.y = 0
        velocidade = 0

    tela.fill(AZUL_CEU)  # Fundo primeiro

    #Obstáculos
    for obstaculo in obstaculos:
        obstaculo.x -= velocidade_obstaculos
        pygame.draw.rect(tela, VERDE_OBSTACULO, obstaculo)

        #Colisão
        if passaro.colliderect(obstaculo):
            resetar_jogo()

    # Remove obstáculos que saíram da tela
    obstaculos = [ob for ob in obstaculos if ob.x + ob.width > 0]

    # Pássaro
    pygame.draw.rect(tela, AMARELO_PASSARO, passaro)

    pygame.display.update()
    atualizar_jogo.tick(60)



    
    
    
    













