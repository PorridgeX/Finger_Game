# from zipfile import compressor_names


import pygame
import time,os,random
import math
from math import pow as power
from pynput.keyboard import Key, Listener
import threading
from pygame.mixer_music import queue
import Gesture_recognition

#from musicplaycircle import pypresskeys, combo, starttime
from multiprocessing import Queue

FILE = {
    'bgfile':'image/bg/',#背景图文件夹路径
    'playfile':'gamedata',#这个就是当前文件夹下的子文件夹名称,里面存放音乐(支持.wav,.mp3),和谱面(支持.cir)文件
}


time.sleep(2)

size = [1080,720]

fixspeedpartten = False
fixspeed = 0.4

AUTO = False

simple = False

verysimple = True
rever = False#方向反向

Quick = True

bg = True
bgcenter = True
bgimgfiles = FILE['bgfile']+random.choice(os.listdir(FILE['bgfile']))
bgimg = pygame.image.load(bgimgfiles)
if bgcenter:
    bgrect = bgimg.get_rect()
    bgrect.center = (540,360)
else:
    bgrect = (0,0)#决定背景图片中心为画面中心还是画面左上角

if verysimple:fixspeedpartten=True;fixspeed=2
musicfile = None
txtfile=None
files = os.listdir(FILE['playfile'])
for i in files:
    part=os.path.splitext(i)
    if len(part)!=2:continue
    if part[1] in ['.wav','.mp3']:musicfile = FILE['playfile']+'/'+i
    if part[1] in ['.cir']:txtfile = FILE['playfile']+'/'+i

if not musicfile or not txtfile:
    raise ValueError('文件路径错误')

missedbefore = 2000
missedafter = 1600
codes = ['bad','bad+','good','great','great+'][::-1]

circlefilerange = [1,2,3] if not Quick else [5,6,7]

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('music')

pygame.mixer.music.load(musicfile)

clock = pygame.time.Clock()

def spesort(item):
    return item[1]
def loadrhythm():
    showlist = []
    with open(txtfile,'r',encoding='utf8') as f:
        for i in f.readlines(): #谱面数据
            i = i.strip().split(' ')
            speed = random.uniform(1.2,2) if not fixspeedpartten else fixspeed
            i[1] = float(i[1])-speed
            if i[1]<0:
                speed = speed-i[1]
                i[1]=0
            i.append(speed)
            showlist.append(i)
    showlist.sort(key=spesort)
    return showlist

rhythmcircle = []
for i in circlefilerange:
    rhythmcircle.append([])
    imgfile = 'image/%d/'%i
    files = os.listdir(imgfile)[10:]
    for i in files:
        rhythmcircle[-1].append(pygame.image.load(imgfile+i))

showlist = loadrhythm()

