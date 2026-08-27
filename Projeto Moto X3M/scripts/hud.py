# scripts/hud.py
import pygame
from scripts.config import *

class HUD:
    def __init__(self, tela):
        self.tela = tela
        self.fonte_grande = pygame.font.SysFont("arial", 36, bold=True)
        self.fonte_media = pygame.font.SysFont("arial", 24)
        self.fonte_pequena = pygame.font.SysFont("arial", 16)
        self.fonte_titulo = pygame.font.SysFont("arial", 20, bold=True)
        
        # Cores
        self.cor_fundo = (0, 0, 0, 180)
        self.cor_borda = (255, 215, 0)
        self.cor_ouro = (255, 215, 0)
        self.cor_laranja = (255, 165, 0)
        self.cor_amarelo = (255, 215, 0)
        self.cor_cinza = (128, 128, 128)
        self.cor_cinza_claro = (200, 200, 200)
        self.cor_branco = (255, 255, 255)
        
        # Ícone de boost
        self.icone_boost = None
        try:
            self.icone_boost = pygame.image.load("assets/imagens/boost.png")
            self.icone_boost = pygame.transform.scale(self.icone_boost, (25, 25))
        except:
            pass
    
    def desenhar(self, distancia, velocidade, boost_ativo, tempo_boost, recorde, pontos=0, moedas=0):
        """Desenha todos os elementos do HUD"""
        
        # --- PAINEL SUPERIOR ESQUERDO ---
        painel_x, painel_y = 10, 10
        painel_largura, painel_altura = 200, 70
        
        # Fundo do painel
        surf = pygame.Surface((painel_largura, painel_altura), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 150))
        self.tela.blit(surf, (painel_x, painel_y))
        
        # Borda
        pygame.draw.rect(self.tela, self.cor_amarelo, 
                        (painel_x, painel_y, painel_largura, painel_altura), 2, border_radius=4)
        
        # Distância
        texto_dist = self.fonte_grande.render(f"🏁 {int(distancia)}m", True, self.cor_branco)
        self.tela.blit(texto_dist, (painel_x + 15, painel_y + 5))
        
        # Velocidade
        texto_vel = self.fonte_media.render(f"⚡ {int(abs(velocidade))} km/h", True, self.cor_amarelo)
        self.tela.blit(texto_vel, (painel_x + 15, painel_y + 40))
        
        # --- RECORDE (canto superior direito) ---
        rec_x = LARGURA - 180
        rec_y = 10
        surf_rec = pygame.Surface((170, 35), pygame.SRCALPHA)
        surf_rec.fill((0, 0, 0, 150))
        self.tela.blit(surf_rec, (rec_x, rec_y))
        pygame.draw.rect(self.tela, self.cor_ouro, (rec_x, rec_y, 170, 35), 2, border_radius=4)
        
        texto_rec = self.fonte_media.render(f"🏆 Recorde: {recorde}m", True, self.cor_ouro)
        self.tela.blit(texto_rec, (rec_x + 10, rec_y + 5))
        
        # --- BOOST (canto superior direito, abaixo do recorde) ---
        if boost_ativo:
            boost_x = rec_x
            boost_y = rec_y + 45
            
            # Fundo
            surf_boost = pygame.Surface((170, 50), pygame.SRCALPHA)
            surf_boost.fill((0, 0, 0, 150))
            self.tela.blit(surf_boost, (boost_x, boost_y))
            pygame.draw.rect(self.tela, self.cor_laranja, 
                           (boost_x, boost_y, 170, 50), 2, border_radius=4)
            
            # Ícone
            if self.icone_boost:
                self.tela.blit(self.icone_boost, (boost_x + 10, boost_y + 10))
            
            # Texto BOOST!
            texto_boost = self.fonte_titulo.render("BOOST!", True, self.cor_laranja)
            self.tela.blit(texto_boost, (boost_x + 45, boost_y + 5))
            
            # Barra de boost
            largura_barra = 100
            preenchimento = (tempo_boost / 180) * largura_barra
            barra_x = boost_x + 45
            barra_y = boost_y + 30
            
            pygame.draw.rect(self.tela, self.cor_cinza, (barra_x, barra_y, largura_barra, 8))
            pygame.draw.rect(self.tela, self.cor_laranja, (barra_x, barra_y, preenchimento, 8))
        
        # --- PONTOS E MOEDAS (canto inferior esquerdo) ---
        info_x = 10
        info_y = ALTURA - 50
        
        surf_info = pygame.Surface((180, 40), pygame.SRCALPHA)
        surf_info.fill((0, 0, 0, 150))
        self.tela.blit(surf_info, (info_x, info_y))
        pygame.draw.rect(self.tela, self.cor_amarelo, 
                        (info_x, info_y, 180, 40), 2, border_radius=4)
        
        texto_pontos = self.fonte_media.render(f"⭐ {pontos}", True, self.cor_amarelo)
        self.tela.blit(texto_pontos, (info_x + 15, info_y + 8))
        
        texto_moedas = self.fonte_media.render(f"🪙 {moedas}", True, self.cor_cinza_claro)
        self.tela.blit(texto_moedas, (info_x + 100, info_y + 8))
        
        # --- CONTROLES (canto inferior direito) ---
        ctrl_x = LARGURA - 200
        ctrl_y = ALTURA - 50
        
        surf_ctrl = pygame.Surface((190, 40), pygame.SRCALPHA)
        surf_ctrl.fill((0, 0, 0, 150))
        self.tela.blit(surf_ctrl, (ctrl_x, ctrl_y))
        pygame.draw.rect(self.tela, self.cor_cinza, 
                        (ctrl_x, ctrl_y, 190, 40), 2, border_radius=4)
        
        texto_ctrl = self.fonte_pequena.render("← → Acelerar  |  ↓ Frear", True, self.cor_cinza_claro)
        self.tela.blit(texto_ctrl, (ctrl_x + 10, ctrl_y + 5))
        
        texto_ctrl2 = self.fonte_pequena.render("ESPAÇO Pular  |  B Boost", True, self.cor_cinza_claro)
        self.tela.blit(texto_ctrl2, (ctrl_x + 10, ctrl_y + 20))