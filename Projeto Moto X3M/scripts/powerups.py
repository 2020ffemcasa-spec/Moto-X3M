# scripts/powerups.py
import pygame

class PowerUp:
    def __init__(self, x, y, tipo, gerenciador_imagens):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.ativo = True
        self.gi = gerenciador_imagens
        
        cores = {
            "boost": (255, 165, 0),
            "escudo": (30, 144, 255),
            "ima": (200, 50, 50),
            "pulo_duplo": (50, 205, 50)
        }
        
        self.imagem = self.gi.carregar(f"{tipo}.png", redimensionar=(30, 30))
        self.cor = cores.get(tipo, (255, 255, 255))
        self.rect = self.imagem.get_rect(center=(x, y))
        self.timer = 0
        self.offset_y = 0
    
    def atualizar(self):
        self.timer += 1
        self.offset_y = abs(self.timer % 60 - 30) * 0.3
        self.rect.center = (int(self.x), int(self.y - self.offset_y))
    
    def desenhar(self, tela, offset_x=0):  # <-- ADICIONADO offset_x
        if self.ativo:
            # Glow
            pygame.draw.circle(tela, (*self.cor, 50), 
                              (int(self.x - offset_x), int(self.y - self.offset_y)), 20)
            tela.blit(self.imagem, (self.x - offset_x - self.imagem.get_width()//2, 
                                     self.y - self.offset_y - self.imagem.get_height()//2))
    
    def get_rect(self):
        return self.rect