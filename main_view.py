import keyboard as kb
import pyautogui as pag
from time import sleep

pag.PAUSE = 0.5
delay = 0.5

names = [
    'app number',
    'magnifier',
    'exit'
]


def get_coordinates(stay):
    coordinates = {}
    for i in range(len(names)):
        sleep(stay)
        coordinates[names[i]] = pag.position()
        pag.click()
    return coordinates

coords = {'app number': (470, 177),
          'exit': (985, 75),
          'magnifier': (965, 254)}


def viewing():
    kb.press('alt')
    kb.send('tab')
    sleep(delay)
    kb.send('tab')
    kb.release('alt')

    sleep(delay)
    kb.send('ctrl+1')
    sleep(delay)

    pag.moveTo(coords['app number'])
    pag.click(coords['app number'])

    while True:
        for _ in range(2):
            kb.send('backspace')
        kb.wait('enter')
        sleep(delay)
        pag.click(coords['magnifier'])
        kb.wait('enter')
        pag.click(coords['exit'])
        pag.click()
        pag.click(coords['app number'])

    kb.send('alt+tab')

try:
	viewing()
except KeyboardInterrupt:
	print('\nDone')
