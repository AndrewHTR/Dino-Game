import pygame, sys, os, random
from pygame.locals import *

diretorio_principal = os.path.dirname(__file__) # Pega o diretorio absoluto de onde este arquivo se encontra
diretorio_imagens   = os.path.join(diretorio_principal, 'img') # Procura pelo diretorio img
diretorio_sons      = os.path.join(diretorio_principal, 'sounds') # Procura pelo diretorio sounds

LARGURA = 640 # Largura da janela
ALTURA = 480 # Altura da janela

BRANCO = (255, 255, 255) # Cor branca
PRETO = (0, 0, 0) # Cor preta

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((LARGURA, ALTURA)) # Inicializando tela
pygame.display.set_caption('Dino Game')
clock = pygame.time.Clock() # Variavel que define os frames do jogo

# Pegando a sprite sheet e mantendo a transparência da imagem 
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha() 

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'sons_death_sound.wav'))
som_colisao.set_volume(0.3)

som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, "sons_score_sound.wav"))
som_pontuacao.set_volume(0.3)
escolha_obstaculo = random.choice([0, 1])
pontos = 0
velocidade_jogo = 10

def texto(msg, tamanho, cor):
	fonte = pygame.font.SysFont('Arial', tamanho, True, False)
	txt = f"{msg}"
	txt_formatado = fonte.render(txt, True, cor)
	return txt_formatado

def reiniciar_jogo():
	global pontos, velocidade_jogo, colidiu, escolha_obstaculo
	pontos = 0
	velocidade_jogo = 10
	colidiu = False
	dino.rect.y = ALTURA - 64 - 96//2
	dino.pulo = False
	voador.rect.x = LARGURA
	cacto.rect.x = LARGURA
	escolha_obstaculo = random.choice([0, 1])

# Classe do player (dinossauro)
class Dino(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) # Inicianlizando Herança
		self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'sons_jump_sound.wav'))
		self.som_pulo.set_volume(0.3)
		self.sprites_dino = [] # Criando lista com os sprites
		for i in range(3): # loop que se repete duas vezes
			img = self.img  = sprite_sheet.subsurface((i * 32,0), (32, 32)) # Pegando cada frame multiplicando o i que se repete duas vezes
			img = pygame.transform.scale(img, (32 * 3, 32 * 3)) # Transformando a escala da imagem
			self.sprites_dino.append(img) # Adicionando as imagens a lista

		self.index_lista = 0 # Variavel para manipular index da lista self.sprites_dino
		self.image = self.sprites_dino[self.index_lista]

		self.rect = self.image.get_rect() # Pegando retangulo da sprite
		self.mask = pygame.mask.from_surface(self.image)
		self.pos_y_init = ALTURA - 64 - 96 // 2
		self.rect.center = (130, ALTURA - 64) # Colocando sprite no X e Y da janela
		self.pulo = False

	def pular(self):
		self.pulo = True
		self.som_pulo.play()


	def update(self):
		if self.pulo == True:
			if self.rect.y <= 230:
				self.pulo = False
			self.rect.y -= 18
		else:
			if self.rect.y < self.pos_y_init:
				self.rect.y += 18 
			else: 
				self.rect.y = self.pos_y_init

		if self.index_lista > 2:
			self.index_lista = 0
		self.index_lista += 0.25
		self.image = self.sprites_dino[int(self.index_lista)]

