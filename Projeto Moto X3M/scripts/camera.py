# scripts/camera.py
from scripts.config import *

class Camera:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.x = 0
        self.y = 0
        self.alvo_x = 0
        self.alvo_y = 0
        
        # Limites da câmera
        self.min_x = 0
        self.max_x = 5000  # Largura total do nível
    
    def seguir(self, alvo_x, alvo_y):
        """Faz a câmera seguir um alvo suavemente"""
        self.alvo_x = alvo_x - self.largura // 3
        self.alvo_y = alvo_y - self.altura // 2
        
        # Limitar
        self.alvo_x = max(self.min_x, min(self.alvo_x, self.max_x - self.largura))
        
        # Movimento suave
        self.x += (self.alvo_x - self.x) * 0.1
        self.y += (self.alvo_y - self.y) * 0.1
    
    def get_offset(self):
        return int(self.x), int(self.y)