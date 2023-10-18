import keyboard as kb
import pyautogui as pag
from time import sleep, time
from datetime import date, timedelta
from re import fullmatch

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


pag.PAUSE = 0.3
PATH = 'X:\\Tele2\\Scan'
with open('passwd.txt') as file:
        passwd = file.readline()

def web_wait(t_delay, driver, by, key):
    return WebDriverWait(driver, t_delay).until(
        EC.presence_of_element_located((by, key)))

def form_list(amount, flag):
    lst = []
    for i in range(amount):
        while True:
            try:
                if flag == '0':
                    number_tele2, passport_number, portable_number, surname = input(
                        ).lower().replace('*', '0').split('/')
                else:
                    number_tele2, passport_number, portable_number = input(
                        ).lower().replace('*', '0').split('/')
                    surname = 'фамилия'
            
            except ValueError:
                pass
            else:
                break
        while True:
            if fullmatch('9[0-9*]{9}', number_tele2):
                break
            print('Введите корректный номер ------------------------------')
            number_tele2 = input('Введите номер Tele2: ')

        while True:
            if fullmatch('[0-9*]{5,6}', passport_number):
                    break
            print('Введите корректный номер паспорта ------------------------------')
            passport_number = input('Введите номер паспорта: ')

        while True:
            if fullmatch('9[0-9*]{9}', number_tele2):
                break
            print('Введите корректный номер ------------------------------')
            portable_number = input('Введите номер к переносу: ')

        while True:
            if surname and surname[0].isalpha():
                break
            print('Введите корректную фамилию ------------------------------')
            surname = input('Введите фамилию: ').lower()
        lst.append({
            'number_tele2': number_tele2,
            'passport_number': passport_number,
            'portable_number': portable_number,
            'surname': surname
        })
    return lst

def fill_out_MNP_application(driver, actions, i, day, PATH, mods, number_Tele2, passport_number, portable_number, surname):
    web_wait(10, driver, By.CSS_SELECTOR, '[title="Номер лицевого счета"]')
    while True:
        number = driver.find_elements(By.CSS_SELECTOR, '[title="Номер телефона полностью (10 цифр), без префикса 8 или +7"]')[0]
        number.send_keys(number_Tele2)
        passport = driver.find_elements(By.CSS_SELECTOR,
                             '[title="Номер документа, указанного при регистрации контракта: от 5 до 20 цифр или латинских букв (A-Z)"]'
                             )[0]
        passport.send_keys(passport_number + '\n')
        if not i:
            web_wait(5, driver, By.CSS_SELECTOR, '.z-messagebox-btn.z-button-os')
            driver.find_elements(By.CSS_SELECTOR, '.z-messagebox-btn.z-button-os')[0].click()
        try:
            web_wait(5, driver, By.XPATH, '//span[contains(text(), "Статус клиента")]')
        except:
            try:
            	driver.find_element(By.XPATH, '//button[text()="ОК"]').click()
            except:
            	pass
            web_wait(10, driver, By.CSS_SELECTOR, '[title="Номер лицевого счета"]')
            number.click()
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
            passport.click()
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
            temp = input(f'{number_Tele2} - ')
            if temp:
                number_Tele2 = temp
            temp = input(f'{passport_number} - ')
            if temp:
                passport_number = temp
        else:
            break
    elem = driver.find_element(By.XPATH, '//button[contains(text(), "Операции")]')
    actions.move_to_element(elem)
    actions.perform()
    sleep(1)
    elem = driver.find_elements(By.CLASS_NAME, 'z-menu-item-cnt')[47].click()
    while True:
        try:
            web_wait(2, driver, By.XPATH, '//button[text()="ОК"]').click()
        except:
            pass
        windows = driver.window_handles
        if len(windows) == i + 2:
            driver.switch_to.window(windows[-1])
            break
        else:
            print('STOP')
            
    if mods[0] == '1':
        kb.wait('esc')
        
        
    web_wait(10, driver, By.CSS_SELECTOR, '[for="mode:0"]')
    driver.find_element(By.ID, 'phone').send_keys(number_Tele2)
    driver.find_element(By.ID, 'b2c:transferPhoneNumber0').send_keys(portable_number)

    elem = f'//a[text()="{day}"]'
    while True:
        try:
            driver.find_element(By.ID, 'selectTransferDateBtn').click()
        except:
            sleep(2)
        else:
            break
    web_wait(10, driver, By.XPATH, elem)
    driver.find_element(By.XPATH, elem).click()
    web_wait(10, driver, By.CSS_SELECTOR, '[for="selectedTimeslot:14"]')
    driver.find_element(By.ID, 'updateStartServiceDate').click()

    sleep(1.5)
    web_wait(5, driver, By.ID, 'generateRequestId').click()
    sleep(1)
    if mods[1] == '0':
        elem = driver.find_element(By.ID, 'requestDocument')
        print(f'{PATH}{surname}.jpg')
        while True:
            try:
                elem.send_keys(f'{PATH}{surname}.jpg')
            except:
                try:
                    elem.send_keys(f'{PATH}{surname} {portable_number[-2:]}.jpg')
                except:
                    surname = input(f'Новая фамилия ({surname}) - ').lower()
                else:
                    break
            else:
                break
                 
        driver.find_element(By.CSS_SELECTOR, '[value="На регистрацию"]').click()
    
    return windows


def main():
    start = time()
    global PATH
    dt = date.today()
    year, month, day = map(str, [dt.year, dt.month, dt.day])
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    PATH += f'\\{month}\\{day}\\'
    day = (dt + timedelta(days=8)).day
    print(day)
    print(PATH)

    amount = int(input('Введите количество заявлений: '))
    mods = list(input(
        'Введите коды режимов (2) через пробел (00 - обычный, без проверок, клавиша продолжения - esc): '))
    lst = form_list(amount, mods[1])
    
    driver = webdriver.Chrome()
    actions = ActionChains(driver)
    driver.get('https://www.t2wd.tele2.ru/t2wd/login.zul')
    driver.maximize_window()
    driver.find_element(By.NAME, 'j_username').send_keys('makieva_nadezhda')
    driver.find_element(By.NAME, 'j_password').send_keys(passwd)
    web_wait(10, driver, By.CLASS_NAME, 'z-combobox-inp').send_keys('811874\n')
    
    web_wait(5, driver, By.CLASS_NAME, 'z-window-highlighted-header')
    driver.find_elements(By.CLASS_NAME, 'z-messagebox-btn')[0].click()

    for i in range(amount):
        number_tele2 = lst[i]['number_tele2']
        passport_number = lst[i]['passport_number']
        portable_number = lst[i]['portable_number']
        surname = lst[i]['surname']
        windows = fill_out_MNP_application(driver, actions, i, day, PATH, mods, number_tele2, passport_number, portable_number, surname)
        print(len(windows))
        if len(windows) == i + 2:
            driver.switch_to.window(windows[0])
            web_wait(5, driver, By.CLASS_NAME, 'z-menu-item-btn')
            driver.find_elements(By.CLASS_NAME, 'z-menu-item-btn')[1].click()
            kb.send('enter')
            sleep(0.5)
            kb.send('f5')

    seconds = time() - start
    print(f'{seconds} seconds passed\n{seconds / 60 / amount}')
    kb.wait('esc')

try:
	main()
except KeyboardInterrupt:
	print('\nDone')
