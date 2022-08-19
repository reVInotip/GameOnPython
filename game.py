import pygame
import sys
from pygame.color import THECOLORS
from time import sleep
import os


WIDTH = 1000
HEIGHT = 600

pygame.init()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.blit(pygame.image.load(os.path.join(img_folder,'фон.png')), (-500, -250))


hero_walk_right_set = [pygame.image.load(os.path.join(img_folder,'base_rigth.png')), pygame.image.load(os.path.join(img_folder,'walk_rigth.png'))]
hero_walk_left_set = [pygame.image.load(os.path.join(img_folder,'base_left.png')), pygame.image.load(os.path.join(img_folder,'walk_left.png'))]
hero_hits_set = [pygame.image.load(os.path.join(img_folder,'right_hit.png')), pygame.image.load(os.path.join(img_folder,'left_hit.png'))]
dragon_set = [pygame.image.load(os.path.join(img_folder,'dragon.png')), pygame.image.load(os.path.join(img_folder,'dragon1.png'))]
fireball_set = [pygame.image.load(os.path.join(img_folder, 'fireball.png')), pygame.image.load(os.path.join(img_folder, 'fireball_left.png'))]

clock = pygame.time.Clock()


class Hero(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = hero_walk_right_set[0]
		self.rect = self.image.get_rect()
		self.rect.x = 450
		self.rect.y = 450
		self.frame = 0
		self.up = False; self.left = False; self.right = False; self.last_left = False; self.hit = False
		self.flag = False; self.flag1 = False; self.hit_time = True
		self.t = 0
		self.health = 300
		self.attack = 5
		self.impact_delay = 0

	def update(self):
		keys = pygame.key.get_pressed()#Список нажатых клавишь: True - нажата, False - нет
		mouse = pygame.mouse.get_pressed()#Список нажатых кнопок мыши: 0 - левая кнопка, 1 - колёсико, 2 - правая кнопка

		#Изменение координат при нажатии клавишь, при нажатии W срабатывает цикл в jump(),
		#который отвечает за изменение координаты при прыжке
		if keys[pygame.K_d]:
			self.rect.x += 5
			self.right = True
		if keys[pygame.K_a]:
			self.rect.x -= 5
			self.left = True
		if keys[pygame.K_w]:
			self.up = True			
		#if keys[pygame.K_s]:
			#self.rect.y -= 10 добавить блок на пробел
		if mouse[0]:
			self.hit = True

		if self.rect.x < 0:
			self.rect.x = 0
		if self.rect.x > 890:
			self.rect.x = 890

		self.jump()

		if not(self.hit_time):
			self.impact_delay += 1

		#Отрисовка срайта героя с учётом того, в какую сторону он идёт
		if self.left:
			if not(self.hit) or not(self.hit_time):
				self.image = hero_walk_left_set[int(self.frame)]
				if self.impact_delay == 5:
					self.hit_time = True
					self.impact_delay = 0
			elif self.hit_time:
				self.image = hero_hits_set[1]
				self.hit_time = False
			self.last_left = True
		elif self.right:
			if not(self.hit) or not(self.hit_time):
				self.image = hero_walk_right_set[int(self.frame)]
				if self.impact_delay == 5:
					self.hit_time = True
					self.impact_delay = 0
			elif self.hit_time:
				self.image = hero_hits_set[0]
				self.hit_time = False
			self.last_left = False

		if self.left == self.right:
			if self.last_left:
				if not(self.hit) or not(self.hit_time):
					self.image = hero_walk_left_set[0]
					if self.impact_delay == 5:
						self.hit_time = True
						self.impact_delay = 0
				elif self.hit_time:
					self.image = hero_hits_set[1]
					self.hit_time = False
			else:
				if not(self.hit) or not(self.hit_time):
					self.image = hero_walk_right_set[0]
					if self.impact_delay == 5:
						self.hit_time = True
						self.impact_delay = 0
				elif self.hit_time:
					self.image = hero_hits_set[0]
					self.hit_time = False

		self.frame += 0.1
		if self.frame >= 2:
			self.frame = 0

		self.left = False
		self.right = False
		self.hit = False


	def jump(self):#Функция отвечает заww прыжок
		#При нажатии W происходят расчёты координаты по оси y
		if self.up:
			self.flag = True
			v = 60 - 10 * self.t
			if v == 0: self.flag1 = True
			if not(self.flag1):
				self.rect.y = 450 - 60*self.t + (10*(self.t**2)//2)

		if self.rect.y > 450:
			self.t = 0
			self.flag1 = False
			self.flag = False
			self.up = False
			self.rect.y = 450

		if self.flag:
			#Значение t изменяется пока персонаж прыгает(пока не достигнет стартовой точки: y = 40)
			self.t += 0.8


class Dragon(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = dragon_set[0]
		self.image.set_colorkey((246, 246, 246))
		self.rect = self.image.get_rect()
		self.rect.x = 700#старотовые позиции
		self.rect.y = 300#по x и y
		self.flag = 1#текущая позиция дракона
		self.i = 0
		self.last_flag = 1#место, в котором дракон был в прошлый раз
		self.health = 985

	def update(self):
		# разделение на 2 последлвательности перемещений необходимо, что бы не возникало путанницы в
		# условиях
		if self.flag == 1:
			self.i = 0
			if self.rect.x == 700 and self.rect.y != 50:
				self.rect.y -= 25
			elif self.rect.y == 50 and self.rect.x != 100:
				self.image = dragon_set[1]
				self.image.set_colorkey((246, 246, 246)) 
				self.rect.x -= 50
			elif self.rect.x == 100 and self.rect.y != 300:
				self.image = dragon_set[1]
				self.image.set_colorkey((246, 246, 246)) 
				self.rect.y += 25
			else:
				self.flag = 0
		elif self.flag == 2:
			self.i = 0
			if self.rect.x == 100 and self.rect.y != 50:
				self.rect.y -= 25
			elif self.rect.y == 50 and self.rect.x != 700:
				self.image = dragon_set[0] 
				self.image.set_colorkey((246, 246, 246))
				self.rect.x += 50
			elif self.rect.x == 700 and self.rect.y != 300:
				self.image = dragon_set[0] 
				self.image.set_colorkey((246, 246, 246))
				self.rect.y += 25
			else:
				self.flag = 0
		else:
			# задержка в нижней позиции на некоторое время
			self.i += 1
			if self.i == 10:
				if self.last_flag == 1:
					self.flag = 2
					self.last_flag = 2
				else:
					self.flag = 1
					self.last_flag = 1


class Fireball(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = fireball_set[0]
		self.rect = self.image.get_rect()
		self.rect.x = 700#старотовые позиции
		self.rect.y = 300#по x и y
		self.i = dragon.i
		self.position = dragon.flag
		self.fireball = False

	def update(self):
		if self.i in (2, 5, 8):
			if self.position == 1:
				self.fireball = True
		if self.fireball:
			self.rect.x -= 10


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 985
    BAR_HEIGHT = 10
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, pct, BAR_HEIGHT)
    pygame.draw.rect(surf, THECOLORS['orange'], fill_rect)
    pygame.draw.rect(surf, THECOLORS['white'], outline_rect, 2)

def end_game():
	font = pygame.font.SysFont('arial', 100, bold=True, italic=False)
	text = font.render(str('You win!'), True, THECOLORS['orange'])
	screen.blit(text, (275, 250))

all_sprites = pygame.sprite.Group()
hero = Hero()
dragon = Dragon()
fireball = Fireball()
all_sprites.add(hero, dragon, fireball)
hit = False
run = True

#Цикл основной программы
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT or not(run): #Срабатывает при закрытии программы, или окончании игры
			pygame.quit()
			sys.exit()

	mouse = pygame.mouse.get_pressed()
	if mouse[0]:
		hit = True

	all_sprites.update()

	distance = pygame.sprite.collide_rect(hero, dragon)
	if distance and hit:
		dragon.health -= hero.attack
		if dragon.health <= 0:
			run = False

	#Отрисовка фона, а также обновление катинки на экране
	screen.blit(pygame.image.load(os.path.join(img_folder,'фон.png')), (-500, -250))
	all_sprites.draw(screen)
	pygame.draw.line(screen, THECOLORS['red'], (0, 567), (1000, 567), width=1)
	draw_shield_bar(screen, 5, 5, dragon.health)
	if not(run):
		end_game()

	pygame.display.flip()
	if not(run):
		sleep(5)
	clock.tick(90)