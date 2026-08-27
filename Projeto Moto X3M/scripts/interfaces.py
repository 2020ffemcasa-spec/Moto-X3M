# scripts/interfaces.py
import pygame
import math

class HUD:
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.SysFont("arial", 22, bold=True)
        
        # CORRIGIDO: Usar a imagem da pasta imagens/
        try:
            self.icone_pato = pygame.image.load("assets/imagens/pato.png").convert_alpha()
        except:
            # Fallback: criar um ícone simples
            self.icone_pato = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(self.icone_pato, (255, 200, 50), (12, 12), 10)
            pygame.draw.polygon(self.icone_pato, (255, 150, 50), [(18, 10), (24, 12), (18, 14)])
        
        self.icone_pato = pygame.transform.scale(self.icone_pato, (24, 24))

    def desenhar(self, qtd_patos, pontuacao):
        fundo_rect = pygame.Rect(15, 15, 180, 70)
        pygame.draw.rect(self.tela, (0, 0, 0, 180), fundo_rect, border_radius=8)
        pygame.draw.rect(self.tela, (255, 215, 0), fundo_rect, width=2, border_radius=8)

        self.tela.blit(self.icone_pato, (25, 23))
        texto_patos = self.fonte.render(f"x {qtd_patos}", True, (255, 255, 255))
        self.tela.blit(texto_patos, (55, 23))

        texto_pontos = self.fonte.render(f"Pontos: {int(pontuacao)}", True, (255, 255, 255))
        self.tela.blit(texto_pontos, (25, 52))


class GerenciadorAudio:
    def __init__(self):
        pygame.mixer.init()
        
        # CORRIGIDO: Usar caminho assets/sons/
        try:
            self.som_pulo = pygame.mixer.Sound("assets/sons/pulo.wav")
            self.som_quack = pygame.mixer.Sound("assets/sons/quack.wav")
            self.som_colisao = pygame.mixer.Sound("assets/sons/colisao.wav")
        except FileNotFoundError:
            # Fallback: criar sons vazios
            print("⚠️ Arquivos de som não encontrados. Criando sons placeholder.")
            self.som_pulo = self._criar_beep(600, 0.15)
            self.som_quack = self._criar_beep(350, 0.2)
            self.som_colisao = self._criar_beep(120, 0.3)
        
        self.som_pulo.set_volume(0.3)
        self.som_quack.set_volume(0.5)
        self.som_colisao.set_volume(0.6)
        
        # Sons adicionais
        self.som_combo = self._criar_beep(440, 0.1)
        self.som_powerup = self._criar_beep(500, 0.15)
        self.som_conquista = self._criar_beep(600, 0.2)
        
        self.som_combo.set_volume(0.4)
        self.som_powerup.set_volume(0.5)
        self.som_conquista.set_volume(0.7)
    
    def _criar_beep(self, frequencia, duracao):
        """Cria um beep simples sem arquivo"""
        try:
            import numpy as np
            sample_rate = 22050
            num_samples = int(sample_rate * duracao)
            
            t = np.linspace(0, duracao, num_samples, False)
            wave = np.sin(2 * np.pi * frequencia * t)
            
            # Envelopamento
            envelope = np.exp(-t * 8)
            wave = wave * envelope
            
            # Converter para 16-bit
            wave = (wave * 32767).astype(np.int16)
            return pygame.mixer.Sound(buffer=wave.tobytes())
        except:
            # Fallback: som vazio
            return pygame.mixer.Sound(buffer=bytes([128]) * 1000)
    
    def tocar_pulo(self):
        self.som_pulo.play()

    def tocar_quack(self):
        self.som_quack.play()

    def tocar_colisao(self):
        self.som_colisao.play()
    
    def tocar_combo(self):
        self.som_combo.play()
    
    def tocar_powerup(self):
        self.som_powerup.play()
    
    def tocar_conquista(self):
        self.som_conquista.play()