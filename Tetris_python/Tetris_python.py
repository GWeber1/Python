import pygame 
import random 

pygame.font.init()

tela_tamanho = 800
tela_largura = 700
play_width = 300 
play_height = 600  
tamanho_bloco = 30 #tamanho das formas

top_left_x = (tela_tamanho - play_width) // 2
top_left_y = tela_largura - play_height

#CORES = todas as cores usadas no jogo

cor_verde = (0,255,0)
cor_vermelho = (255,0,0)
cor_azul_claro = (0,255,255)
cor_amarelo = (255,255,0)
cor_laranja = (255,165,0)
cor_azul = (0,0,255)
cor_roxo = (128,0,128)
cor_cinza = (128,128,128)
cor_preta = (0,0,0)
cor_branca = (255, 255, 255)

#FORMATOS = matrizes de todas as peças e suas possíveis posições

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

formas = [S, Z, I, O, J, L, T] #Lista de formas possíveis 
cores_formas = [(cor_verde),(cor_vermelho),(cor_azul_claro), (cor_amarelo),(cor_laranja), (cor_azul),(cor_roxo)] # índice de cores para as formas
# indíce de representação das formas

class Peca(object): #superclasse
    def __init__(self, x, y, forma):
        self.x = x
        self.y = y 
        self.forma = forma 
        self.cor = cores_formas[formas.index(forma)] #associa formas com cores
        self.rotacao = 0 # variável para rotacionar peças

def criar_area(posicao={}):
    area = [[(cor_preta) for _ in range(10)] for _ in range(20)] #Criação da área de jogo

    for i in range(len(area)):
        for j in range(len(area[i])):
            if (j,i) in posicao:
                c = posicao[(j,i)] 
                area[i][j] = c
    return area 

def converte_forma(forma): 
    posicoes = []
    format = forma.forma[forma.rotacao % len(forma.forma)]

    for i, linha_area in enumerate(format):
        linha = list(linha_area)
        for j, coluna in enumerate(linha):
            if coluna == '0':
                posicoes.append((forma.x + j, forma.y + i))
    
    for i, pos in enumerate(posicoes):
        posicoes[i] = (pos[0] - 2, pos[1] - 4)
    
    return posicoes

def espaco_valido(forma, area): #função de delimitação do espaço válido
    posicao_aceita = [[(j, i) for j in range(10) if area[i][j] == (cor_preta)] for i in range(20)]
    posicao_aceita = [j for sub in posicao_aceita for j in sub]

    formato = converte_forma(forma)

    for pos in formato:
        if pos not in posicao_aceita:
            if pos[1] > -1:
                return False 
    return True

def checa_perda(posicoes): # função que verifica se o jogador perdeu
    for pos in posicoes:
        x, y = pos 
        if y < 1:
            return True 

    return False

def pega_forma(): #função que aleatoriza as formas que descem
    return Peca(5, 0, random.choice(formas))

def desenha_texto(superficie, texto, tamanho, cor): #função que escreve na tela
    fonte = pygame.font.SysFont("comicsans", tamanho, bold=True)
    label = fonte.render(texto, 1, cor)

    superficie.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))

def desenha_area(superficie, area): #função que deixa a área quadriculada
    sx = top_left_x
    sy = top_left_y

    for i in range(len(area)):
        pygame.draw.line(superficie, (cor_cinza), (sx, sy  + i*tamanho_bloco),(sx+play_width, sy+i*tamanho_bloco))
        for j in range(len(area[i])):
            pygame.draw.line(superficie, (cor_cinza), (sx+j*tamanho_bloco, sy),(sx + j*tamanho_bloco, sy + play_height))

def limpa_linhas(area, sorteado): #função que limpa a linha cada vez que uma for preenchida
    inc = 0
    for i in range(len(area)-1,-1,-1):
        linha = area[i]
        if (cor_preta) not in linha: 
            inc += 1
            ind = i 
            for j in range(len(linha)):
                try:
                    del sorteado[(j,i)]
                except: 
                    continue 
    
    if inc > 0:
        for key in sorted(list(sorteado), key=lambda x: x[1])[::-1]:
            x, y = key 
            if y < ind: 
                new_key = (x,y + inc)
                sorteado[new_key] = sorteado.pop(key)
    return inc

def desenha_proxima_forma(forma, superficie): #função que escreve e desenha na tela as próximas peças a virem
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Próxima Peça', 1, (cor_branca))

    sx = top_left_x + play_width + 50 
    sy = top_left_y + play_height/2 - 100 
    format = forma.forma[forma.rotacao % len(forma.forma)]

    for i, linha_area in enumerate(format):
        linha = list(linha_area)
        for j, coluna in enumerate(linha):
            if coluna == '0':
                pygame.draw.rect(superficie, forma.cor, (sx + j*tamanho_bloco, sy + i*tamanho_bloco, tamanho_bloco, tamanho_bloco), 0)
    
    superficie.blit(label, (sx+10, sy-30))

def atualiza_score(nscore): #função que envia os pontos para o .txt
    score = score_maximo()

    with open('pontuacao.txt','w') as f:
        if int(score) > nscore: 
            f.write(str(score))
        else:
            f.write(str(nscore))

