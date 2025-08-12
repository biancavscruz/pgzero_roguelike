import pgzero
import math
import random
from pygame import Rect
import pgzrun
from pgzero.builtins import Actor, keyboard
from pgzero.clock import schedule_interval
from random import randint

#background_game limites
#tamanho dos tiles e do mundo
TILE_WIDTH = 32
TILE_HEIGHT = 32  
WIDTH = 960  # 30 blocos
HEIGHT = 544 #17 blocos
TITLE = "Cow vs Aliens"  # titulo da janela flutuante
tilemap = [[-1 for _ in range(30)] for _ in range(16)]

game_state = "menu"
music_on = True
music.play('music_menu')
sounds.enemy1_walk.set_volume(0.3)
sounds.enemy2_flying.set_volume(0.8)

background_menu = Actor("background_menu") # fundo
background_game = Actor("background_game")

button_start = Actor('button_start')  # botões do menu
button_music_on = Actor('button_music_on')
button_music_off = Actor('button_music_off')
button_exit = Actor('button_exit')

button_start.pos = (WIDTH // 2, 200)
button_music_on.pos = (WIDTH // 2, 260)
button_music_off.pos = (WIDTH // 2, 260)
button_exit.pos = (WIDTH // 2, 320)

tilemap = [
    [120, 120, 120, 0, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 0, 120, 120, 68, 69, 69, 69,
     69, 69, 69, 69, 69, 68, 120, 120, 120, 120],

    [120, 120, 120, 0, 221, 221, 221, 221, 221, 221,
     221, 221, 221, 1, 0, 120, 68, 221, 221, 221,
     221, 221, 221, 221, 221, 69, 68, 120, 120, 120],

    [120, 120, 120, 0, 221, 221, 221, 221, 221, 221,
     221, 221, 221, 221, 0, 120, 68, 221, 221, 221,
     221, 221, 221, 221, 221, 221, 69, 68, 120, 120],

    [120, 120, 120, 1, 1, 1, 0, 221, 221, 221,
     221, 221, 221, 221, 0, 120, 68, 221, 221, 221,
     241, 221, 221, 221, 240, 221, 221, 68, 120, 120],

    [119, 119, 120, 119, 119, 120, 1, 0, 221, 221,
     240, 221, 0, 1, 1, 120, 68, 221, 221, 221,
     221, 221, 221, 221, 221, 221, 222, 68, 120, 120],

    [119, 113, 119, 115, 119, 119, 119, 0, 221, 241,
     0, 1, 1, 120, 120, 120, 68, 221, 221, 221,
     221, 221, 221, 221, 221, 221, 221, 69, 68, 120],

    [119, 119, 119, 119, 119, 17, 18, 18, 221, 221,
     17, 120, 120, 120, 120, 120, 68, 221, 221, 221,
     221, 221, 221, 221, 221, 221, 221, 221, 68, 120],

    [119, 119, 17, 18, 18, 18, 221, 221, 221, 221,
     18, 18, 17, 120, 120, 120, 68, 221, 221, 221,
     221, 240, 221, 241, 221, 68, 69, 69, 69, 120],

    [114, 119, 17, 221, 221, 221, 221, 221, 221, 221,
     221, 240, 18, 18, 69, 69, 69, 221, 221, 68,
     69, 69, 69, 69, 69, 69, 120, 120, 120, 120],

    [17, 18, 18, 221, 221, 221, 221, 221, 221, 221,
     221, 221, 221, 221, 221, 221, 221, 221, 221, 68,
     120, 120, 120, 120, 120, 120, 120, 120, 120, 120],

    [17, 221, 241, 221, 221, 240, 221, 221, 221, 240,
     221, 221, 221, 221, 221, 221, 221, 221, 221, 35,
     35, 35, 35, 35, 35, 35, 35, 35, 35, 34],

    [17, 221, 221, 221, 221, 221, 221, 221, 223, 221,
     221, 221, 221, 221, 221, 221, 221, 221, 221, 221,
     221, 240, 221, 221, 221, 221, 221, 221, 221, 34],

    [17, 221, 221, 221, 221, 221, 221, 221, 221, 221,
     221, 17, 18, 34, 221, 221, 221, 221, 221, 221,
     221, 221, 221, 221, 221, 221, 241, 221, 221, 34],

    [17, 221, 221, 221, 221, 221, 221, 221, 221, 221,
     221, 17, 120, 34, 221, 221, 221, 221, 221, 221,
     221, 221, 221, 221, 221, 221, 221, 221, 221, 34],

    [17, 221, 221, 221, 221, 241, 221, 221, 240, 221,
     17, 18, 120, 34, 221, 221, 221, 221, 221, 221,
     221, 221, 221, 221, 221, 221, 221, 221, 221, 34],

    [17, 221, 221, 221, 221, 221, 221, 221, 221, 221,
     17, 120, 120, 35, 34, 221, 221, 221, 240, 221,
     221, 241, 221, 221, 221, 221, 224, 221, 221, 34],

    [18, 18, 18, 18, 18, 18, 18, 18, 18, 18,
     18, 120, 120, 120, 35, 35, 35, 35, 35, 35,
     35, 35, 35, 35, 35, 35, 35, 35, 35, 35]
]

#valores que representam chão livre (andáveis)
walkable_values = {221, 222, 223, 224, 240, 241}

walls = []
for r, row in enumerate(tilemap):
    for c, val in enumerate(row):
        if val not in walkable_values:
            x = c * TILE_WIDTH
            y = r * TILE_HEIGHT
            walls.append(Rect((x, y), (TILE_WIDTH, TILE_HEIGHT)))

def collides_with_walls(actor, pad=8):
    hb = Rect(
        actor.left + pad,
        actor.top + pad,
        actor.width - 2*pad,
        actor.height - 2*pad)
    return any(hb.colliderect(w) for w in walls)

def move_and_collide(actor, dx, dy):
    # Eixo X
    actor.x += dx
    if collides_with_walls(actor):
        actor.x -= dx
    # Eixo Y
    actor.y += dy
    if collides_with_walls(actor):
        actor.y -= dy

class Hero:
    def __init__(self, x, y, speed=2):
        # Listas de imagens por estado/direção
        self.frames = {
            "idle":  ["hero_idle1", "hero_idle2", "hero_idle3", "hero_idle4"],

            "walk_down":  ["hero_walk_down1", "hero_walk_down2",
                           "hero_walk_down3", "hero_walk_down4"],
            "walk_up":    ["hero_walk_up1", "hero_walk_up2", "hero_walk_up3"],
            "walk_left":  ["hero_walk_left1", "hero_walk_left2",
                           "hero_walk_left3", "hero_walk_left4"],
            "walk_right": ["hero_walk_right1", "hero_walk_right2",
                           "hero_walk_right3", "hero_walk_right4"],
        }

        self.direction = "down"   # direção atual
        self.state = "idle"       # "idle" ou "walk"
        self.speed = speed
        self.has_key = False

        self.current_list = self.frames["idle"]
        self.frame_index = 0
        self.actor = Actor(self.current_list[self.frame_index], (x, y))

    def animate(self):
        self.frame_index = (self.frame_index + 1) % len(self.current_list)
        self.actor.image = self.current_list[self.frame_index]

    def draw(self):
        self.actor.draw()

    def update(self):
        dx = dy = 0
        moving = False

        if keyboard.right or keyboard.d:
            dx += self.speed
            self.direction = "right"
            moving = True
        if keyboard.left or keyboard.a:
            dx -= self.speed
            self.direction = "left"
            moving = True
        if keyboard.down or keyboard.s:
            dy += self.speed
            self.direction = "down"
            moving = True
        if keyboard.up or keyboard.w:
            dy -= self.speed
            self.direction = "up"
            moving = True

        move_and_collide(self.actor, dx, dy)

        self.state = "walk" if moving else "idle"
        key = f"{self.state}_{self.direction}"
        new_list = self.frames.get(key, self.frames["idle"])
        if new_list != self.current_list:
            self.current_list = new_list
            self.frame_index = 0
            self.actor.image = self.current_list[self.frame_index]

hero = Hero(150, 50, speed=2)
schedule_interval(hero.animate, 0.15)

class Enemy:
    def __init__(self, x, y, speed=1.0, target=None):
        self.animations = {
            "idle": ["enemy_idle1", "enemy_idle2", "enemy_idle3", "enemy_idle4"],
            "walk": ["enemy_walk1", "enemy_walk2", "enemy_walk3"],
            "dead": ["enemy_dead1", "enemy_dead2"]
        }

        self.state = "idle"
        self.frame_index = 0
        self.actor = Actor(self.animations[self.state][self.frame_index], (x, y))
        self.speed = speed
        self.target = target
        self.looping = True
        self.dead_done = False

    def set_state(self, state):
        if self.state != state:
            self.state = state
            self.frame_index = 0
            self.looping = (state != "dead")
            self.actor.image = self.animations[state][0]

    def animate(self):
        frames = self.animations[self.state]
        if self.looping:
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.actor.image = frames[self.frame_index]
        else:
            if self.frame_index < len(frames) - 1:
                self.frame_index += 1
                self.actor.image = frames[self.frame_index]
            else:
                self.dead_done = True
    
    def draw(self):
        self.actor.draw()

    def update(self):
        if not self.target or self.state == "dead":
            return

        tx, ty = self.target.actor.x, self.target.actor.y
        ax, ay = self.actor.x, self.actor.y
        dx, dy = tx - ax, ty - ay
        dist = (dx*dx + dy*dy) ** 0.5

        stop_radius = 6.0
        if dist < stop_radius:
            self.set_state("idle")
            return

        if dist > 0:
            ux = self.speed * dx / dist
            uy = self.speed * dy / dist

            # tenta mover; colisão usa hitbox com padding (def collides_with_walls foi ajustada)
            oldx, oldy = self.actor.x, self.actor.y
            move_and_collide(self.actor, ux, uy)
            moved = (self.actor.x != oldx) or (self.actor.y != oldy)

            if not moved:
                # fallback para “escorregar” em quinas
                if abs(dx) > abs(dy):
                    oldx, oldy = self.actor.x, self.actor.y
                    move_and_collide(self.actor, math.copysign(self.speed, dx), 0)
                    if (self.actor.x == oldx) and (self.actor.y == oldy):
                        move_and_collide(self.actor, 0, math.copysign(self.speed, dy))
                else:
                    oldx, oldy = self.actor.x, self.actor.y
                    move_and_collide(self.actor, 0, math.copysign(self.speed, dy))
                    if (self.actor.x == oldx) and (self.actor.y == oldy):
                        move_and_collide(self.actor, math.copysign(self.speed, dx), 0)

            self.set_state("walk")
            try:
                if not sounds.enemy1_walk.is_playing():
                    sounds.enemy1_walk.play()
            except:
                pass
        else:
            self.set_state("idle")

enemy = Enemy(400, 300, speed=1.2, target=hero)
schedule_interval(enemy.animate, 0.12)

def play_enemy1_walk_sound():
    if game_state == "game" and enemy.state == "walk":
        try:
            sounds.enemy1_walk.play()
        except:
            pass

schedule_interval(play_enemy1_walk_sound, 1.1)  # toca a cada 1.1 segundo

class Enemy2Flying:
    def __init__(self, x, y, speed=1.0, target=None):
        self.top = Actor("enemy2_flying1", (x, y))     # topo da nave
        self.bottom = Actor("enemy2_flying2", (x, y+10))  # base da nave
        self.speed = speed
        self.target = target
        self.base_offset = 10
        self.amplitude = 3
        self.bob_speed = 3.0
        self.t = 0.0
        self.sound_played = False

    def sync_bottom(self):
        # flutuação da base em relação ao topo
        offset = self.base_offset + math.sin(self.t * self.bob_speed) * self.amplitude
        self.bottom.pos = (self.top.x, self.top.y + offset)

    def update(self):
        self.t += 0.016  # aprox. ~60 FPS
        if not self.target:
            self.sync_bottom()
            return

        # mover o topo em direção ao alvo; a base segue com flutuação
        tx, ty = self.target.actor.x, self.target.actor.y
        ax, ay = self.top.x, self.top.y
        dx, dy = tx - ax, ty - ay
        dist = (dx*dx + dy*dy) ** 0.5
        if dist > 0:
            ux = self.speed * dx / dist
            uy = self.speed * dy / dist
            # mover o topo com colisão em paredes
            move_and_collide(self.top, ux, uy)

            if not self.sound_played:
                try:
                    sounds.enemy2_flying.play()
                    self.sound_played = True
                except:
                    pass
            try:
                if not sounds.enemy2_flying.is_playing():
                    sounds.enemy2_flying.play()
            except:
                pass
        self.sync_bottom()

    def draw(self):
        # desenhar base e topo (ajuste a ordem se preferir o topo por cima)
        self.bottom.draw()
        self.top.draw()

enemy2 = Enemy2Flying(700, 120, speed=1.6, target=hero)

class Barn:
    def __init__(self, x, y):
        self.frames = ["barn1", "barn2", "barn3"]  # nomes das imagens do barn
        self.frame_index = 0
        self.actor = Actor(self.frames[self.frame_index], (x, y))

    def animate(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.actor.image = self.frames[self.frame_index]

    def draw(self):
        self.actor.draw()
        
barn = Barn(WIDTH -125, HEIGHT -200) # posição do celeiro
barn.actor.anchor = ('center', 'center')  # centraliza o celeiro
schedule_interval(barn.animate, 0.2)
barn_entry_rect = Rect((barn.actor.x - 32, barn.actor.y + 40), (64, 32))

class AnimatedKey:
    def __init__(self, images, pos):
        self.images = images  # lista de nomes: ["key1", "key2", "key3"]
        self.actor = Actor(self.images[0], pos)
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 0.2  # ajuste para velocidade de troca

        self.active = True

    def update(self):
        if not self.active:
            return

        self.frame_timer += self.frame_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.images)
            self.actor.image = self.images[self.frame_index]

    def draw(self):
        if self.active:
            self.actor.draw()

    def spawn(self, avoid=(), walls=None, padding=16, tries=200, min_dist=24):
        for _ in range(tries):
            self.actor.pos = (randint(48, WIDTH - 48), randint(48, HEIGHT - 48))
            if walls and any(
                self.actor.colliderect(w.actor if hasattr(w, "actor") else w)
             for w in walls
            ):
                continue
            if avoid and any(
                self.actor.distance_to(getattr(o, "actor", o)) < min_dist
                for o in avoid
                ):
                continue
            return True
        return False

    def check_collect(self, player):
        if self.active and self.actor.distance_to(player.actor) <= 14:
            self.active = False
            player.has_key = True

            try:
                sounds.hero_sound.play()
            except:
                pass

key = AnimatedKey([
    "key1", "key2", "key3", "key4", "key5", "key6",
    "key7", "key8", "key9", "key10", "key11", "key12",
    "key13", "key14", "key15", "key16", "key17", "key18",
    "key19", "key20", "key21", "key22", "key23", "key24"
], (0, 0))
# spawn será feito no reset_game()

def draw():  # função para desenhar na tela as coisas, screen clear limpa a tela
    screen.clear()
    

    if game_state == "menu":
        background_menu.draw()
        screen.draw.text(
            "Cow vs Aliens",
            center = (WIDTH // 2, 90), #centraliza na largura
            fontsize = 60,
            color = "green",
            shadow=(1, 1),
            scolor="black" #cor da sombra
        )
        button_start.draw()
        button_exit.draw()
        if music_on:
            button_music_on.draw()
        else:
            button_music_off.draw()

    elif game_state == "game":
        background_game.draw()
        barn.draw()
        hero.draw()
        enemy.draw()
        key.draw()  # desenha a chave se estiver ativa
        enemy2.draw()
        
    elif game_state == "lose":
        background_menu.draw()
        screen.draw.text(
            "GAME OVER!",
            center=(WIDTH // 2, HEIGHT // 2 - 10),
            fontsize=48,
            color="white",
            shadow=(2,2),
            scolor="black"
    )
        screen.draw.text(
            "The cow has been abducted. \n Press ESC to return to the menu.",
            center=(WIDTH // 2, HEIGHT // 2 + 40),
            fontsize=28,
            color="yellow"
    )
    elif game_state == "win":
        background_menu.draw()
        screen.draw.text(
            "YOU WIN!",
            center=(WIDTH // 2, HEIGHT // 2 - 10),
            fontsize=48,
            color="white",
            shadow=(2,2),
            scolor="black"
)
        screen.draw.text(
            "The cow has reached the barn safely. \n Press ESC to return to the menu.",
            center=(WIDTH // 2, HEIGHT // 2 + 40),
            fontsize=28,
            color="yellow"
        )

def update():
    global game_state
    if game_state == "game":
        hero.update() # atualiza a vaquinha
        enemy.update()
        enemy2.update()
        key.update()
        key.check_collect(hero)  # verifica se a chave foi coletada

        #captura: o que acontece se o alien pegar a vaquinha
        if enemy.actor.distance_to(hero.actor) <= 14:
            game_state = "lose"
            try:
                music.play('music_menu')
            except:
                pass

                # zona de vitória (porta do celeiro)
                # checagem por distância
        dx = hero.actor.x - barn.actor.x
        dy = hero.actor.y - barn.actor.y
        dist = (dx * dx + dy * dy) ** 0.5

        if hero.has_key and hero.actor.colliderect (barn_entry_rect):
            print("WIN!") 
            game_state = "win"
            try:
                music.play('music_win')
            except:
                pass

        if (enemy2.top.distance_to(hero.actor) <= 14 or
            enemy2.bottom.distance_to(hero.actor) <= 14):
            # se a vaquinha colidir com a parte de cima ou de baixo da nave
            game_state = "lose"
            try:
                music.play('music_menu')  # se tiver um efeito sonoro
            except:
                pass

def on_key_down(key):
    global game_state
    if key == keys.ESCAPE and game_state in ("lose", "win"):
        game_state = "menu"
        try:
            if music_on:
                music.play('music_menu')
        except:
            pass

def on_mouse_down(pos): # função para clique da tela, o "pos" é a posição onde cliquei
    global game_state, music_on #chama variaveis, global ajuda a mudar só aqui

    if game_state == "menu":
        if button_start.collidepoint(pos):
            reset_game() # reseta o jogo
            game_state = "game" # muda o estado do jogo para game
            try:
                music.stop()
                music.set_volume(0.6)  # ajusta o volume da música
                music.play('music_game')  # toca música do jogo
            except:
                pass
            game_state = "game"  # muda o estado do jogo para game

        elif button_exit.collidepoint(pos):
            exit()  # fecha o jogo

        elif music_on and button_music_on.collidepoint(pos):
            music.stop()
            music_on = False

        elif not music_on and button_music_off.collidepoint(pos):
            music.play('music_menu')
            music_on = True

def reset_game():
    # reset do herói
    hero.actor.pos = (150, 50)
    hero.direction = "down"
    hero.state = "idle"
    hero.has_key = False
    hero.frame_index = 0
    hero.current_list = hero.frames["idle"]
    hero.actor.image = hero.current_list[hero.frame_index]

    # reset do inimigo terrestre
    enemy.actor.pos = (400, 300)
    enemy.set_state("idle")

    # reset do inimigo voador
    enemy2.top.pos = (700, 120)
    enemy2.t = 0.0
    enemy2.sync_bottom()

    # reset da chave (ativa + respawn)
    key.active = True
    key.frame_index = 0
    key.frame_timer = 0
    key.actor.image = key.images[0]
    # respawn evitando colisão com cow, inimigos e celeiro
    key.spawn(avoid=[hero, enemy, enemy2.top, barn], walls=walls)
pgzrun.go()  # rodar o game