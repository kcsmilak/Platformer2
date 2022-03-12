import pgzrun
import pygame
import random



import io
try:
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen

MAP_URL="https://docs.google.com/spreadsheets/d/1jbsapypHN5FX6k8K7Zs271bY8QSzSMiLkHFi2667nsU/gviz/tq?tqx=out:csv&sheet=live"



TITLE = "Hello World"

#WIDTH = 600
#HEIGHT = 450

WIDTH = 800
HEIGHT = 600


MAX_PLATFORMS = 3
MAX_BALLS = 0

GRAVITY = 1
GRAVITY_MAX = 10
HEIGHT_MIN = -200
JUMP_BOOST = 11

BACKGROUND_ENTITY = 0
WALL_ENTITY = 1
PLAYER_ENTITY = -1
PLATFORM_ENTITY = -7
BALL_ENTITY = -8
BULLET_ENTITY = -9

SHOOT_COOLDOWN = 20
TILE_SIZE = 16

MAP1 = [[1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,1],
        [1,2,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,2,2,1],
        [1,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,2,2,0,0,0,0,0,0,1],
        [1,5,2,3,3,0,2,0,0,0,0,1],
        [1,2,1,1,1,2,1,2,2,2,2,1]]






# edge behaviors: STOP, STICK, BOUNCE, DIE, DESTROY


DIRECTION_RIGHT = 1
DIRECTION_LEFT = 2

MOVEMENT_RIGHT = 1
MOVEMENT_LEFT = 2

MOVEMENT_JUMPING = 3
MOVEMENT_IDLE = 0

class Entity(Actor):
    def __init__(self, image):
        Actor.__init__(self, image)
        self.xspeed = 0
        self.yspeed = 0
        self.max_right = WIDTH
        self.min_left = 0
        self.min_top = 0
        self.max_bottom = HEIGHT
        self.airborn = False
        self.hit = False
        self.id = random.randint(1,1024)
        self.type = -1
        self.solid = True
        self.shooting = False
        self.edgeBounce = True
        self.shootCooldown = 0
        self.movement = MOVEMENT_IDLE
        self.direction = DIRECTION_RIGHT


        
    def move(self, player):
        entity = self

        # try to move in x direction
        entity.x += entity.xspeed

        # if hit edge, bounce or die
        if (self.right > self.max_right):
            self.xspeed *= -1
            self.right = self.max_right
        
        elif (self.left < self.min_left):
            self.xspeed *= -1
            self.left = self.min_left
        
        # if hit player, do something
        if entity.colliderect(player):
            # if platform, push the player
            if (PLATFORM_ENTITY == entity.type):
                player.x += entity.xspeed
            # if ball, hurt the player
            elif (BALL_ENTITY == entity.type):
                player.hit = True
                entity.hit = True
    
        entity.y += entity.yspeed

        # if hit edge, bounce
        if (entity.bottom > entity.max_bottom):
            entity.yspeed *= -1
            entity.bottom = entity.max_bottom           
            
        elif (entity.top < entity.min_top):
            entity.yspeed *= -1
            entity.top = entity.min_top

    def draw2(self, screen):
        screen.draw.rect(Rect((self.topleft, (self.width, self.height))), (255,255,255)) 
        self.draw()
        
    

        
