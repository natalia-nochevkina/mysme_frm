from pymouse import PyMouse
from PIL import ImageGrab, ImageOps
import time
import re
import pytesseract

#       x,    y,    clr

# settings button (the grey part)
sett = (626,  101,  594)
# load icon (the white part of it)
load = (458,  364,  765)
# autosave slot (anywhere)
slot = (348,  219,  746)
# confirm button
conf = (261, 761, 765)
# big "chatroom button" (also something white)
main = (409,  756,  765)
# first day
days = (224,  439,  263)
# chat place depending on time
# after 23:01
cha0 = (433,  573,  153)
# after 20:53
cha1 = (433,  858,  153)
# after 19:18
cha2 = (433, 1044, 153)
# max speed button (anywhere)
mspd = (216,  95,   336)
# just the coordinates of answers
# (you should be able to click 
# regardless of number of answers)
anss = (554,  524)
# chat button if waiting for the answer
psed = (318,  1037, 178)
# chat button if paused 
paus = (318,  1037, 260)
# chat button if golden
answ = (292,  1023, 550)
# chat button if has save icon
save = (318,  1037, 756)
# exit button after save
exit = (383,  670,  765)

time2 = 19 * 60 + 18
time1 = 20 * 60 + 53
time0 = 23 * 60 +  1

# "time" of you save in (hh * 60 + mm) format  
timeS = 22 * 60 +  6

# for makelog, optional
# (top left coord concat bottom right 
# coord of the box) 

# whether you want it or not
log = True
# hourglasses box
hg_box = (272, 77, 380, 106)
# hearts box
hs_box = (486, 77, 590, 106)
# log time in minutes
lg = 5

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
    hs_im = ImageOps.invert(ImageGrab.grab(bbox=hs_box))
    hg_im = ImageOps.invert(ImageGrab.grab(bbox=hg_box))
    hs = int(re.sub(r'[^0-9]', '', pytesseract.image_to_string(hs_im, config='--psm 7')))
    hg = int(re.sub(r'[^0-9]', '', pytesseract.image_to_string(hg_im, config='--psm 7')))
    b = time.localtime()
    a = f'[{norm(b[3])}:{norm(b[4])}:{norm(b[5])} {n} times]  '
    a+= f' ⧖:{hg + hs // 100}   ❤︎:{hs % 100}.'
    print(a)

st = time.time() - lg * 65
numb = 0

while True:
    wait_color(*sett)
    wait_color(*load)
    wait_color(*slot)
    wait_color(*conf)
    wait_color(*main)

    l = time.time()
    if (l - st) > lg * 60:
        st = l
        if log:
            makelog(numb)
        numb = 0

    wait_color(*days)

    l = time.localtime()
    t = l[3] * 60 + l[4]
    chat = 0

    if time1 >= t >= timeS > time2:
        chat = cha2
    elif (time1 >= t > time2 and time0 >= timeS > time1) \
        or (time0 >= t >= timeS > time1):
        chat = cha1
    else:
        chat = cha0
    
    wait_color(*chat, 0.8)
    wait_color(*mspd, single=True)
    
    d = -1
    while d != save[2]:
        a = get_clr(*answ[0:2])
        b = get_clr(*psed[0:2])
        c = get_clr(*paus[0:2])
        d = get_clr(*save[0:2])

        if   (a == answ[2]):
            click(*answ[0:2])
            time.sleep(0.01)
        elif (b == psed[2]):
            click(*anss)
            time.sleep(0.01)
        elif (c == paus[2]):
            click(*paus[0:2])
            time.sleep(0.07)

    wait_color(*save)
    wait_color(*exit)
    numb += 1
