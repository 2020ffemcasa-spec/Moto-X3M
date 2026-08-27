# main.py - CORRIGIDO E COMPLETO
import pygame
import sys
import random
from scripts.config import *
from scripts.moto import Moto
from scripts.terreno import Terreno
from scripts.obstaculos import Obstaculo
from scripts.camera import Camera
from scripts.hud import HUD
from scripts.particulas import SistemaParticulas
from scripts.gerenciador_imagens import GerenciadorImagens
from scripts.fisica import Fisica
from scripts.colecionaveis import Colecionavel
from scripts.powerups import PowerUp

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)
relogio = pygame.time.Clock()

# ============================================
# INICIALIZAR SISTEMAS
# ============================================
gi = GerenciadorImagens()
terreno = Terreno(LARGURA)
moto = Moto(100, ALTURA_TERRENO - 30, gi)
camera = Camera(LARGURA, ALTURA)
hud = HUD(tela)
particulas = SistemaParticulas()
fisica = Fisica()

# ============================================
# VARIÁVEIS DO JOGO
# ============================================
obstaculos = []
colecionaveis = []
powerups = []
distancia = 0
recorde = 0
tempo_spawn_obstaculo = 0
tempo_spawn_colecionavel = 0
tempo_spawn_powerup = 0
game_over = False
jogando = True
offset_x = 0
offset_y = 0

# Tentar carregar recorde
try:
    with open("recorde.txt", "r") as f:
        recorde = int(f.read())
except:
    recorde = 0

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def resetar_jogo():
    """Reinicia o jogo completamente"""
    global moto, obstaculos, colecionaveis, powerups, distancia, game_over
    global particulas, tempo_spawn_obstaculo, tempo_spawn_colecionavel
    global tempo_spawn_powerup
    
    moto = Moto(100, ALTURA_TERRENO - 30, gi)
    obstaculos.clear()
    colecionaveis.clear()
    powerups.clear()
    distancia = 0
    game_over = False
    particulas = SistemaParticulas()
    tempo_spawn_obstaculo = 0
    tempo_spawn_colecionavel = 0
    tempo_spawn_powerup = 0

def spawnar_obstaculo():
    """Spawna um novo obstáculo"""
    x = camera.x + LARGURA + random.randint(50, 200)
    
    # Tipos de obstáculos com pesos (probabilidades)
    tipos = ["cone"] * 4 + ["barreira"] * 2 + ["caixa"] * 2 + ["rampa"] * 1
    
    # Adicionar obstáculos mais difíceis com a distância
    if distancia > 300:
        tipos += ["pneu"] * 2
    if distancia > 500:
        tipos += ["espinho"] * 2
    
    tipo = random.choice(tipos)
    altura = terreno.get_altura(x)
    obstaculo = Obstaculo(x, tipo, gi)
    obstaculo.altura_terreno = altura
    obstaculos.append(obstaculo)

def spawnar_colecionavel():
    """Spawna um novo colecionável"""
    x = camera.x + LARGURA + random.randint(100, 300)
    y_base = terreno.get_altura(x)
    y = y_base - random.randint(30, 80)
    
    # 70% moeda, 30% estrela
    tipo = "moeda" if random.random() < 0.7 else "estrela"
    colecionavel = Colecionavel(x, y, tipo, gi)
    colecionaveis.append(colecionavel)

def spawnar_powerup():
    """Spawna um novo power-up"""
    x = camera.x + LARGURA + random.randint(200, 400)
    y_base = terreno.get_altura(x)
    y = y_base - 50
    
    tipos_powerup = ["boost", "escudo", "ima", "pulo_duplo"]
    tipo = random.choice(tipos_powerup)
    powerup = PowerUp(x, y, tipo, gi)
    powerups.append(powerup)

# ============================================
# LOOP PRINCIPAL
# ============================================

