import pygame
import random
import os
from sys import exit


os.chdir(os.path.dirname(os.path.abspath(__file__))) #encontra a pasta com as sprites

pygame.init()


#configuracoes_basicas_do_jogo

LARGURA = 360
ALTURA = 640
TELA = pygame.display.set_mode((LARGURA, ALTURA)) #largura 360 e altura 640, estilo tela de celular
pygame.display.set_caption("Advance Bird")
FPS = 60
RELOGIO = pygame.time.Clock()

#Cores, caso_de_urgencia
AZUL_CEU = (135, 206, 250)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (220, 220, 220)
LARANJA = (255, 140, 0, 200)

#tamanho das fontes, usada anteriormente quando gerava as formas geometricas
FONTE = pygame.font.Font(None, 25)
FONTE_MENU = pygame.font.Font(None, 50) 
ALTURA_CAPA = 35


def carregar_recorde(): #record do jogador """Carrega o recorde atual do arquivo recorde.txt."""
    with open("recorde.txt", "r") as f:
        return int(f.read().strip())

def salvar_recorde(pontuacao):   #Salva a nova pontuação se for um novo record                         
    recorde_atual = carregar_recorde()
    if pontuacao > recorde_atual:
        with open("recorde.txt", "w") as f:
            f.write(str(pontuacao))
        return True
    return False

record = carregar_recorde()

#sprites do jogo

#fundo do jogo

fundo_img = pygame.image.load("imagem/fundo.png").convert()
fundo_img = pygame.transform.scale(fundo_img, (LARGURA, ALTURA))

#fundo do menu

fundo_menu_img_raw = pygame.image.load("imagem/fundo_menu.png").convert()
fundo_menu_img = pygame.transform.scale(fundo_menu_img_raw, (LARGURA, ALTURA))

#fundo_game_over
gameover_paineis = []

gameover_painel_red_raw = pygame.image.load("imagem/gameover_red.png").convert_alpha()
gameover_paineis.append(pygame.transform.scale(gameover_painel_red_raw, (LARGURA, ALTURA)))

gameover_painel_orange_raw = pygame.image.load("imagem/gameover_orange.png").convert_alpha()
gameover_paineis.append(pygame.transform.scale(gameover_painel_orange_raw, (LARGURA, ALTURA)))


passaro_frames = [
    pygame.transform.scale(pygame.image.load("imagem/passaro1.png").convert_alpha(), (40, 28)),
    pygame.transform.scale(pygame.image.load("imagem/passaro2.png").convert_alpha(), (40, 28)),
    pygame.transform.scale(pygame.image.load("imagem/passaro3.png").convert_alpha(), (40, 28))
]

#sprites dos obstaculos do jogo com alpha

sprites_obstaculos_originais = {
    "luz": pygame.image.load("imagem/luz.png").convert_alpha(),
    "arvore": pygame.image.load("imagem/arvore.png").convert_alpha(),
    "torre": pygame.image.load("imagem/torre.png").convert_alpha(),
    "antena": pygame.image.load("imagem/antena.png").convert_alpha(),
    "poste": pygame.image.load("imagem/poste.png").convert_alpha(),
}

#sprites com imagens ddo topo 

topo_imagem = pygame.image.load("imagem/topo.png").convert_alpha() #necessario pq alguns obstaculos nao estavam sendo gerados desde a base do jogo.
topo = pygame.transform.scale(topo_imagem, (LARGURA, ALTURA_CAPA)) 

base_imagem = pygame.image.load("imagem/baixo.png").convert_alpha() #a sprite de poste nao estava alcançando a base da tela, esta cobre em parte essa falha
base = pygame.transform.scale(base_imagem, (LARGURA, ALTURA_CAPA)) 

#sprite do botao iniciar

botao = pygame.image.load("imagem/botao_iniciar.png").convert_alpha()
BOTAO = pygame.transform.scale(botao, (150, 70))

#CLASSE_PÁSSARO 

