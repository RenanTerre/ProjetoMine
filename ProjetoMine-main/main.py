import pygame
import random
import os
from tkinter import simpledialog

pygame.init()

relogio = pygame.time.Clock()
icone = pygame.image.load("recursos/icone.png")
steve = pygame.image.load("recursos/steve.png")
fundo = pygame.image.load("recursos/fundomine.png")
fundoStart = pygame.image.load("recursos/fundostart.png")
fundoDead = pygame.image.load("recursos/fundoDead.png")

mob = pygame.image.load("recursos/creeper.png")
mob2 = pygame.image.load("recursos/zombie.png")
abelha = pygame.image.load("recursos/abelha.png")  # Nova imagem da abelha adicionada
tamanho = (800, 600)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Minecraft 2")
pygame.display.set_icon(icone)
creeperSound = pygame.mixer.Sound("recursos/creeper.wav")
zombieSound = pygame.mixer.Sound("recursos/zombie.wav")
stevemorrendoSound = pygame.mixer.Sound("recursos/stevemorrendo.wav")
fonte = pygame.font.SysFont("comicsans", 28)
fonteStart = pygame.font.SysFont("comicsans", 55)
fonteMorte = pygame.font.SysFont("arial", 120)
pygame.mixer.music.load("recursos/stevesound.mp3")

branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)

tamanho_sol = 30
tamanho_sol_min = 20
tamanho_sol_max = 50
tempo_troca_tamanho_sol = 500
ultimo_tempo_troca_sol = pygame.time.get_ticks()

def atualizar_tamanho_sol():
    global tamanho_sol, ultimo_tempo_troca_sol
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultimo_tempo_troca_sol > tempo_troca_tamanho_sol:
        tamanho_sol = random.randint(tamanho_sol_min, tamanho_sol_max)
        ultimo_tempo_troca_sol = tempo_atual

def jogar(nome):
    pygame.mixer.Sound.play(creeperSound)
    pygame.mixer.Sound.play(zombieSound)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona = 0
    movimentoYPersona = 0
    posicaoXmob = 400
    posicaoYmob = -240
    posicaoXmob2 = 600
    posicaoYmob2 = -350
    velocidademob = 1
    pontos = 0
    larguraPersona = 200
    alturaPersona = 250
    larguamob = 85
    alturamob = 85
    dificuldade = 30

    # Variáveis para a abelha móvel
    posicaoXAbelha = 0
    movimentoAbelha = 5  # Velocidade de movimento da abelha (pixels por frame)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0

        posicaoXPersona = posicaoXPersona + movimentoXPersona
        posicaoYPersona = posicaoYPersona + movimentoYPersona

        if posicaoXPersona < 0:
            posicaoXPersona = 10
        elif posicaoXPersona > 550:
            posicaoXPersona = 540

        if posicaoYPersona < 0:
            posicaoYPersona = 10
        elif posicaoYPersona > 473:
            posicaoYPersona = 463

        tela.fill(branco)
        tela.blit(fundo, (0, 0))
        tela.blit(steve, (posicaoXPersona, posicaoYPersona))

        posicaoYmob = posicaoYmob + velocidademob
        if posicaoYmob > 600:
            posicaoYmob = -240
            pontos = pontos + 1
            velocidademob = velocidademob + 1
            posicaoXmob = random.randint(0, 800)
            pygame.mixer.Sound.play(creeperSound)

        posicaoYmob2 = posicaoYmob2 + velocidademob
        if posicaoYmob2 > 600:
            posicaoYmob2 = -240
            pontos = pontos + 1
            velocidademob = velocidademob + 1
            posicaoXmob2 = random.randint(0, 800)
            pygame.mixer.Sound.play(zombieSound)

        tela.blit(mob, (posicaoXmob, posicaoYmob))
        tela.blit(mob2, (posicaoXmob2, posicaoYmob2))

        texto = fonte.render(nome + "- Pontos: " + str(pontos), True, branco)
        tela.blit(texto, (10, 10))

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona + larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona + alturaPersona))
        pixelsmobX = list(range(posicaoXmob, posicaoXmob + larguamob))
        pixelsmobY = list(range(posicaoYmob, posicaoYmob + alturamob))
        pixelsmobX2 = list(range(posicaoXmob2, posicaoXmob2 + larguamob))
        pixelsmobY2 = list(range(posicaoYmob2, posicaoYmob2 + alturamob))

        if len(list(set(pixelsmobY).intersection(set(pixelsPersonaY)))) > dificuldade:
            if len(list(set(pixelsmobX).intersection(set(pixelsPersonaX)))) > dificuldade:
                dead(nome, pontos)

        if len(list(set(pixelsmobY2).intersection(set(pixelsPersonaY)))) > dificuldade:
            if len(list(set(pixelsmobX2).intersection(set(pixelsPersonaX)))) > dificuldade:
                dead(nome, pontos)

        atualizar_tamanho_sol()
        pygame.draw.circle(tela, amarelo, (750, 50), tamanho_sol)

        posicaoXAbelha += movimentoAbelha

        if posicaoXAbelha >= tela.get_width() - abelha.get_width() or posicaoXAbelha <= 0:
            movimentoAbelha = -movimentoAbelha

        tela.blit(abelha, (posicaoXAbelha, 350)) 

        pygame.display.update()
        relogio.tick(60)

def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(stevemorrendoSound)

    jogadas = {}
    try:
        arquivo = open("historico.txt", "r", encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt", "w", encoding="utf-8")
        arquivo.close()

    jogadas[nome] = pontos
    arquivo = open("historico.txt", "w", encoding="utf-8")
    arquivo.write(str(jogadas))
    arquivo.close()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        textoStart = fonteStart.render("RESTART", True, branco)
        tela.blit(textoStart, (400, 482))
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (60, 482))
        pygame.display.update()
        relogio.tick(60)

def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt", "r", encoding="utf-8")
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass

    nomes = sorted(estrelas, key=estrelas.get, reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330, 482))

        posicaoY = 50
        for key, nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - " + str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300, posicaoY))
            posicaoY = posicaoY + 30

        pygame.display.update()
        relogio.tick(60)

def start():
    nome = simpledialog.askstring("Minecraft", "Nome Completo:")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        buttonRanking = pygame.draw.rect(tela, preto, (35, 50, 200, 50), 0, 30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90, 50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (330, 482))

        pygame.display.update()
        relogio.tick(60)

start()