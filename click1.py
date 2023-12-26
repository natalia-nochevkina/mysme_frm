from pymouse import PyMouse
from PIL import ImageGrab, ImageOps
import time
import re
import pytesseract

#         x,    y,  clr
sett = (626,  101,  594)
load = (458,  364,  765)
slot = (348,  219,  746)
conf = (226,  743,  411)
main = (409,  756,  765)
days = (224,  439,  263)
chat = (433,  573,  153)
mspd = (216,  95,   336)
anss = (554,  524)
psed = (318,  1037, 178)
paus = (318,  1037, 260)
answ = (292,  1023, 550)
save = (318,  1037, 756)
exit = (383,  670,  765)
time0 = 1285
time1 = 1381
m = PyMouse()

def click(x, y):
    pos = m.position()
    m.click(x, y)
    m.move(*pos)

def get_clr(x, y):
    im = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    return sum(im.convert('RGB').getpixel((0,0)))

def wait_color(x, y, color, s1 = 0.01, s2 = 0.02, single = False):
    a = -1
    while (a != color):
        a = get_clr(x, y)
    time.sleep(s1)
    while (a == color):
        click(x, y)
        if single: break
        time.sleep(s2)
        a = get_clr(x, y)

def norm(b):
    return ("0" if b < 10 else "") + str(b)

def makelog(n):
    time.sleep(0.2)
    hs_im = ImageOps.invert(ImageGrab.grab(bbox=(486, 77, 590, 106)))
    hg_im = ImageOps.invert(ImageGrab.grab(bbox=(272, 77, 380, 106)))
    hs = int(re.sub(r'[^0-9]', '', pytesseract.image_to_string(hs_im, config='--psm 7')))
    hg = int(re.sub(r'[^0-9]', '', pytesseract.image_to_string(hg_im, config='--psm 7')))
    b = time.localtime()
    a = f'[{norm(b[3])}:{norm(b[4])}:{norm(b[5])} {n} times]  '
    a+= f' ⧖:{hg + hs // 100}   ❤︎:{hs % 100}.'
    print(a)

st = time.time() - 350
numb = 0
while True:
    wait_color(*sett)
    wait_color(*load)
    wait_color(*slot)
    wait_color(*conf)
    wait_color(*main)

    l = time.time()
    if (l - st) > 300:
        st = l
        makelog(numb)
        numb = 0

    wait_color(*days)

    l = time.localtime()
    t = l[3] * 60 + l[4]
    wait_color(*chat, 0.8)
    wait_color(*mspd, single=True)
    
    b = -1
    while b != save[2]:
        a = get_clr(292,  1023)
        b = get_clr(318,  1037)
        if   (a == answ[2]):
            click(*answ[0:2])
            time.sleep(0.01)
        elif (b == psed[2]):
            click(*anss)
            time.sleep(0.01)
        elif (b == paus[2]):
            click(*paus[0:2])
            time.sleep(0.07)

    wait_color(*save)
    wait_color(*exit)
    numb += 1
