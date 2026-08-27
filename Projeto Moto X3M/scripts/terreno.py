# scripts/terreno.py
import pygame
import random
import math
from scripts.config import *

class Terreno:
    def __init__(self, largura_tela):
        self.largura_tela = largura_tela
        self.alturas = []
        self.pontos = []
        self.offset_x = 0
        self.tamanho_segmento = TAMANHO_SEGMENTO
        self.largura_total = 5000  # 5000 pixels de pista
        
        # Gerar terreno
        self.gerar_terreno()
    
    def gerar_terreno(self):
        """Gera um terreno com colinas e obstáculos naturais"""
        self.alturas = []
        num_segmentos = self.largura_total // self.tamanho_segmento
        
        altura_base = ALTURA_TERRENO
        
        for i in range(num_segmentos):
            # Gerar altura com senoides para colinas suaves
            x = i * self.tamanho_segmento
            
            # Colinas
            altura = altura_base
            altura += math.sin(x * 0.008) * 50  # Colina grande
            altura += math.sin(x * 0.02 + 1.5) * 30  # Colina média
            altura += math.sin(x * 0.05 + 3.2) * 15  # Colina pequena
            
            # Picos e vales aleatórios
            if i % random.randint(15, 30) == 0:
                altura += random.randint(-20, 40)
            
            self.alturas.append(altura)
        
        # Criar pontos para desenho
        self.pontos = []
        for i, altura in enumerate(self.alturas):
            x = i * self.tamanho_segmento
            self.pontos.append((x, altura))
    
    def get_altura(self, x):
        """Retorna a altura do terreno em uma posição x"""
        indice = int(x // self.tamanho_segmento)
        if indice < 0:
            indice = 0
        if indice >= len(self.alturas):
            indice = len(self.alturas) - 1
        return self.alturas[indice]
    
    def get_angulo(self, x):
        """Retorna o ângulo do terreno em uma posição x"""
        indice = int(x // self.tamanho_segmento)
        if indice < 0 or indice >= len(self.alturas) - 1:
            return 0
        
        altura_atual = self.alturas[indice]
        altura_prox = self.alturas[indice + 1]
        diferenca = altura_prox - altura_atual
        
        return math.atan2(diferenca, self.tamanho_segmento)
    
    def atualizar(self, offset_x):
        self.offset_x = offset_x
    
    def desenhar(self, tela, offset_x):
        """Desenha o terreno com parallax"""
        # Céu (fundo)
        for y in range(ALTURA):
            cor = (135 - y * 0.1, 206 - y * 0.15, 235 - y * 0.1)
            pygame.draw.line(tela, cor, (0, y), (LARGURA, y))
        
        # Montanhas (parallax)
        self._desenhar_montanhas(tela, offset_x * 0.3)
        
        # Terreno principal
        pontos_visiveis = []
        for i, ponto in enumerate(self.pontos):
            x = ponto[0] - offset_x
            if -50 <= x <= LARGURA + 50:
                pontos_visiveis.append((x, ponto[1]))
        
        if len(pontos_visiveis) > 1:
            # Preencher o terreno
            pontos_preenchimento = pontos_visiveis + [(pontos_visiveis[-1][0], ALTURA), 
                                                       (pontos_visiveis[0][0], ALTURA)]
            pygame.draw.polygon(tela, (139, 69, 19), pontos_preenchimento)
            
            # Grama no topo
            for i in range(len(pontos_visiveis) - 1):
                x1, y1 = pontos_visiveis[i]
                x2, y2 = pontos_visiveis[i + 1]
                pygame.draw.line(tela, (34, 139, 34), (x1, y1), (x2, y2), 8)
                
                # Detalhes da grama
                if i % 5 == 0:
                    pygame.draw.line(tela, (50, 205, 50), (x1, y1 - 2), (x1 - 3, y1 - 6), 2)
    
    def _desenhar_montanhas(self, tela, offset):
        """Desenha montanhas com parallax"""
        # Montanhas distantes
        for i in range(5):
            x = (i * 250 - offset % 250) % (LARGURA + 200) - 100
            y = ALTURA_TERRENO - 50
            tamanho = 150 + i * 30
            pontos = [
                (x, y),
                (x + tamanho//2, y - tamanho),
                (x + tamanho, y)
            ]
            pygame.draw.polygon(tela, (100, 120, 140), pontos)
        
        # Montanhas próximas
        for i in range(3):
            x = (i * 400 - offset * 0.7 % 400) % (LARGURA + 300) - 150
            y = ALTURA_TERRENO - 30
            tamanho = 100 + i * 20
            pontos = [
                (x, y),
                (x + tamanho//2, y - tamanho//2),
                (x + tamanho, y)
            ]
            pygame.draw.polygon(tela, (70, 90, 110), pontos)