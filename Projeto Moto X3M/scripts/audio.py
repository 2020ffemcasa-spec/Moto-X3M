# scripts/audio.py
import pygame
import os
from scripts.config import PASTA_SONS

class GerenciadorAudio:
    def __init__(self):
        pygame.mixer.init()
        self.sons = {}
        self.musica_atual = None
        self.volume = 0.5
    
    def carregar_som(self, nome):
        """Carrega um som do disco"""
        if nome in self.sons:
            return self.sons[nome]
        
        caminho = os.path.join(PASTA_SONS, nome)
        try:
            som = pygame.mixer.Sound(caminho)
            self.sons[nome] = som
            return som
        except:
            print(f"⚠️ Som não encontrado: {nome}")
            return None
    
    def tocar(self, nome, volume=None):
        """Toca um som"""
        som = self.carregar_som(nome)
        if som:
            if volume is not None:
                som.set_volume(volume)
            som.play()
    
    def tocar_musica(self, nome, loop=True):
        """Toca música de fundo"""
        caminho = os.path.join(PASTA_SONS, nome)
        try:
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.play(-1 if loop else 0)
            self.musica_atual = nome
        except:
            print(f"⚠️ Música não encontrada: {nome}")
    
    def parar_musica(self):
        """Para a música"""
        pygame.mixer.music.stop()
    
    def pausar_musica(self):
        """Pausa a música"""
        pygame.mixer.music.pause()
    
    def despausar_musica(self):
        """Despausa a música"""
        pygame.mixer.music.unpause()
    
    def set_volume(self, volume):
        """Ajusta o volume geral"""
        self.volume = max(0, min(1, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def criar_som_placeholder(self, frequencia=440, duracao=0.2):
        """Cria um som placeholder usando pygame"""
        try:
            import numpy as np
            sample_rate = 22050
            t = np.linspace(0, duracao, int(sample_rate * duracao))
            wave = np.sin(2 * np.pi * frequencia * t)
            wave = (wave * 32767).astype(np.int16)
            return pygame.mixer.Sound(buffer=wave.tobytes())
        except:
            return pygame.mixer.Sound(buffer=bytes([128]) * 1000)