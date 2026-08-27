# gerar_assets.py
import os
import pygame

pygame.init()

# Criar pastas
os.makedirs("assets/imagens", exist_ok=True)
os.makedirs("assets/sons", exist_ok=True)

print("🎨 Gerando imagens placeholder...")

# ---------- MOTO ----------
moto = pygame.Surface((40, 30), pygame.SRCALPHA)
pygame.draw.ellipse(moto, (200, 50, 50), (10, 10, 30, 15))
pygame.draw.circle(moto, (30, 30, 30), (15, 25), 6)
pygame.draw.circle(moto, (30, 30, 30), (25, 25), 6)
pygame.draw.rect(moto, (50, 50, 200), (20, 0, 10, 12))
pygame.draw.circle(moto, (255, 200, 50), (22, 5), 4)
pygame.image.save(moto, "assets/imagens/moto.png")

# Moto rodando
moto_rodando = moto.copy()
pygame.draw.circle(moto_rodando, (100, 100, 100), (15, 25), 4)
pygame.draw.circle(moto_rodando, (100, 100, 100), (25, 25), 4)
pygame.image.save(moto_rodando, "assets/imagens/moto_rodando.png")

# Moto pulando
moto_pulando = pygame.Surface((40, 35), pygame.SRCALPHA)
pygame.draw.ellipse(moto_pulando, (200, 50, 50), (10, 15, 30, 15))
pygame.draw.circle(moto_pulando, (30, 30, 30), (15, 30), 6)
pygame.draw.circle(moto_pulando, (30, 30, 30), (25, 30), 6)
pygame.draw.rect(moto_pulando, (50, 50, 200), (20, 5, 10, 12))
pygame.draw.circle(moto_pulando, (255, 200, 50), (22, 8), 4)
pygame.image.save(moto_pulando, "assets/imagens/moto_pulando.png")

# ---------- OBSTÁCULOS ----------
cone = pygame.Surface((20, 30), pygame.SRCALPHA)
pygame.draw.polygon(cone, (255, 165, 0), [(10, 0), (0, 30), (20, 30)])
pygame.draw.rect(cone, (255, 255, 255), (6, 20, 8, 3))
pygame.image.save(cone, "assets/imagens/obstaculo_cone.png")

barreira = pygame.Surface((60, 40), pygame.SRCALPHA)
pygame.draw.rect(barreira, (200, 30, 30), (0, 0, 60, 40))
for i in range(4):
    pygame.draw.rect(barreira, (255, 255, 255), (5 + i*15, 5, 8, 30))
pygame.image.save(barreira, "assets/imagens/obstaculo_barreira.png")

rampa = pygame.Surface((80, 20), pygame.SRCALPHA)
pygame.draw.polygon(rampa, (139, 69, 19), [(0, 20), (80, 20), (80, 0)])
pygame.image.save(rampa, "assets/imagens/rampa.png")

# ---------- BOOST ----------
boost = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.draw.circle(boost, (255, 165, 0), (15, 15), 12)
pygame.draw.circle(boost, (255, 200, 50), (15, 15), 8)
pygame.draw.polygon(boost, (255, 255, 255), [(22, 12), (30, 15), (22, 18)])
pygame.image.save(boost, "assets/imagens/boost.png")

print("✅ Imagens geradas!")
pygame.quit()