from pynput import mouse
from PIL import ImageGrab

def on_click(x, y, button, pressed):
    if pressed: 
        im = ImageGrab.grab(bbox=(x, y, x+1, y+1))
        a = sum(im.convert('RGB').getpixel((0,0)))
        print(f'{x}, {y}, {a}')

while True:
    with mouse.Listener(on_click = on_click) as listener:
        listener.join()