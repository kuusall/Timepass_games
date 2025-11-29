import pygame
import random
import sys

WIDTH, HEIGHT = 480, 640
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteor Dash")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
player_size = 40
player_x = WIDTH//2 - player_size//2
player_y = HEIGHT - player_size - 10
player_speed = 6
meteor_size = 30
meteor_speed_min =2
meteor_speed_max = 6
meteor_spawn_delay = 800
meteors = []
score = 0
game_over = False
last_spawn_time = pygame.time.get_ticks()
def spawn_meteor():
    x= random.randint(0, WIDTH -  meteor_size)
    speed = random.randint(meteor_speed_min, meteor_speed_max)
    meteors.append({"x": x, "y": -meteor_size, "speed": speed})
def draw_player(x,y):
    pygame.draw.rect(screen, (50,150,255), (x,y, player_size, player_size))
    pygame.draw.polygon(screen, (255,100,0), [(x+10, y+player_size), (x+player_size - 10, y+player_size),(x+player_size//2, y+player_size+10)])
def draw_meteor(m):
    pygame.draw.circle(screen, (160,80,60), (int(m["x"]+meteor_size/2), int(m["y"]+meteor_size/2)), meteor_size//2)
    pygame.draw.circle(screen, (120,60,40), (int(m["x"]+meteor_size/2)+4, int(m["y"]+meteor_size/2)-4), meteor_size//4)
def rects_collide(rx,ry,rw,rh,cx,cy,cr):
    nearest_x = max(rx, min(cx, rx+rw))
    nearest_y = max(ry, min(cy, ry+rh))
    dx = cx - nearest_x; dy = cy - nearest_y
    return (dx*dx +dy*dy) <= (cr*cr)
def reset_game():
    global meteors, score, player_x, game_over, last_spawn_time, metoer_spawn_delay
    meteors = []; score = 0
    player_x = WIDTH//2 - player_size //2
    game_over = False
    meteor_spawn_delay = 800
    last_spawn_time = pygame.time.get_ticks()
while True:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()
    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] or keys[pygame.K_a] :
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
            player_x += player_speed
    player_x = max(0, min(WIDTH- player_size, player_x))
    if not game_over:
        now = pygame.time.get_ticks()
        if now - last_spawn_time > meteor_spawn_delay:
            spawn_meteor(); last_spawn_time = now
            if meteor_spawn_delay > 300: meteor_spawn_delay -= 10
    for m in meteors[:]:
        m["y"] += m["speed"]
        if m["y"] > HEIGHT:
            meteors.remove(m); score += 1
    for m in meteors[:]:
        m["y"] += m ["speed"]
        if m["y"] > HEIGHT:
            meteors.remove(m); score += 1
    for m in meteors:
        cx = m["x"] + meteor_size/2; cy = m["y"] + meteor_size/2
        if rects_collide(player_x, player_y, player_size, player_size, cx, cy, meteor_size/2):
            game_over = True
    screen.fill((10,10,30))

    #STARS
    for i in range(25):
        sx = (i*47 + (pygame.time.get_ticks()//50)%WIDTH) % WIDTH
        sy = (i*31 + (pygame.time.get_ticks()//33)%HEIGHT) % HEIGHT
        pygame.draw.circle(screen, (200,200,220), (sx,sy), 1)
    draw_player(player_x,player_y)
    for m in meteors:
        draw_meteor(m)
    score_surf = font.render(f"Score: {score}", True, (240,240,240))
    screen.blit(score_surf, (10,10))
    if game_over:
        over_surf = font.render("GAME OVER - Press R to restart", True, (255,200,200))
        screen.blit(over_surf, (WIDTH//2 - over_surf.get_width()//2, HEIGHT//2 - 20))
    pygame.display.flip()