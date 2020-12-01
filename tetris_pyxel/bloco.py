import constantes 
import random 

class Bloco():
    def __init__(self, forma = None):
        self.rotacao = 0
        if forma != None: 
            self.forma = forma 
        else: 
            self.forma = random.randint(0,6)
        self.posicao = (0,3) 
    
    def mover_bloco(self, direcao, area):
        if direcao == None:
            return 
        
        if direcao == constantes.direcao_L:
            nova_posicao = (self.posicao[0], self.posicao[1] - 1)
        elif direcao == constantes.direcao_R:
            nova_posicao = (self.posicao[0], self.posicao[1] + 1)
        elif direcao == constantes.direcao_D: 
            nova_posicao = (self.posicao[0] + 1, self.posicao[1])

        if self.bloco_valido(self.get_bloco_peca(nova_posicao, self.rotacao), area):
            self.posicao = nova_posicao 
            return True 
        return False 

    def rotacionar_bloco(self, direcao, area):
        if direcao == None: 
            return
        nova_rotacao = (self.rotacao + 1) % 4 if direcao == constantes.direcao_R else(self.rotacao - 1) % 4
        if self.bloco_valido(self.get_bloco_peca(self.posicao,nova_rotacao), area):
            self.rotacao = nova_rotacao
            return True
        
        return False

    def bloco_valido(self, bloco_pecas, area):
        for peca in bloco_pecas:
            if not(0 <= peca[0] <= 21) or not (0 <= peca[1] <= 9) or area[peca[0]][peca[1]] != 0:
                return False 
        return True 
            
    def get_bloco_peca(self, posicao, rotacao):
        bloco_nome = constantes.forma_dict[self.forma] + '_' + constantes.rotacao_dict[rotacao]
        bloco_pecas = constantes.bloco_dict[bloco_nome]
        return {(peca[0] + posicao[0], peca[1] + posicao[1]) for peca in bloco_pecas}