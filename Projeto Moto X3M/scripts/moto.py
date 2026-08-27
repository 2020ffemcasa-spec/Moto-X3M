# scripts/moto.py
import pygame
import math
from scripts.config import *

class Moto:
    def __init__(self, x, y, gerenciador_imagens):
        self.x = x
        self.y = y
        self.gi = gerenciador_imagens
        
        # Carregar imagens
        self.imagem_normal = self.gi.carregar("moto.png", redimensionar=(45, 35))
        self.imagem_rodando = self.gi.carregar("moto_rodando.png", redimensionar=(45, 35))
        self.imagem_pulando = self.gi.carregar("moto_pulando.png", redimensionar=(45, 40))
        
        self.imagem = self.imagem_normal
        self.rect = self.imagem.get_rect(center=(x, y))
        
        # Física
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.no_chao = False
        self.angulo = 0
        self.velocidade_angular = 0
        
        # ============================================
        # ATRIBUTOS ADICIONADOS PARA POWER-UPS
        # ============================================
        self.vivo = True
        self.boost_ativo = False
        self.tempo_boost = 0
        self.escudo_ativo = False
        self.tempo_escudo = 0
        self.ima_ativo = False      # <-- ADICIONADO
        self.tempo_ima = 0          # <-- ADICIONADO
        self.pulo_duplo_ativo = False
        self.tempo_pulo_duplo = 0
        self.pulos_restantes = 1
        
        # Animação
        self.frame_roda = 0
        self.tempo_animacao = 0
        self.rastro = []
        
        # Estatísticas
        self.distancia = 0
        self.pontos = 0
        self.moedas = 0
    
    def pular(self):
        """Pular - suporta pulo duplo"""
        if self.no_chao:
            self.velocidade_y = FORCA_PULO
            self.no_chao = False
            self.pulos_restantes = 2 if self.pulo_duplo_ativo else 1
            self.imagem = self.imagem_pulando
            return True
        elif self.pulo_duplo_ativo and self.pulos_restantes > 0 and not self.no_chao:
            self.velocidade_y = FORCA_PULO * 0.8
            self.pulos_restantes -= 1
            self.imagem = self.imagem_pulando
            return True
        return False
    
    def acelerar(self, direcao=1):
        """Acelerar ou frear"""
        if self.boost_ativo:
            self.velocidade_x += direcao * ACELERACAO * 1.8
        else:
            self.velocidade_x += direcao * ACELERACAO
        
        # Limitar velocidade
        limite = VELOCIDADE_MAXIMA * (1.5 if self.boost_ativo else 1)
        if abs(self.velocidade_x) > limite:
            self.velocidade_x = limite * (1 if self.velocidade_x > 0 else -1)
    
    def frear(self):
        """Frear bruscamente"""
        self.velocidade_x *= (1 - FRENAGEM)
        if abs(self.velocidade_x) < 0.1:
            self.velocidade_x = 0
    
    def ativar_boost(self):
        """Ativar power-up Boost"""
        if not self.boost_ativo:
            self.boost_ativo = True
            self.tempo_boost = DURACAO_BOOST
    
    def ativar_escudo(self):
        """Ativar power-up Escudo"""
        if not self.escudo_ativo:
            self.escudo_ativo = True
            self.tempo_escudo = DURACAO_ESCUDO
    
    def ativar_ima(self):
        """Ativar power-up Imã"""
        if not self.ima_ativo:
            self.ima_ativo = True
            self.tempo_ima = DURACAO_IMA
    
    def ativar_pulo_duplo(self):
        """Ativar power-up Pulo Duplo"""
        if not self.pulo_duplo_ativo:
            self.pulo_duplo_ativo = True
            self.tempo_pulo_duplo = DURACAO_PULO_DUPLO
            self.pulos_restantes = 2
    
    def atualizar(self, terreno):
        """Atualizar estado da moto"""
        # --- FÍSICA ---
        # Gravidade
        self.velocidade_y += GRAVIDADE
        self.y += self.velocidade_y
        
        # Movimento horizontal
        self.x += self.velocidade_x
        
        # Atrito
        if self.no_chao:
            self.velocidade_x *= ATRITO_CHAO
        else:
            self.velocidade_x *= ATRITO_AR
        
        # --- POWER-UPS ---
        if self.boost_ativo:
            self.tempo_boost -= 1
            if self.tempo_boost <= 0:
                self.boost_ativo = False
        
        if self.escudo_ativo:
            self.tempo_escudo -= 1
            if self.tempo_escudo <= 0:
                self.escudo_ativo = False
        
        if self.ima_ativo:  # <-- CORRIGIDO
            self.tempo_ima -= 1
            if self.tempo_ima <= 0:
                self.ima_ativo = False
        
        if self.pulo_duplo_ativo:
            self.tempo_pulo_duplo -= 1
            if self.tempo_pulo_duplo <= 0:
                self.pulo_duplo_ativo = False
        
        # --- COLISÃO COM TERRENO ---
        altura_terreno = terreno.get_altura(self.x)
        if self.y >= altura_terreno - self.rect.height//2:
            self.y = altura_terreno - self.rect.height//2
            if not self.no_chao:
                self.no_chao = True
                self.imagem = self.imagem_rodando
                self.pulos_restantes = 1
            self.velocidade_y = 0
        
        # --- ÂNGULO ---
        angulo_terreno = terreno.get_angulo(self.x)
        self.angulo = math.degrees(angulo_terreno) * 0.5
        
        # Inclinação baseada na velocidade
        if abs(self.velocidade_x) > 2:
            self.angulo += self.velocidade_x * 0.3
        
        # --- ANIMAÇÃO ---
        if self.no_chao and abs(self.velocidade_x) > 1:
            self.tempo_animacao += 1
            if self.tempo_animacao > 4:
                self.tempo_animacao = 0
                self.frame_roda = (self.frame_roda + 1) % 2
                if self.frame_roda == 0:
                    self.imagem = self.imagem_normal
                else:
                    self.imagem = self.imagem_rodando
        
        # --- DISTÂNCIA ---
        if self.velocidade_x > 0:
            self.distancia += self.velocidade_x * 0.1
        
        # --- RASTRO ---
        if abs(self.velocidade_x) > 3 and self.no_chao:
            self.rastro.append({
                'x': self.x,
                'y': self.y + self.rect.height//2,
                'vida': 20
            })
        
        # Atualizar rastro
        for r in self.rastro[:]:
            r['vida'] -= 1
            if r['vida'] <= 0:
                self.rastro.remove(r)
        
        # --- ATUALIZAR RECT ---
        self.rect.center = (int(self.x), int(self.y))
    
    def desenhar(self, tela, offset_x=0):
        """Desenhar a moto"""
        # Desenhar rastro
        for r in self.rastro:
            alpha = int(r['vida'] / 20 * 100)
            cor = (150, 150, 150, alpha)
            pygame.draw.circle(tela, cor, (int(r['x'] - offset_x), int(r['y'])), 3)
        
        # Desenhar moto com rotação
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        rect = imagem_rotacionada.get_rect(center=(self.x - offset_x, self.y))
        tela.blit(imagem_rotacionada, rect)
        
        # Escudo (efeito visual)
        if self.escudo_ativo:
            pygame.draw.circle(tela, (30, 144, 255, 100), 
                              (int(self.x - offset_x), int(self.y)), 
                              40, 3)
        
        # Efeito de Boost
        if self.boost_ativo:
            for i in range(3):
                x_boost = self.x - offset_x - 20 - i * 8
                y_boost = self.y + 5 + i * 3
                tamanho = 8 - i * 2
                cor = (255, 165 - i * 30, 0)
                pygame.draw.circle(tela, cor, (int(x_boost), int(y_boost)), tamanho)
        
        # Efeito Imã
        if self.ima_ativo:
            # Desenhar um círculo magnético
            for i in range(3):
                raio = 30 + i * 10
                alpha = 50 - i * 15
                pygame.draw.circle(tela, (200, 50, 50, alpha), 
                                  (int(self.x - offset_x), int(self.y)), 
                                  raio, 2)
    
    def get_rect(self):
        return self.rect
    
    def get_center(self):
        return self.rect.center