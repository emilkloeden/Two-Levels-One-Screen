import pygame
import sys

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
TILE_SIZE = 64

FPS = 60

LEVEL_ONE_MAP = [
    ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ','p',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','e','x',],
    ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',],
]

LEVEL_TWO_MAP = [
    ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ','p',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x','x',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','e','x',],
    ['x',' ',' ',' ',' ',' ',' ','x','x',' ',' ','x',' ',' ',' ',' ',' ','x','x','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',],
    ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',],
]

class AbstractImageSprite(pygame.sprite.Sprite):
    def __init__(self, position, image, groups) -> None:
        super().__init__(groups)

        self.position = pygame.math.Vector2(position)
        self.image = image
        self.rect = self.image.get_rect(topleft=position)


class AbstractTile(AbstractImageSprite):
    def __init__(self, position, image_path, groups) -> None:
        interstitial_image = pygame.image.load(image_path)
        image = pygame.transform.scale(interstitial_image, (TILE_SIZE, TILE_SIZE))
        super().__init__(position, image, groups)
        

class Tile(AbstractTile):
    def __init__(self, position, groups) -> None:
        super().__init__(position, 'assets/images/tile_0047.png', groups)

class Exit(AbstractTile):
    def __init__(self, position, groups) -> None:
        super().__init__(position, 'assets/images/tile_0132.png', groups)


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups) -> None:
        super().__init__(groups)

        interstitial_image = pygame.image.load('assets/images/character_0000.png')
        self.image = pygame.transform.scale(interstitial_image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=position)
        
        # Movement
        self.direction = pygame.math.Vector2((0,0))
        self.speed = 3
        self.gravity = 0.8
        self.jump_power = -16

        self.num_jumps = 2

    def handle_input(self):
        for event in pygame.event.get():
            if is_quit_requested(event):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: 
                if event.key in [pygame.K_UP, pygame.K_w, pygame.K_SPACE]:
                    self.jump()


        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.direction.x = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.direction.x = self.speed
        else:
            self.direction.x = 0



    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if self.num_jumps > 0:
            self.direction.y = self.jump_power
            self.num_jumps -= 1

    def update(self):
        self.handle_input()

class Level:
    def __init__(self, level_map, level_bg_path=None):
        self.is_current_level = True
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.get_surface()
        if level_bg_path:
            self.bg_image = pygame.image.load(level_bg_path)
        else:
            self.bg_image = None
        self.level_map = level_map
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def run(self):
        while self.is_current_level:
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)


    def handle_horizontal_movement_and_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:  # moving left
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:  # moving right
                    player.rect.right = sprite.rect.left
                    if isinstance(sprite, Exit):
                        self.is_current_level = False


    def handle_vertical_movement_and_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:  # moving down
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0  # cancel out apply gravity
                    player.num_jumps = 2 # reset can_jump_logic
                elif player.direction.y < 0:  # moving up
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0  # cancel out jumping up through a block


    def update(self):
        self.player.update()
        self.handle_horizontal_movement_and_collision()
        self.handle_vertical_movement_and_collision()

    def draw(self):
        self.display_surface.fill('black')
        if self.bg_image:
            self.display_surface.blit(self.bg_image, (0,0))
        self.player.draw(self.display_surface)
        self.tiles.draw(self.display_surface)

    def create_map(self):
        for row_index, row in enumerate(self.level_map):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if col == 'x':
                    Tile((x, y), [self.tiles, self.obstacle_sprites])
                if col == 'e':
                    Exit((x, y), [self.tiles, self.obstacle_sprites])
                if col == 'p':
                    Player((x,y), [self.player])




class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Two Levels, One Screen")
        self.levels = [
            Level(LEVEL_ONE_MAP),
            Level(LEVEL_TWO_MAP),
        ]
        
    def run(self):
        for level in self.levels:
            level.run()

def is_quit_requested(event):
    if event.type == pygame.QUIT:
        return True
    return event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE


if __name__ == "__main__":
    game = Game()
    game.run()