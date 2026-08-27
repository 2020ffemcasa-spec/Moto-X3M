# scripts/fisica.py
import math
from scripts.config import *

class Fisica:
    """Sistema de física para o jogo de motocross"""
    
    def __init__(self):
        self.gravidade = GRAVIDADE
        self.atrito_chao = ATRITO_CHAO
        self.atrito_ar = ATRITO_AR
        self.velocidade_maxima = VELOCIDADE_MAXIMA
    
    def aplicar_gravidade(self, objeto):
        """Aplica gravidade ao objeto"""
        objeto.velocidade_y += self.gravidade
        objeto.y += objeto.velocidade_y
    
    def aplicar_atrito(self, objeto, no_chao):
        """Aplica atrito baseado no estado (chão ou ar)"""
        if no_chao:
            objeto.velocidade_x *= self.atrito_chao
        else:
            objeto.velocidade_x *= self.atrito_ar
        
        # Para completamente se estiver quase parado
        if abs(objeto.velocidade_x) < 0.01:
            objeto.velocidade_x = 0
    
    def verificar_colisao_chao(self, objeto, terreno):
        """Verifica e corrige colisão com o chão"""
        altura = terreno.get_altura(objeto.x)
        metade_altura = objeto.rect.height // 2
        
        if objeto.y >= altura - metade_altura:
            objeto.y = altura - metade_altura
            if objeto.velocidade_y > 0:
                objeto.velocidade_y = 0
            return True
        return False
    
    def verificar_colisao_obstaculo(self, objeto, obstaculo):
        """Verifica colisão entre moto e obstáculo"""
        if not obstaculo.ativo:
            return False
        
        rect_moto = objeto.get_rect()
        rect_obst = obstaculo.get_rect()
        
        # Inflar o retângulo para colisão mais justa
        rect_moto_inflado = rect_moto.inflate(-5, -5)
        
        return rect_moto_inflado.colliderect(rect_obst)
    
    def verificar_colisao_colecionavel(self, objeto, colecionavel):
        """Verifica colisão entre moto e colecionável"""
        if not colecionavel.ativo:
            return False
        
        rect_moto = objeto.get_rect()
        rect_colec = colecionavel.get_rect()
        
        # Distância mais precisa (colisão circular)
        dx = rect_moto.centerx - rect_colec.centerx
        dy = rect_moto.centery - rect_colec.centery
        distancia = math.sqrt(dx*dx + dy*dy)
        
        raio_colisao = 25  # Raio de colisão
        return distancia < raio_colisao
    
    def aplicar_impulso(self, objeto, forca_x, forca_y):
        """Aplica um impulso ao objeto"""
        objeto.velocidade_x += forca_x
        objeto.velocidade_y += forca_y
    
    def aplicar_boost(self, objeto, multiplicador=1.8):
        """Aplica efeito de boost na velocidade"""
        if objeto.velocidade_x > 0:
            objeto.velocidade_x *= multiplicador
        # Limitar velocidade máxima com boost
        limite = self.velocidade_maxima * 1.5
        if abs(objeto.velocidade_x) > limite:
            objeto.velocidade_x = limite if objeto.velocidade_x > 0 else -limite
    
    def calcular_angulo_terreno(self, objeto, terreno, distancia=20):
        """Calcula o ângulo do terreno para a moto"""
        x1 = objeto.x - distancia
        x2 = objeto.x + distancia
        
        y1 = terreno.get_altura(x1)
        y2 = terreno.get_altura(x2)
        
        return math.atan2(y2 - y1, x2 - x1)
    
    def calcular_angulo_moto(self, objeto, terreno):
        """Calcula o ângulo da moto baseado no terreno e velocidade"""
        # Ângulo do terreno
        angulo_terreno = self.calcular_angulo_terreno(objeto, terreno)
        
        # Ângulo baseado na velocidade
        angulo_velocidade = objeto.velocidade_x * 0.3
        
        # Combinar ângulos (com suavização)
        angulo = math.degrees(angulo_terreno) * 0.6 + angulo_velocidade * 0.4
        
        # Limitar ângulo máximo
        return max(-30, min(30, angulo))
    
    def aplicar_pulo(self, objeto, forca=None):
        """Aplica pulo ao objeto"""
        forca_pulo = forca if forca is not None else FORCA_PULO
        objeto.velocidade_y = forca_pulo
    
    def verificar_queda(self, objeto, altura_maxima=ALTURA + 100):
        """Verifica se o objeto caiu da tela"""
        return objeto.y > altura_maxima
    
    def atualizar_posicao(self, objeto):
        """Atualiza a posição do objeto baseado na velocidade"""
        objeto.x += objeto.velocidade_x
        objeto.y += objeto.velocidade_y
        objeto.rect.center = (int(objeto.x), int(objeto.y))
    
    def aplicar_derrapagem(self, objeto):
        """Aplica efeito de derrapagem (frear bruscamente)"""
        # Reduz velocidade horizontal
        objeto.velocidade_x *= 0.8
        
        # Pequena perda de controle
        if abs(objeto.velocidade_x) > 1:
            objeto.velocidade_x += math.copysign(0.2, -objeto.velocidade_x)
        
        return abs(objeto.velocidade_x) > 2  # Retorna True se está derrapando
    
    def calcular_distancia_percorrida(self, objeto, dt=1):
        """Calcula a distância percorrida"""
        return abs(objeto.velocidade_x) * dt * 0.1
    
    def verificar_colisao_rampa(self, objeto, obstaculo):
        """Verifica colisão com rampa (impulsiona para cima)"""
        if not obstaculo.ativo or obstaculo.tipo != "rampa":
            return False
        
        rect_moto = objeto.get_rect()
        rect_rampa = obstaculo.get_rect()
        
        # Colisão mais precisa para rampa
        if rect_moto.colliderect(rect_rampa):
            # Aplicar impulso para cima
            self.aplicar_impulso(objeto, 0, -8)
            return True
        return False
    
    def calcular_velocidade_media(self, objeto, frame_anterior=None):
        """Calcula a velocidade média entre frames"""
        if frame_anterior is None:
            return 0
        return (objeto.velocidade_x - frame_anterior) / 2