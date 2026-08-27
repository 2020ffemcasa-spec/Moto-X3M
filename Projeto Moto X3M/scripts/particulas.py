# scripts/particulas.py
import pygame
import random
import math

class Particula:
    def __init__(self, x, y, cor, velocidade, angulo, vida, tamanho):
        self.x = x
        self.y = y
        self.cor = cor
        self.vx = velocidade * math.cos(angulo)
        self.vy = velocidade * math.sin(angulo) - 1
        self.vida = vida
        self.vida_max = vida
        self.tamanho = tamanho
        self.gravidade = 0.2
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravidade
        self.vida -= 1
        return self.vida > 0
    
    def draw(self, tela):
        alpha = int((self.vida / self.vida_max) * 255)
        tamanho_atual = int(self.tamanho * (self.vida / self.vida_max))
        surf = pygame.Surface((tamanho_atual*2, tamanho_atual*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.cor, alpha), (tamanho_atual, tamanho_atual), tamanho_atual)
        tela.blit(surf, (self.x - tamanho_atual, self.y - tamanho_atual))

class SistemaParticulas:
    def __init__(self):
        self.particulas = []
    
    def adicionar_explosao(self, x, y, cor, quantidade=20, velocidade_extra=0):
        for _ in range(quantidade):
            angulo = random.uniform(0, 2 * math.pi)
            velocidade = random.uniform(2, 6) + velocidade_extra
            vida = random.randint(20, 40)
            tamanho = random.randint(3, 8)
            self.particulas.append(Particula(x, y, cor, velocidade, angulo, vida, tamanho))
    
    def update(self):
        self.particulas = [p for p in self.particulas if p.update()]
    
    def draw(self, tela):
        for p in self.particulas:
            p.draw(tela)