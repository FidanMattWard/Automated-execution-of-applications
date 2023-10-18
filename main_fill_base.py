import keyboard as kb
from time import sleep

delay_0 = 0.5
delay_1 = 0.7

def fill_base():
    mod = input('Введите код режима: ')
    kb.press('alt')
    kb.send('tab')
    sleep(delay_0)
    kb.send('tab')
    kb.release('alt')

    while True:
        kb.wait('m')
        if mod == '1':
            sleep(0.1)
            kb.send('enter')
            sleep(delay_1)
        elif mod == '0':
            kb.send('f5')
            sleep(delay_0)
        kb.send('down')
        if mod == '1':
            kb.send('down')
            sleep(0.1)
        kb.write(' лично')
        kb.wait('enter')

try:
	fill_base()
except KeyboardInterrupt:
	print('Done')