while jogando:
    # --- EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not game_over:
                if moto.pular():
                    particulas.adicionar_explosao(
                        moto.x, moto.y + 20,
                        (200, 220, 255), 10, 1
                    )
            
            if evento.key == pygame.K_r and game_over:
                resetar_jogo()
            
            if evento.key == pygame.K_b and not game_over:
                moto.ativar_boost()
            
            if evento.key == pygame.K_ESCAPE:
                jogando = False
    
    # --- TECLAS PRESSIONADAS ---
    if not game_over:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            moto.acelerar(1)
            # Partículas de poeira
            if moto.no_chao and random.random() < 0.3:
                particulas.adicionar_explosao(
                    moto.x - 10, moto.y + 10,
                    (180, 150, 100), 3, 0.5
                )
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            moto.acelerar(-1)
        else:
            # Desacelerar naturalmente
            if moto.no_chao:
                moto.velocidade_x *= 0.95
        
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            if fisica.aplicar_derrapagem(moto):
                particulas.adicionar_explosao(
                    moto.x, moto.y + 10,
                    (200, 150, 100), 5, 2
                )
    
    # --- ATUALIZAÇÃO ---
    if not game_over:
        # Aplicar física
        fisica.aplicar_gravidade(moto)
        
        # Verificar colisão com o chão
        no_chao = fisica.verificar_colisao_chao(moto, terreno)
        moto.no_chao = no_chao
        
        # Aplicar atrito
        fisica.aplicar_atrito(moto, no_chao)
        
        # Calcular ângulo da moto
        angulo = fisica.calcular_angulo_moto(moto, terreno)
        moto.angulo = angulo
        
        # Atualizar moto (física adicional)
        moto.atualizar(terreno)
        
        # Atualizar distância
        distancia += fisica.calcular_distancia_percorrida(moto)
        
        # Atualizar câmera
        camera.seguir(moto.x, moto.y)
        offset_x, offset_y = camera.get_offset()
        
        # --- SPAWNS ---
        # Obstáculos
        tempo_spawn_obstaculo += 1
        intervalo_spawn = max(40, 180 - int(distancia * 0.02))
        if tempo_spawn_obstaculo > random.randint(40, intervalo_spawn):
            spawnar_obstaculo()
            tempo_spawn_obstaculo = 0
        
        # Colecionáveis
        tempo_spawn_colecionavel += 1
        if tempo_spawn_colecionavel > random.randint(20, 80):
            spawnar_colecionavel()
            tempo_spawn_colecionavel = 0
        
        # Power-ups (mais raros)
        tempo_spawn_powerup += 1
        if tempo_spawn_powerup > random.randint(300, 600):
            spawnar_powerup()
            tempo_spawn_powerup = 0
        
        # --- ATUALIZAR OBJETOS ---
        # Obstáculos
        for obstaculo in obstaculos[:]:
            altura_terreno = terreno.get_altura(obstaculo.x)
            obstaculo.atualizar(0, altura_terreno)
            
            # Verificar colisão com obstáculo
            if fisica.verificar_colisao_obstaculo(moto, obstaculo):
                if obstaculo.tipo == "rampa":
                    # Rampa - impulso para cima
                    fisica.aplicar_impulso(moto, 0, -12)
                    particulas.adicionar_explosao(
                        obstaculo.x, obstaculo.altura_terreno - 20,
                        (200, 200, 100), 15, 2
                    )
                    obstaculo.ativo = False
                elif moto.escudo_ativo:
                    # Escudo ativo - destrói obstáculo sem dano
                    particulas.adicionar_explosao(
                        obstaculo.x, obstaculo.altura_terreno - 20,
                        (30, 144, 255), 20, 3
                    )
                    obstaculo.ativo = False
                else:
                    # Colidiu - Game Over
                    particulas.adicionar_explosao(
                        obstaculo.x, obstaculo.altura_terreno - 20,
                        (255, 50, 50), 30, 4
                    )
                    game_over = True
                    
                    # Salvar recorde
                    if distancia > recorde:
                        recorde = int(distancia)
                        with open("recorde.txt", "w") as f:
                            f.write(str(recorde))
                    break
            
            if not obstaculo.ativo:
                obstaculos.remove(obstaculo)
        
        # Colecionáveis
        for colecionavel in colecionaveis[:]:
            colecionavel.atualizar()
            
            # Verificar colisão com colecionável
            if fisica.verificar_colisao_colecionavel(moto, colecionavel):
                if colecionavel.tipo == "moeda":
                    moto.pontos += 5
                    moto.moedas += 1
                else:  # estrela
                    moto.pontos += 25
                    moto.moedas += 2
                
                particulas.adicionar_explosao(
                    colecionavel.x, colecionavel.y,
                    (255, 215, 0), 15, 2
                )
                colecionavel.ativo = False
            
            if not colecionavel.ativo:
                colecionaveis.remove(colecionavel)
        
        # Power-ups
        for powerup in powerups[:]:
            powerup.atualizar()
            
            # Verificar colisão com power-up
            if fisica.verificar_colisao_colecionavel(moto, powerup):
                if powerup.tipo == "boost":
                    moto.ativar_boost()
                elif powerup.tipo == "escudo":
                    moto.ativar_escudo()
                elif powerup.tipo == "ima":
                    moto.ativar_ima()
                elif powerup.tipo == "pulo_duplo":
                    moto.ativar_pulo_duplo()
                
                particulas.adicionar_explosao(
                    powerup.x, powerup.y,
                    (0, 255, 100), 25, 3
                )
                powerup.ativo = False
            
            if not powerup.ativo:
                powerups.remove(powerup)
        
        # --- EFEITO IMÃ ---
        if moto.ima_ativo:
            for colecionavel in colecionaveis:
                dx = moto.x - colecionavel.x
                dy = moto.y - colecionavel.y
                dist = (dx*dx + dy*dy) ** 0.5
                if dist < 200 and dist > 10:
                    fator = 3 / (dist + 1)
                    colecionavel.x += dx * fator
                    colecionavel.y += dy * fator
        
        # Atualizar partículas
        particulas.update()
        
        # Verificar se caiu da tela
        if fisica.verificar_queda(moto):
            game_over = True
            if distancia > recorde:
                recorde = int(distancia)
                with open("recorde.txt", "w") as f:
                    f.write(str(recorde))
    
    # --- RENDERIZAÇÃO ---
    tela.fill(CORES['azul'])
    
    # Desenhar terreno
    terreno.desenhar(tela, offset_x)
    
    # Desenhar power-ups
    for powerup in powerups:
        powerup.desenhar(tela, offset_x)
    
    # Desenhar colecionáveis
    for colecionavel in colecionaveis:
        colecionavel.desenhar(tela, offset_x)
    
    # Desenhar obstáculos
    for obstaculo in obstaculos:
        obstaculo.desenhar(tela, offset_x)
    
    # Desenhar moto
    moto.desenhar(tela, offset_x)
    
    # Desenhar partículas
    particulas.draw(tela)
    
    # Desenhar HUD
    hud.desenhar(distancia, moto.velocidade_x, moto.boost_ativo, 
                 moto.tempo_boost, recorde, moto.pontos, moto.moedas)
    
    # Efeitos de power-up ativos (texto na tela)
    if moto.escudo_ativo:
        fonte = pygame.font.SysFont("arial", 20, bold=True)
        texto = fonte.render("🛡️ ESCUDO ATIVO", True, (30, 144, 255))
        tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 80))
    
    if moto.boost_ativo:
        fonte = pygame.font.SysFont("arial", 20, bold=True)
        texto = fonte.render("⚡ BOOST ATIVO!", True, (255, 165, 0))
        tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 50))
    
    if moto.pulo_duplo_ativo:
        fonte = pygame.font.SysFont("arial", 20, bold=True)
        texto = fonte.render("🦘 PULO DUPLO!", True, (50, 205, 50))
        tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 110))
    
    # --- GAME OVER ---
    if game_over:
        s = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        tela.blit(s, (0, 0))
        
        fonte_go = pygame.font.SysFont("arial", 72, bold=True)
        texto_go = fonte_go.render("💀 GAME OVER", True, CORES['vermelho'])
        tela.blit(texto_go, (LARGURA//2 - texto_go.get_width()//2, ALTURA//2 - 120))
        
        fonte_info = pygame.font.SysFont("arial", 28)
        
        # Distância
        texto_dist = fonte_info.render(f"🏁 Distância: {int(distancia)}m", True, CORES['branco'])
        tela.blit(texto_dist, (LARGURA//2 - texto_dist.get_width()//2, ALTURA//2 - 50))
        
        # Recorde
        if distancia >= recorde:
            texto_rec = fonte_info.render("🏆 NOVO RECORDE!", True, CORES['ouro'])
        else:
            texto_rec = fonte_info.render(f"🏆 Recorde: {recorde}m", True, CORES['ouro'])
        tela.blit(texto_rec, (LARGURA//2 - texto_rec.get_width()//2, ALTURA//2 - 10))
        
        # Pontos
        texto_pts = fonte_info.render(f"⭐ Pontos: {moto.pontos}", True, CORES['amarelo'])
        tela.blit(texto_pts, (LARGURA//2 - texto_pts.get_width()//2, ALTURA//2 + 30))
        
        # Moedas
        texto_moedas = fonte_info.render(f"🪙 Moedas: {moto.moedas}", True, CORES['cinza_claro'])
        tela.blit(texto_moedas, (LARGURA//2 - texto_moedas.get_width()//2, ALTURA//2 + 70))
        
        # Instruções
        texto_reset = fonte_info.render("Pressione 'R' para reiniciar", True, CORES['branco'])
        tela.blit(texto_reset, (LARGURA//2 - texto_reset.get_width()//2, ALTURA//2 + 130))
        
        texto_menu = fonte_info.render("Pressione 'ESC' para sair", True, CORES['cinza'])
        tela.blit(texto_menu, (LARGURA//2 - texto_menu.get_width()//2, ALTURA//2 + 170))
    
    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
sys.exit()