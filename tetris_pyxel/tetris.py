import bloco #código com o objeto que termina as ações dos blocos
import constantes # código onde se encontra determinado o formato dos blocos, as rotações e as direções possíveis
import random 
import pyxel 

class Tetris: 
    def __init__(self):
        pyxel.init(120, 220, fps = 75) # fps determina a taxa de atualização e consequentemente a velocidade de queda
        pyxel.image(0).load(0,0, 'bloco_imagem.png') # carrega imagem das cores
        self.reinicia() # começa o jogo
        pyxel.run(self.atualiza, self.desenha) #cria as imagens
    
    def reinicia(self):
        self.estado = 'iniciado' #inicia o jogo
        self.frame_count_ultimo_movimento = 0 #leva o bloco ao início
        self.pontos = 0 #zera os pontos
        self.area = [] 
        self.area_peca_cores = []
        self.blocos = [0,1,2,3,4,5,6]
        for linha in range(22):
            self.area.append([0] * 10)
            self.area_peca_cores.append([-1] * 10)
        self.bloco = bloco.Bloco(forma = self.blocos.pop(random.randint(0, len(self.blocos) - 1)))
    
    def atualiza(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if pyxel.btnp(pyxel.KEY_R):
            self.reinicia()
            return

        if pyxel.btnp(pyxel.KEY_P):
            if self.estado == 'iniciado':
                self.estado = 'pausado'
            else:
                self.estado = 'iniciado'
        
        if self.estado == 'pausado':
            return
        
        mover_direcao = None 
        rotacionar_direcao = None
        if pyxel.btnp(pyxel.KEY_LEFT, 12, 2):
            mover_direcao = constantes.direcao_L
        elif pyxel.btnp(pyxel.KEY_RIGHT, 12, 2):
            mover_direcao = constantes.direcao_R
        elif pyxel.btnp(pyxel.KEY_DOWN, 12, 2):
            mover_direcao = constantes.direcao_D
        elif pyxel.btnp(pyxel.KEY_UP, 12, 20):
            rotacionar_direcao = constantes.direcao_L
        
        if self.bloco.mover_bloco(mover_direcao, self.area):
            if mover_direcao == constantes.direcao_D:
                self.frame_count_ultimo_movimento = 0
        
        self.bloco.rotacionar_bloco(rotacionar_direcao, self.area)

        if (self.frame_count_ultimo_movimento == 45):
            self.frame_count_ultimo_movimento = 0
            if not(self.bloco.mover_bloco(constantes.direcao_D, self.area)):
                if self.game_over():
                    self.reinicia()
                    return
                self.para_bloco()
                self.limpa_linhas()
                if (len(self.blocos) == 0):
                    self.blocos = [0,1,2,3,4,5,6]
                self.bloco = bloco.Bloco(forma = self.blocos.pop(random.randint(0, len(self.blocos) - 1)))

        self.frame_count_ultimo_movimento += 1
    
    def desenha(self):
        self.desenha_area()
        pyxel.text(40, 190, "PONTOS: ", 10)
        pyxel.text(70, 190, str(self.pontos), 12)
        pyxel.text(6, 200, "Q:Quit", 8)
        pyxel.text(40, 200, "P:Pause", 9)
        pyxel.text(76, 200, "R:Restart", 11)
    
    def desenha_area(self):
        pyxel.cls(0)
        bloco_atual_peca = self.bloco.get_bloco_peca(self.bloco.posicao, self.bloco.rotacao)

        #desenhar blocos 
        pyxel.rectb(20, 20, 82, 162, 3)
        for peca in bloco_atual_peca:
            if 2 <= peca[0] <= 21:
                pyxel.blt(peca[1] * 8 + 21, 21 + (peca[0] - 2) * 8, 0, self.bloco.forma * 8, 0, 8, 8, 0)

        # tela parada 
        for linha in range(2, 22):
            for coluna in range(10):
                if self.area[linha][coluna] == 1:
                    pyxel.blt(21 + coluna * 8, 21 + (linha - 2) * 8, 0, self.area_peca_cores[linha][coluna] * 8, 0, 8, 8, 0)
    
    def para_bloco(self):
        for peca in self.bloco.get_bloco_peca(self.bloco.posicao, self.bloco.rotacao):
            self.area[peca[0]][peca[1]] = 1
            self.area_peca_cores[peca[0]][peca[1]] = self.bloco.forma
    
    def limpa_linhas(self):
        linhas_para_limpar = []
        for linha in range(2,22):
            if sum(self.area[linha]) == 10:
                linhas_para_limpar.append(linha)
        if len(linhas_para_limpar) < 4:
            self.pontos += (100* len(linhas_para_limpar))
        else:
            self.pontos += 800   
        for linha in linhas_para_limpar:
            for r in range(linha, 1, -1):
                self.area[r] = [x for x in self.area[r - 1]]
                self.area_peca_cores[r] = [x for x in self.area_peca_cores[r - 1]]
        
    def game_over(self):
        if self.bloco.posicao[0] == 0:
            return True
        return False

if __name__ == '__main__':
    Tetris()