class Nuvens(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = sprite_sheet.subsurface((32 * 7, 0), (32, 32))
		self.image = pygame.transform.scale(self.image, (32 * 3, 32* 3))

		self.rect = self.image.get_rect()
		self.rect.y = random.randrange(50, 200, 50)
		self.rect.x = LARGURA - random.randrange(30, 300, 90)

	def update(self):
		if self.rect.topright[0] < 0:
			self.rect.x = LARGURA
			self.rect.y = random.randrange(50, 200, 50)

		self.rect.x -= velocidade_jogo

class Chao(pygame.sprite.Sprite):
	def __init__(self, pos_x):
		pygame.sprite.Sprite.__init__(self)
		self.image = sprite_sheet.subsurface((32*6, 0), (32, 32))
		self.image = pygame.transform.scale(self.image, (32*2, 32*2))

		self.rect   = self.image.get_rect()
		self.rect.y = ALTURA - 64
		self.rect.x = pos_x * 64

	def update(self):
		if self.rect.topright[0] < 0:
			self.rect.x = LARGURA
		self.rect.x -= 13

class Cacto(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = sprite_sheet.subsurface((32*5, 0), (32, 32))
		self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))

		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.escolha = escolha_obstaculo
		self.rect.center = (LARGURA, ALTURA - 64)
		self.rect.x = LARGURA

	def update(self):
		if self.escolha == 0:
			if self.rect.topright[0] < 0:
				self.rect.x = LARGURA
			self.rect.x -= velocidade_jogo

class Voador(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.sprites = []
		for i in range(3, 5): # loop que se repete duas vezes
			
			img = sprite_sheet.subsurface((i * 32,0), (32, 32)) # Pegando cada frame multiplicando o i que se repete duas vezes
			img = pygame.transform.scale(img, (32 * 3, 32 * 3)) # Transformando a escala da imagem
			self.sprites.append(img) # Adicionando as imagens a lista

		self.index_lista = 0 # Variavel para manipular index da lista self.sprites_dino
		self.image = self.sprites[self.index_lista]
		self.mask = pygame.mask.from_surface(self.image)
		self.escolha = escolha_obstaculo
		self.rect = self.image.get_rect()
		self.rect.center = (LARGURA, 300)
		self.rect.x = LARGURA


	def update(self):
		if self.escolha == 1:
			if self.rect.topright[0] < 0:
				self.rect.x = LARGURA
			self.rect.x -= velocidade_jogo
			
			if self.index_lista > 1:
				self.index_lista = 0
			self.index_lista += 0.25
			self.image = self.sprites[int(self.index_lista)]

all_sprites = pygame.sprite.Group()
dino = Dino()
all_sprites.add(dino)
for i in range(4):
	nuvens = Nuvens()
	all_sprites.add(nuvens)

for i in range(11):
	chao = Chao(i)
	all_sprites.add(chao)

cacto = Cacto()
all_sprites.add(cacto)

voador = Voador()
all_sprites.add(voador)

obstacle_sprite = pygame.sprite.Group()
obstacle_sprite.add(cacto)
obstacle_sprite.add(voador)

colidiu = False
escolha_obstaculo = random.choice([0, 1])
while True:
	clock.tick(30)
	screen.fill(BRANCO)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == KEYDOWN:
			if event.key == K_SPACE and colidiu == False:
				if dino.rect.y != dino.pos_y_init:
					pass
				else:
					dino.pular()
			if event.key == K_r and colidiu == True:
				reiniciar_jogo()

	colisoes = pygame.sprite.spritecollide(dino, obstacle_sprite, False, pygame.sprite.collide_mask)
	all_sprites.draw(screen)

	if cacto.rect.topright[0] <= 0 or voador.rect.topright[0] <= 0:
		escolha_obstaculo = random.choice([0, 1])
		cacto.rect.x  = LARGURA
		voador.rect.x = LARGURA

		cacto.escolha = escolha_obstaculo
		voador.escolha = escolha_obstaculo

	if colisoes and colidiu == False:
		som_colisao.play()
		colidiu = True
	if colidiu == True:
		if pontos % 100 == 0:
			pontos += 1
		txt_game_over = texto('GAME OVER', 55, PRETO)
		screen.blit(txt_game_over, (LARGURA//2 - 45, ALTURA//2))
		txt_restart = texto('Pressione R para reiniciar!', 20, PRETO)
		screen.blit(txt_restart, (LARGURA//2, ALTURA//2 + 60))

	else:
		pontos += 1
		all_sprites.update()
		texto_pontos = texto(pontos, 40, PRETO)

	if pontos % 100 == 0:
		som_pontuacao.play()
		if velocidade_jogo <= 23:
			velocidade_jogo += 1

	screen.blit(texto_pontos, (LARGURA - 140, 30))
	pygame.display.flip()
