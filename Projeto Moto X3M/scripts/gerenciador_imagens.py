# scripts/gerenciador_imagens.py
import pygame
import os

class GerenciadorImagens:
    def __init__(self):
        self.imagens = {}
        self.pasta = "assets/imagens/"
        
        if not os.path.exists(self.pasta):
            os.makedirs(self.pasta)
    
    def carregar(self, nome, redimensionar=None):
        if nome in self.imagens:
            imagem = self.imagens[nome]
            if redimensionar:
                return pygame.transform.scale(imagem, redimensionar)
            return imagem
        
        # Tentar carregar
        imagem = None
        extensoes = ['', '.png', '.jpg', '.jpeg', '.bmp', '.gif']
        
        for ext in extensoes:
            caminho = os.path.join(self.pasta, nome + ext)
            if os.path.exists(caminho):
                try:
                    imagem = pygame.image.load(caminho).convert_alpha()
                    break
                except:
                    continue
        
        # Fallback
        if imagem is None:
            imagem = pygame.Surface((40, 40), pygame.SRCALPHA)
            imagem.fill((200, 100, 100))
            pygame.draw.rect(imagem, (255, 255, 255), (0, 0, 40, 40), 2)
        
        self.imagens[nome] = imagem
        
        if redimensionar:
            return pygame.transform.scale(imagem, redimensionar)
        return imagem