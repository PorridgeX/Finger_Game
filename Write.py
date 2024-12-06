import pygame
import time,os

#写谱的工具
#做好谱子后连同音乐放到当前文件夹下的新建子文件夹下(需要手动)

size = [1080,720]

pygame.init()
musicfile='gamedata/Heaven.mp3' #音乐路径

class Showcommand:
    def __init__(self):
        self.imglist = []
    def update(self):
        for i in self.imglist:
            i.update()
    def add(self,key):
        if key==100 or key==102 or key==106 or key==107:
            if key==100:
                pos = centers[0]
                keystring='d'
            elif key == 102:
                pos = centers[1]
                keystring='f'
            elif key == 106:
                pos = centers[2]
                keystring='j'
            elif key == 107:
                pos = centers[3]
                keystring='k'
            # keystring = str(key)
            print(str(key))
            self.imglist.append(Imgs(list(pos)))
            commands.append([keystring,str(round(time.time()-starttime,3))])

L = []
imgfile = 'image/4/'
files = os.listdir(imgfile)
for i in files:
    L.append(pygame.image.load(imgfile+i))

class Imgs:
    def __init__(self,pos):
        self.imglist = L
        self.count = 0
        self.max = len(L)
        self.alive = True
        self.rect = self.imglist[0].get_rect()
        self.rect.center = pos
    def update(self):
        if not self.alive: return
        img = self.imglist[self.count]
        screen.blit(img,self.rect)
        self.count+=1
        if self.count>=self.max-1:
            self.alive = False

screen = pygame.display.set_mode(size)
pygame.display.set_caption('music')

pygame.mixer.music.load(musicfile)

clock = pygame.time.Clock()

fiximg = pygame.image.load('image/approachcircle.png')
fiximg1 = pygame.image.load('image/approach1.png')
fiximg2 = pygame.image.load('image/approach2.png')
rect = pygame.Rect(0,0,250,253)

# centers = [(j*250+150,(2-i)*250+150) for i in range(3) for j in range(3)]
centers = [[40+125*1,360],
        [40+125*3,360],
        [40+125*5,360],
        [40+125*7,360]
]
# centers.pop(0)

commands = []
show = Showcommand()

pygame.mixer.music.play(1,0)
starttime = time.time()

f = pygame.font.Font("font/simsun.ttc",50)
# render(text, antialias, color, background=None) -> Surface


while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('data3.cir','w',encoding='utf8') as f: #谱面数据储存路径
                for i in commands:
                    f.write(i[0]+' '+i[1]+'\n')
            exit()
        elif event.type == pygame.KEYDOWN:
            show.add(event.key)
            print(event.key)
    for i in range(4):
        rect.center=centers[i]
        screen.blit(fiximg,rect)
    for i in [0,3]:
        rect.center = (centers[i][0]+63,centers[i][1]+63)
        screen.blit(fiximg1,rect)
        if i == 0 :
            text = f.render("D", True, (255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (centers[i][0], centers[i][1]+133)
            screen.blit(text, textRect)
        if i == 3 :
            text = f.render("K", True, (255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (centers[i][0], centers[i][1]+133)
            screen.blit(text, textRect)
    for i in [1,2]:
        rect.center = (centers[i][0]+63,centers[i][1]+63)
        screen.blit(fiximg2,rect)
        if i == 1 :
            text = f.render("F", True, (255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (centers[i][0], centers[i][1]+133)
            screen.blit(text, textRect)
        if i == 2 :
            text = f.render("J", True, (255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (centers[i][0], centers[i][1]+133)
            screen.blit(text, textRect)
    show.update()
    pygame.display.flip()
