# scripts/config.py

# ============================================
# CONFIGURAÇÕES DA TELA
# ============================================
LARGURA = 800
ALTURA = 500
FPS = 60
TITULO = "🏍️ Motocross Mayhem"

# ============================================
# CORES
# ============================================
CORES = {
    'branco': (255, 255, 255),
    'preto': (0, 0, 0),
    'vermelho': (255, 50, 50),
    'verde': (50, 205, 50),
    'verde_escuro': (34, 139, 34),
    'azul': (30, 144, 255),
    'azul_escuro': (25, 25, 112),
    'amarelo': (255, 215, 0),
    'laranja': (255, 165, 0),
    'cinza': (128, 128, 128),
    'cinza_claro': (200, 200, 200),
    'marrom': (139, 69, 19),
    'marrom_claro': (160, 120, 80),
    'dourado': (255, 215, 0),
    'rosa': (255, 100, 100),
    'ouro': (255, 215, 0),
     'roxo': (128, 0, 128),
     'ciano': (0, 255, 255), 
}

# ============================================
# FÍSICA
# ============================================
GRAVIDADE = 0.6
FORCA_PULO = -13
VELOCIDADE_MAXIMA = 10
ACELERACAO = 0.4
FRENAGEM = 0.3
ATRITO_AR = 0.98
ATRITO_CHAO = 0.92  # <-- ADICIONADO

# ============================================
# TERRENO
# ============================================
ALTURA_TERRENO = ALTURA - 100
TAMANHO_SEGMENTO = 8
LARGURA_TOTAL_PISTA = 10000  # 10km de pista

# ============================================
# POWER-UPS
# ============================================
DURACAO_BOOST = 180      # 3 segundos (60fps)
DURACAO_ESCUDO = 300     # 5 segundos
DURACAO_IMA = 480        # 8 segundos
DURACAO_PULO_DUPLO = 360 # 6 segundos

# ============================================
# SPAWN
# ============================================
SPAWN_OBSTACULO_MIN = 40   # frames mínimos entre obstáculos
SPAWN_OBSTACULO_MAX = 180  # frames máximos entre obstáculos
SPAWN_COLECIONAVEL_MIN = 20
SPAWN_COLECIONAVEL_MAX = 100

# ============================================
# CAMINHOS
# ============================================
PASTA_ASSETS = "assets/"
PASTA_IMAGENS = PASTA_ASSETS + "imagens/"
PASTA_SONS = PASTA_ASSETS + "sons/"