class Passaro:
    def __init__(self):
        self.frames = passaro_frames
        self.frame_atual = 0
        self.imagem = self.frames[self.frame_atual]

        self.rect = self.imagem.get_rect(center=(50, ALTURA // 2))
        self.velocidade = 0
        self.gravidade = 0.5
        self.forca_pulo = -10

        
        self.contador_animacao = 0 

    def pular(self):
        self.velocidade = self.forca_pulo

    def atualizar(self):
        
        self.velocidade += self.gravidade 
        self.rect.y += self.velocidade

        if self.rect.bottom >= ALTURA:
            self.rect.bottom = ALTURA
            self.velocidade = 0

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocidade = 0

        
        self.contador_animacao += 1
        if self.contador_animacao >= 4:  
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.imagem = self.frames[self.frame_atual]
            self.contador_animacao = 0

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

#CLASSE_OBSTÁCULOS #bug da distorçao em parte corrigida

class Obstaculo:
    def __init__(self, x):
        self.tipo = random.choice(["poste", "arvore", "torre", "antena", "luz"])
        self.sprite_original = sprites_obstaculos_originais[self.tipo] 

        self.largura = 60
        self.espaco = 180
        self.velocidade = 4
        
        self.altura_topo = random.randint(80, ALTURA - self.espaco - 80) 
        altura_base = ALTURA - (self.altura_topo + self.espaco)

       
        self.topo_rect = pygame.Rect(x, 0, self.largura, self.altura_topo)   #definiçao dos parametros de colisao
        self.base_rect = pygame.Rect(x, self.altura_topo + self.espaco, self.largura, altura_base)

       
        self.topo_img_flip = pygame.transform.flip(self.sprite_original, False, True)  #Imagens dos topo e da base
        self.base_img = self.sprite_original

    def atualizar(self):
        self.topo_rect.x -= self.velocidade
        self.base_rect.x -= self.velocidade

    def fora_da_tela(self):
        return self.topo_rect.right < 0

    def desenhar(self, tela):
        
        scaled_topo = pygame.transform.scale(
            self.topo_img_flip, (self.largura, self.topo_rect.height)  #dimensiona a sprite
        )
        tela.blit(scaled_topo, (self.topo_rect.x, self.topo_rect.y))

        
        scaled_base = pygame.transform.scale(
            self.base_img, (self.largura, self.base_rect.height) #sprite infeior, redimensionada
        )
        tela.blit(scaled_base, (self.base_rect.x, self.base_rect.y))

#MENU do jogo INICIAL, somente o botao de iniciar foi implementado, ranking off nao foi desenvolvido, escolha de passaro, nao desenvolvido

class Menu:
    def __init__(self):
        self.titulo = FONTE_MENU.render(" ", True, PRETO)
        
        self.botao_sprite = BOTAO
        self.botao_rect = self.botao_sprite.get_rect(center=(LARGURA // 2, int(ALTURA * 0.75)))

        self.instrucao_pulo = FONTE.render(" ", True, PRETO)

    def exibir(self, tela):
       
        tela.blit(fundo_menu_img, (0, 0)) 
        
        tela.blit(self.titulo, (LARGURA // 2 - self.titulo.get_width() // 2, ALTURA // 4))
              
        tela.blit(self.botao_sprite, self.botao_rect)
                
        tela.blit(self.instrucao_pulo, (LARGURA // 2 - self.instrucao_pulo.get_width() // 2, ALTURA * 0.75))
        
        pygame.display.update()

    def verificar_clique(self, pos):
        return self.botao_rect.collidepoint(pos)

#classe_perdedor

class GameOver:
    def __init__(self):
        self.titulo = FONTE_MENU.render("   ", True, BRANCO)
        self.instrucao = FONTE.render("Precione ESPAÇO para Reiniciar", True, BRANCO)
        
        self.overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150)) 
        
        self.painel_fundo = random.choice(gameover_paineis) if gameover_paineis else None

    def exibir(self, tela, pontuacao, recorde):
        
        
        if self.painel_fundo:
            tela.blit(self.painel_fundo, (0, 0))
        else:
            tela.blit(fundo_img, (0, 0))
            tela.blit(self.overlay, (0, 0))
            
        texto = FONTE.render(f"Pontuação Final: {pontuacao}", True, BRANCO) #mostra os textos do placar
        
        recorde_cor = (255, 223, 0) if pontuacao >= recorde else BRANCO 
        recorde_texto = FONTE.render(f"Recorde: {recorde}", True, recorde_cor)

    
        tela.blit(self.titulo, (LARGURA // 2 - self.titulo.get_width() // 2, ALTURA // 5)) 

        x_deslocamento = 60 #variavel no eixo x para deslocar para as horizontais
        y_placar_centro = ALTURA // 2  + 150 # #variavel no eixo y para deslocar para as horizontais
        
        
        if self.painel_fundo: #painel da pontuaçao final e recorde do jogador
            painel_width = LARGURA - 150
            painel_height = 100
            border_radius = 12
            painel_rect = pygame.Rect(70 + x_deslocamento, y_placar_centro - painel_height // 2, painel_width, painel_height)
            border_rect = painel_rect.inflate(6, 6)
            pygame.draw.rect(tela, (255, 255, 255), border_rect, border_radius=border_radius)
            pygame.draw.rect(tela, (255, 140, 0, 200), painel_rect, border_radius=12) 
        
        
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2 + x_deslocamento, y_placar_centro - 25))
        tela.blit(recorde_texto, (LARGURA // 2 - recorde_texto.get_width() // 2 + x_deslocamento, y_placar_centro + 15))


       
        tela.blit(self.instrucao, (LARGURA // 2 - self.instrucao.get_width() // 2, ALTURA * 0.9))
        
        pygame.display.update()

# classe_jogo

class Jogo:
    def __init__(self):
        self.passaro = Passaro()
        self.obstaculos = []
        self.pontuacao = 0
        self.menu = Menu() 
        self.game_over = GameOver()
        self.estado = "menu"
        self.tempo_obstaculo = pygame.USEREVENT
        pygame.time.set_timer(self.tempo_obstaculo, 1500)
        self.fundo_x1 = 0        
        self.fundo_x2 = LARGURA  
        self.fundo_velocidade = 2 

    def resetar(self):
        self.passaro = Passaro()
        self.obstaculos = []
        self.pontuacao = 0
        self.estado = "jogando"
        self.game_over = GameOver() 
        
        
        self.fundo_x1 = 0    #ao reiniciar o jogo, retorna tela inicial   
        self.fundo_x2 = LARGURA

    def atualizar(self):
        
        self.fundo_x1 -= self.fundo_velocidade #loop do fundo
        self.fundo_x2 -= self.fundo_velocidade

        if self.fundo_x1 < -LARGURA:
            self.fundo_x1 = LARGURA
        if self.fundo_x2 < -LARGURA:
            self.fundo_x2 = LARGURA
          
        self.passaro.atualizar()
       
        for obst in self.obstaculos:
            obst.atualizar()

        self.obstaculos = [o for o in self.obstaculos if not o.fora_da_tela()]

       
        for obst in self.obstaculos:  #colisao passaro x obstaculos
            if self.passaro.rect.colliderect(obst.topo_rect) or self.passaro.rect.colliderect(obst.base_rect):
                
                global record
                if salvar_recorde(self.pontuacao):
                    record = self.pontuacao 
                
                self.estado = "gameover"
                return 

        
        for obst in self.obstaculos: #pontuaçao ao nao colidir
            if obst.topo_rect.right < self.passaro.rect.left and not hasattr(obst, "pontuado"):
                obst.pontuado = True
                self.pontuacao += 1

    def desenhar(self):
                
        TELA.blit(fundo_img, (self.fundo_x1, 0)) #desenha a tela de fundo repetindo-a
        TELA.blit(fundo_img, (self.fundo_x2, 0))

        for obst in self.obstaculos:
            obst.desenhar(TELA)

        if topo:
            TELA.blit(topo, (0, 0)) 
        
        if base:
            TELA.blit(base, (0, ALTURA - ALTURA_CAPA))

        self.passaro.desenhar(TELA)

        
        placar_texto = FONTE.render(f"Pontos: {self.pontuacao}", True, BRANCO) # Placar 
        pygame.draw.rect(TELA, LARANJA, (LARGURA - 150, 10, 140, 40), border_radius=8)
        TELA.blit(placar_texto, (LARGURA - 140, 18))

        pygame.display.update()

#loopdojogo

jogo = Jogo()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if jogo.estado == "menu":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jogo.estado = "jogando"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    pos_mouse = event.pos
                    if jogo.menu.verificar_clique(pos_mouse):
                        jogo.estado = "jogando"

        elif jogo.estado == "jogando":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jogo.passaro.pular()

            if event.type == jogo.tempo_obstaculo:
                jogo.obstaculos.append(Obstaculo(LARGURA))

        elif jogo.estado == "gameover":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jogo.resetar()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

    if jogo.estado == "menu":
        jogo.menu.exibir(TELA)
    elif jogo.estado == "jogando":
        jogo.atualizar()
        jogo.desenhar()
    elif jogo.estado == "gameover":
        jogo.game_over.exibir(TELA, jogo.pontuacao, record)
        
    RELOGIO.tick(FPS)