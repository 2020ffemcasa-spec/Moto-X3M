# scripts/obstaculos.py
import pygame
from scripts.config import *

class Obstaculo:
    def __init__(self, x, tipo, gerenciador_imagens):
        self.x = x
        self.tipo = tipo
        self.ativo = True
        self.gi = gerenciador_imagens
        
        # Configurar baseado no tipo
        configs = {
            "cone": {"imagem": "obstaculo_cone.png", "tamanho": (20, 30), "dano": 1},
            "barreira": {"imagem": "obstaculo_barreira.png", "tamanho": (60, 40), "dano": 3},
            "caixa": {"imagem": "obstaculo_caixa.png", "tamanho": (30, 30), "dano": 2},
            "rampa": {"imagem": "rampa.png", "tamanho": (80, 20), "dano": 0},
            "pneu": {"imagem": "obstaculo_pneu.png", "tamanho": (25, 25), "dano": 1},
            "espinho": {"imagem": "obstaculo_espinho.png", "tamanho": (20, 20), "dano": 2},
        }
        
        conf = configs.get(tipo, configs["cone"])
        self.imagem = self.gi.carregar(conf["imagem"], redimensionar=conf["tamanho"])
        self.dano = conf["dano"]
        self.y_offset = 0
        
        if tipo == "rampa":
            self.y_offset = -5
        
        self.rect = self.imagem.get_rect(center=(x, 0))
        self.altura_terreno = 0
    
    def atualizar(self, offset_x, altura_terreno):
        self.altura_terreno = altura_terreno
        self.rect.center = (int(self.x), int(altura_terreno - self.rect.height//2 + self.y_offset))
        
        if self.x < -100:
            self.ativo = False
    
    def desenhar(self, tela, offset_x=0):  # <-- ADICIONADO offset_x com valor padrão
        if self.ativo:
            tela.blit(self.imagem, (self.x - offset_x - self.imagem.get_width()//2, 
                                     self.altura_terreno - self.imagem.get_height() + self.y_offset))
    
    def get_rect(self):
        return self.rect