# scripts/colecionaveis.py
import pygame

class Colecionavel:
    def __init__(self, x, y, tipo, gerenciador_imagens):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.ativo = True
        self.gi = gerenciador_imagens
        
        if tipo == "moeda":
            self.imagem = self.gi.carregar("moeda.png", redimensionar=(15, 15))
            self.valor = 5
        else:  # estrela
            self.imagem = self.gi.carregar("estrela.png", redimensionar=(20, 20))
            self.valor = 25
        
        self.rect = self.imagem.get_rect(center=(x, y))
        self.frame = 0
        self.timer = 0
        self.offset_y = 0
    
    def atualizar(self):
        self.timer += 1
        if self.timer > 5:
            self.timer = 0
            self.frame = (self.frame + 1) % 2
        
        self.offset_y = abs(self.frame - 0.5) * 5
        self.rect.center = (int(self.x), int(self.y - self.offset_y))
    
    def desenhar(self, tela, offset_x=0):  # <-- ADICIONADO offset_x
        if self.ativo:
            tela.blit(self.imagem, (self.x - offset_x, self.y - self.offset_y - self.imagem.get_height()//2))
    
    def get_rect(self):
        return self.rect