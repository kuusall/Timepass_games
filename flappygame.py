import pygame, random, sys
pygame.init()
W,H=400,600
win=pygame.display.set_mode((W,H))
clock=pygame.time.Clock()
y,vel,pipes=H//2,0,[(300,random.randint(200,400))]
score=0
while True:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type==pygame.QUIT: sys.exit()
        if e.type==pygame.KEYDOWN: vel=-7
    vel+=0.5; y+=vel
    if y>H: y=H//2; pipes=[(300,random.randint(200,400))]; score=0
    pipes=[(x-5,h) for (x,h) in pipes if x>-50]
    if pipes[-1][0]<200: pipes.append((400,random.randint(200,400)))
    win.fill((135,206,250))
    for x,h in pipes:
        pygame.draw.rect(win,(0,255,0),(x,0,50,h-150))
        pygame.draw.rect(win,(0,255,0),(x,h,50,H-h))
        if 50<x<100 and (y<h-150 or y>h): y=H+1
    pygame.draw.rect(win,(255,0,0),(75,y,30,30))
    score+=1; pygame.display.set_caption(f"Score:{score//30}")
    pygame.display.flip()