class Player(Entity):
    def __init__(self):
        Entity.__init__(self, "red")
        self.type = PLAYER_ENTITY
        self.min_top = -200        
        self.x, self.y = 100, 100
        self.frame = 0
        self.run = pygame.image.load("images/run.png")
        self.idle = pygame.image.load("images/idle.png")
        self.jump = pygame.image.load("images/jump.png")
        
    def updateImage(self):
        cropped = pygame.Surface((32, 32), pygame.SRCALPHA, 32)

        img = 0
        frame = 0
        if (MOVEMENT_IDLE == self.movement):
            img = self.idle
            frame = (self.frame // 1) % 11 
        elif (MOVEMENT_JUMPING == self.movement):
            img = self.jump
            frame = 0
        else:
            img = self.run
            frame = (self.frame // 1) % 12


        
        cropped.blit(img, (0, 0), (32 * (frame), 0, 32, 32))

        if (DIRECTION_LEFT == self.direction):
            cropped = pygame.transform.flip(cropped, True, False)
        
        self.frame += 1
        self._surf = cropped
        
        #self._surf = pygame.transform.scale(self._surf,( 48, 48))
        self._update_pos()        
        

        
    def move(self, obstacles):
        entity = self

        # try to move in x direction
        entity.x += entity.xspeed

        # if hit edge, bounce
        if (entity.right > entity.max_right):
            entity.xspeed *= -1
            entity.right = entity.max_right
        
        elif (entity.left < entity.min_left):
            entity.xspeed *= -1
            entity.left = entity.min_left                
        else:
            for obstacle in obstacles:
                if entity.colliderect(obstacle):
                    if (obstacle.solid):
                        entity.x -= entity.xspeed                        
                        entity.xspeed = 0

        
        entity.y += entity.yspeed

        # if hit edge, bounce
        if (entity.bottom > entity.max_bottom):
            entity.yspeed *= -1
            entity.bottom = entity.max_bottom

            entity.yspeed = 0
            entity.airborn = False               
            
        elif (entity.top < entity.min_top):
            entity.yspeed *= -1
            entity.top = entity.min_top

        else:
            for obstacle in obstacles:
                if entity.colliderect(obstacle):
                    if (obstacle.solid):
                        entity.y -= entity.yspeed
                        if (entity.yspeed > 0):
                            entity.airborn = False
                        entity.yspeed = 0
                        entity.x += obstacle.xspeed
                        break
            if entity.yspeed > 0:
                entity.airborn = True

        self.updateImage()

        


class Platform(Entity):
    def __init__(self, i):
        Entity.__init__(self, "red")


        oh = 5
        ow = 96
        cropped = pygame.Surface((ow, oh), pygame.SRCALPHA, 32)
        img = pygame.image.load("images/tiles.png")
  
        cropped.blit(img, (0, 0), (16*17, 0, 16, oh))
        cropped.blit(img, (16, 0), (16*18, 0, 16, oh))
        cropped.blit(img, (32, 0), (16*18, 0, 16, oh))
        cropped.blit(img, (48, 0), (16*18, 0, 16, oh))
        cropped.blit(img, (64, 0), (16*18, 0, 16, oh))
        cropped.blit(img, (80, 0), (16*19, 0, 16, oh))

        self._surf = cropped
        
        #self._surf = pygame.transform.scale(self._surf,( 2*ow*(TILE_SIZE/48), 2* oh * (TILE_SIZE/48)))
        self._update_pos()








        
        self.type = PLATFORM_ENTITY
        self.pos = 100 * i + 100, i * 135 + 50
        self.xspeed = random.randint(1, 3)        
        self.max_right = WIDTH * .75
        self.min_left = WIDTH * .25


class Ball(Entity):
    def __init__(self):
        Entity.__init__(self, "red")
        self.type = BALL_ENTITY
        self.pos = random.randint(0,WIDTH - self.width), random.randint(0,HEIGHT - self.height)
        self.xspeed = random.randint(1, 3) 
        if (random.randint(0,1)): self.xspeed *= -1
        self.yspeed = random.randint(1, 3) 
        if (random.randint(0,1)): self.yspeed *= -1
        self.solid = True

class Bullet(Entity):
    def __init__(self, x, y, dx, dy):
        Entity.__init__(self, "red")
        self.angle = -90
        self.type = BULLET_ENTITY
        self.pos = x, y
        self.xspeed = dx 
        self.yspeed = dy 
        self.solid = True
        self.max_right = self.max_left = 100



class Tile(Entity):
    def __init__(self, x, y, type):
        Entity.__init__(self,"red")        
        cropped = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
        img = pygame.image.load("images/tiles.png")
        col = type % 100
        row = type // 100
        cropped.blit(img, (0, 0), (16*col, 16*row, 16, 16))
        self._surf = cropped
            
        self.type = type
        
        
        #self._surf = pygame.transform.scale(self._surf, (TILE_SIZE, TILE_SIZE))
        self._update_pos()
            
        self.left = x * TILE_SIZE
        self.top = y * TILE_SIZE         

class World():
    def __init__(self):
        self.all_entities = []
        self.player = 0
        self.reset()

    def reset(self):
        self.all_entities.clear()

        map = []
        str = io.BytesIO(urlopen(MAP_URL).read()).read().decode('UTF-8')        
        for row in str.split("\n"):
            newrow = []
            for cell in row.split(","):
                newrow.append(int(cell.strip("\"")))
            map.append(newrow)
        
        px, py = 0, 0
        
        for y in range(len(map)):
            for x in range(len(map[y])):
                tileType = map[y][x]
                if (tileType > 0):
                    tile = Tile(x, y, tileType)
                    self.all_entities.append(tile)
                elif (PLAYER_ENTITY == tileType):
                    self.player = Player()
                    self.player.left = x * TILE_SIZE
                    self.player.bottom = y * TILE_SIZE
    
        for i in range(0, MAX_PLATFORMS):
            self.all_entities.append(Platform(i))    

        for i in range(0, MAX_BALLS):
            self.all_entities.append(Ball()) 


    
    def update(self):
        player = self.player
        entities = self.all_entities
        
        self.handleInput()
        
        # move entities
        for entity in entities:          
            entity.move(player)

        # move player
        player.move(entities)

        # remove hit entities
        for entity in entities:
            if (entity.hit):
                entities.remove(entity)

        # handle hit Player
        if (player.hit):
            player.hit = False
            print("ouch!")

    def handleInput(self):
        if (keyboard.r):
            self.reset()
            return

        player = self.player


        if (keyboard.b):
            self.all_entities.append(Ball())    
        
        if (keyboard.d):
            #player.image = "alien-right"
            player.direction = DIRECTION_RIGHT
            player.movement = MOVEMENT_RIGHT
        elif (keyboard.a):
            #player.image = "alien-left"
            player.direction = DIRECTION_LEFT
            player.movement = MOVEMENT_RIGHT            
        else:
            player.movement = MOVEMENT_IDLE

        if (player.airborn):
            player.movement = MOVEMENT_JUMPING
            
        player.xspeed = 0
        dx = 5
        if (keyboard.LSHIFT):
            dx = 2
        #player.yspeed = 0
        if (keyboard.d):

            player.xspeed += dx 
        elif (keyboard.a):
            player.xspeed -= dx 
        #else:
            #player.xspeed = 0
            #pass

        if (keyboard.space) and not player.shooting:
            # shoot
            player.shooting = True
            player.shootCooldown = SHOOT_COOLDOWN
            self.all_entities.append(Bullet(player.x,player.y,2,0))
        elif player.shootCooldown > 0: # add cooldown here
            player.shootCooldown -= 1
        else:
            player.shooting = False
    
        if keyboard.w and not player.airborn:
            player.yspeed -= JUMP_BOOST
            player.airborn = True
            player.movement = MOVEMENT_JUMPING
    
        player.yspeed += GRAVITY

    def draw(self,screen):
        
        for entity in self.all_entities:
            entity.draw()

        self.player.draw()


def update():
    global world
    world.update()

def draw_grid(screen):
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * TILE_SIZE), (WIDTH, line * TILE_SIZE))
        pygame.draw.line(screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, HEIGHT))


def draw():
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    global world
    screen.clear()
    screen.fill((100,100,100)) 

    world.draw(screen)

    #draw_grid(screen)


    

world = World()
#DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
#DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pgzrun.go()