class Ways:
    def __init__(self):
        self.imglist = []
    def update(self):
        self.check()
        for index,i in enumerate(self.imglist):
            self.imglist[index]=i.update(time.time()) if type(i)==Imgs else i.update()
    def add(self,pos,center,speed,direct):
        i=Imgs(pos,center,speed,direct)
        self.imglist.append(i)
        pypresskeys[direct].append(i)
    def press(self,key):
        if key not in pykeys.keys():return
        if pypresskeys[pykeys[key]]:
            d = pypresskeys[pykeys[key]][0].distance()
            missed = missedafter if pypresskeys[pykeys[key]][0].outrange() else missedbefore
            missed+=2000//pypresskeys[pykeys[key]][0].speed
            if d < missed and not pypresskeys[pykeys[key]][0].pressed:

                showscore.add(codes[int(d // (missed / 1))])
                pypresskeys[pykeys[key]][0].pressed = True
                combo.add()
                combo.center = pypresskeys[pykeys[key]][0].center
    def check(self):
        for i in self.imglist[::-1]:
            if not i.alive:
                self.imglist.remove(i)
                if type(i)==Imgs and i in pypresskeys[i.direct]:
                    pypresskeys[i.direct].remove(i)



numberlist = []
for i in list('0123456789'):
    numberlist.append(pygame.image.load('image/num/default-%s.png'%i))

class Showcommand:
    def __init__(self):
        self.imglist = []
    def update(self):
        for i in self.imglist:
            i.update()
    def add(self,pos):
        self.imglist.append(Imgs2(pos))
showcommand = Showcommand()

class Showscore:
    def __init__(self):
        file = 'image/score/'
        self.score = {'miss':pygame.image.load(file+'0.png'),
                      'bad':pygame.image.load(file+'1.png'),
                      'bad+':pygame.image.load(file+'2.png'),
                      'good':pygame.image.load(file+'3.png'),
                      'great':pygame.image.load(file+'4.png'),
                      'great+':pygame.image.load(file+'5.png')

        }
        self.imglist = []
        self.max = 12
        self.rect = pygame.Rect(0,621,181,99)
    def add(self,code):
        self.imglist.append([self.score[code],0])
    def update(self):
        if self.imglist:
            screen.blit(self.imglist[0][0],self.rect)
            self.imglist[0][1] += 1
            if self.imglist[0][1]>=self.max:
                self.imglist.pop(0)
showscore = Showscore()

def xor(a,b):
    return not(a and b or not a and not b)



class Combo3:
    def __init__(self,center,w,h):
        self.centers = [(center[0]-2*w,center[1]),(center[0]-w,center[1]),center]
        self.updating = [False,False,False]
        self.speed = 5
        self.center =center
        self.sufs = [pygame.Surface((w,h)).convert_alpha() for i in range(3)]
        self.combo = 0
        self.updatepool = [[],[],[]]
        self.string = '--0'
        self.weight = w
        self.height = h
        self.rect = pygame.Rect(0,0,w,h)
    def _to_string(self):
        return '-'*(3-len(str(self.combo)))+str(self.combo)
    def add(self):
        self.combo+=1
        string = self._to_string()
        old = '-' if self.string[2]=='-' else int(self.string[2])
        self.updatepool[2].append([int(string[2]),old,self.height])
        if self.combo%10 == 0 and self.combo>8:
            old = '-' if self.string[1]=='-' else int(self.string[1])
            self.updatepool[1].append([string[1],old,self.height])
        if self.combo%100 == 0 and self.combo>88:
            old = '-' if self.string[0]=='-' else int(self.string[0])
            self.updatepool[0].append([string[0],old,self.height])
        self.string = string
    def miss(self):
        self.combo=0
        self.string='--0'
    def update(self):
        for i in range(3):
            self.sufs[i].fill((0,0,0,0))
        if self.combo==0:return
        for i,j in enumerate(self.updatepool):
            if not j:
                self.updating[i]=False
                if self.string[i]!='-':
                    self.sufs[i].blit(numberlist[int(self.string[i])],(0,0))
                continue
            elif j and not self.updating[i]: self.updating[i] = True
            else:
                j[0][2]-=self.speed
                j[0][2] = j[0][2] if j[0][2]>=0 else 0
                new,old=j[0][:2]
                self.sufs[i].blit(numberlist[int(new)],(0,j[0][2]))
                if old!='-':
                    self.sufs[i].blit(numberlist[int(old)],(0,j[0][2]-self.height))
                if j[0][2]<=0:
                    self.updating[i]=False
                    self.updatepool[i].pop(0)
        for i in range(3):
            self.rect.center = self.centers[i]
            screen.blit(self.sufs[i],self.rect)

combo = Combo3((1055,27),49,54)




class Imgs:
    def __init__(self,pos,center,speed,direct):
        self.starttime =time.time()
        self.imglist = random.choice(rhythmcircle)
        self.count = 0
        self.speed = speed
        self.center = center
        self.direct = direct
        self.max = len(self.imglist)
        self.alive = True
        self.rect = self.imglist[0].get_rect()
        self.minx = True if pos[0]<=self.center[0] else False
        self.miny = True if pos[1]<=self.center[1] else False
        self.pressed = False
        self.blitpos = pos
        self.pos = pos
        self.finish = pos.copy()
    def distance(self):
        return power(self.finish[0]-self.center[0],2)+power(self.finish[1]-self.center[1],2)
    def outrange(self):
        xor(self.finish[0]<self.center[0],self.minx) and xor(self.finish[1]<self.center[1],self.miny)
    def update(self,t):
        if not self.alive:return
        img = self.imglist[self.count]
        if not self.pressed:
            posx = abs(self.center[0]-self.pos[0])*(t-self.starttime)/self.speed
            posy = abs(self.center[1]-self.pos[1])*(t-self.starttime)/self.speed
            if self.minx:
                x=self.pos[0]+posx
            else :
                x=self.pos[0]-posx
            posy = posy if self.miny else -posy
            y=self.blitpos[1]+posy
            self.finish = [x,y]
        else:
            x,y = self.finish
        d = power(x-self.center[0],2)+power(y-self.center[1],2)
        missed = missedafter if self.outrange() else missedbefore
        missed+=1000//self.speed
        if d>=1000 and not self.pressed and xor(x<self.center[0],self.minx) and xor(y<self.center[1],self.miny):
            showscore.add('miss')
            showcommand.add(list(self.center))
            combo.miss()
            self.alive=False
            return self
        if self.pressed:
            self.count+=1
        if self.count>=self.max-1:
            self.alive = False
        self.rect.center = (round(x),round(y))
        screen.blit(img,self.rect)
        return self

missdecircle = []
imgfile = 'image/4/'
files = os.listdir(imgfile)
for i in files:
    missdecircle.append(pygame.image.load(imgfile+i))

centerdict = {'d':[40+125*1,360],
        'f':[40+125*3,360],
        'j':[40+125*5,360],
        'k':[40+125*7,360]
              }

centerlist = [[40+125*1,360],
        [40+125*3,360],
        [40+125*5,360],
        [40+125*7,360]
]

class Imgs2:
    def __init__(self,pos):
        self.imglist = missdecircle
        self.count = 0
        self.max = len(missdecircle)
        self.alive = True
        self.rect = self.imglist[0].get_rect()
        self.rect.center = pos
    def update(self):
        if not self.alive: return self
        img = self.imglist[self.count]
        screen.blit(img,self.rect)
        self.count+=1
        if self.count>=self.max-1:
            self.alive = False
        return self

pykeys = {100:'d',102:'f',106:'j',107:'k'}
pyvalues = {'d':100,'f':102,'j':106,'k':107}
pypresskeys = {'d':[],'f':[],'j':[],'k':[]}

def addshows():
    if showlist and time.time()-starttime>=showlist[0][1]:
        item = showlist.pop(0)
        choice1 = random.randint(0,1)
        choice2 = random.randint(0,1)
        if not (simple or verysimple):
            if choice1 ==0:
                posX = random.randint(10,1070)
                posY = -127 if choice2==0 else size[1]+127
                pos = (posX,posY)
            else:
                posY = random.randint(10,460)
                if posY>235:posY+=255
                posX = -127 if choice2 == 0 else size[0]+127
                pos = (posX, posY)
        elif simple:
            posY = -127 if choice2 == 0 else size[1] + 127
            posX = centerdict[item[0]][0]
            pos = (posX,posY)
        elif verysimple:
            posY = -127 if not rever else size[1]+127
            pos = (centerdict[item[0]][0],posY)
        center = centerdict[item[0]]
        way.add(list(pos),center,item[2],item[0])

def autopressed():
    for _,j in enumerate(pykeys.values()):
        if not pypresskeys[j]:continue
        d = pypresskeys[j][0].distance()
        if d<=200:
            way.press(pyvalues[j])
def on_press(key):
    try:
        # 获取普通按键的字符值
        way.press(ord(key.char))

    except AttributeError:
        print(f'特殊键 {key} 被按下，键值为：{key}')




way = Ways()
fiximg = pygame.image.load('image/approachcircle.png')
fiximg1 = pygame.image.load('image/approach1.png')
fiximg2 = pygame.image.load('image/approach2.png')
pygame.mixer.music.set_volume(0.1)
rect = pygame.Rect(0,0,250,253)
centers = [(i*250+165,360) for i in range(4)]
pygame.mixer.music.play(1,0)
starttime = time.time()
# with Listener(on_press=on_press) as listener:
#     listener.join()
def start_listener():
    """启动键盘监听器"""
    with Listener(on_press=on_press) as listener:
        listener.join()
listener_thread = threading.Thread(target=start_listener)
listener_thread.daemon = True  # 设置为守护线程
listener_thread.start()
# q = Queue()
#
# def get_ges():
#     return Gesture_recognition.shared_data['value']

current_key_value = None


while True:
    screen.fill((0,0,0))

    if bg:
        screen.blit(bgimg,bgrect)
        pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            way.press(event.key)
            print(event.key)
    for i in range(4):
        rect.center = centers[i]
        screen.blit(fiximg,rect)
    for i in [0,3]:
        rect.center = (centers[i][0]+63,centers[i][1]+63)
        screen.blit(fiximg1,rect)
    for i in [1,2]:
        rect.center = (centers[i][0]+63,centers[i][1]+63)
        screen.blit(fiximg2,rect)
    if AUTO:autopressed()
    addshows()
    combo.update()
    way.update()
    showcommand.update()
    showscore.update()
    FPS = clock.tick(90)
    pygame.display.flip()