def score_maximo(): #função que verifica qual a maior pontuação já feita no jogo
    with open('pontuacao.txt', 'r') as f:
        linhas = f.readlines()
        score = linhas[0].strip()
    
    return score

def desenha_janela(superficie, area, score = 0, ultimo_score = 0): #Função que coloca os dados na tela de jogo
    superficie.fill((cor_preta))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris',1,(cor_branca))

    superficie.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Pontos: ' + str(score),1,(cor_branca))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    superficie.blit(label, (sx + 20, sy + 160))

    label = font.render('Recorde: ' + ultimo_score, 1, (cor_branca))

    sx = top_left_x - 200
    sy = top_left_y + 200

    superficie.blit(label, (sx + 20, sy + 160))

    for i in range(len(area)):
        for j in range(len(area[i])):
            pygame.draw.rect(superficie, area[i][j], (top_left_x + j*tamanho_bloco, top_left_y + i*tamanho_bloco, tamanho_bloco, tamanho_bloco), 0)
    
    pygame.draw.rect(superficie, (cor_vermelho), (top_left_x,top_left_y,play_width,play_height), 5)

    desenha_area(superficie, area)

def main(inicia): #Função que será chamado ao iniciar o jogo
    pygame.init()
    pygame.mixer.music.load('buttercup.mp3') #trilha sonora
    pygame.mixer.music.play()
    ultimo_score = score_maximo()
    posicoes = {}
    area = criar_area(posicoes)

    mudar_peca = False 
    run = True 
    peca_atual = pega_forma()
    proxima_peca = pega_forma()
    clock = pygame.time.Clock() #define o tempo de atualização da tela
    tempo_queda = 0
    velocidade_queda = 0.27 #velocidade em que a peça cai
    tempo_nivel = 0
    score = 0 #pontos começam em 0
    
    while run: #loop do jogo
        area = criar_area(posicoes)
        tempo_queda += clock.get_rawtime()
        tempo_nivel += clock.get_rawtime()
        clock.tick()

        if tempo_nivel/1000 > 5:
            tempo_nivel = 0
            if tempo_nivel > 0.12:
                tempo_nivel -= 0.005
        
        if tempo_queda/1000 > velocidade_queda:
            tempo_queda = 0
            peca_atual.y += 1
            if not(espaco_valido(peca_atual, area)) and peca_atual.y > 0:
                peca_atual.y -= 1
                mudar_peca = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                pygame.display.quit()
        
            if event.type == pygame.KEYDOWN: #enquanto a peça desce
                if event.key == pygame.K_LEFT: #se a tecla pressionada for <-
                    peca_atual.x -= 1
                    if not(espaco_valido(peca_atual, area)): 
                        peca_atual.x += 1 
                if event.key == pygame.K_RIGHT: #se a tecla pressionada for ->
                    peca_atual.x += 1
                    if not(espaco_valido(peca_atual, area)):
                        peca_atual.x -= 1
                if event.key == pygame.K_DOWN: # se a tecla pressionada for v
                    peca_atual.y += 1
                    if not(espaco_valido(peca_atual, area)):
                        peca_atual.y -= 1
                if event.key == pygame.K_UP: #se a tecla pressionada for ^
                    peca_atual.rotacao += 1
                    if not(espaco_valido(peca_atual, area)):
                        peca_atual.rotacao -= 1
        
        forma_pos = converte_forma(peca_atual) #lança mais uma peça após a peça atual cair

        for i in range(len(forma_pos)):
            x, y = forma_pos[i]
            if y > -1:
                area[y][x] = peca_atual.cor #joga a peça na área de jogo
        
        if mudar_peca:
            for pos in forma_pos: 
                p = (pos[0], pos[1])
                posicoes[p] = peca_atual.cor #armazena a peça na lista
            peca_atual = proxima_peca 
            proxima_peca = pega_forma()
            mudar_peca = False 
            score += limpa_linhas(area, posicoes) * 10 #adiciona 10 pontos após completar uma linha
        
        desenha_janela(inicia, area, score, ultimo_score) 
        desenha_proxima_forma(proxima_peca, inicia)
        pygame.display.update() #atualiza as informações na tela

        if checa_perda(posicoes): #termina o jogo se perdeu
            desenha_texto(inicia, 'VOCÊ PERDEU!', 80, (cor_branca))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False 
            atualiza_score(score)

def menu_principal(inicia): #primeira tela ao iniciar o jogo
    run = True 
    while run: #loop de permanência da tela
        inicia.fill((cor_preta))
        desenha_texto(inicia, 'Pressione qualquer tecla', 60, (cor_branca))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            if event.type == pygame.KEYDOWN:
                main(inicia)

    pygame.display.quit() #sai do jogo ao ter a janela fechada pelo jogador
inicia = pygame.display.set_mode((tela_tamanho, tela_largura)) #inicia o jogo com os parâmetros do tamanho da tela
pygame.display.set_caption('Tetris') #define o nome no topo da janela
menu_principal(inicia) #início da execução  