import keyboard as kb
import pyautogui as pag
from re import fullmatch
from time import sleep, time
from datetime import date
from re import fullmatch

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

pag.PAUSE = 0.3
delay = 0.7

def web_wait(t_delay, driver, by, key):
    return WebDriverWait(driver, t_delay).until(
        EC.presence_of_element_located((by, key)))

PATH = 'X:\\Tele2\\Исправление\\'
with open('passwd.txt') as file:
        passwd = file.readline()

abbreviations = {
    'а': 'адрес регистрации',
    'г': 'гражданство',
    'д': 'дом',
    'дв': 'дата выдачи',
    'док': 'документ, удостоверяющий личность',
    'др': 'дата рождения',
    'и': 'имя',
    'кв': 'квартира',
    'ке': 'кем выдан',
    'ко': 'корпус',
    'кп': 'код подразделения',
    'мр': 'место рождения',
    'н': 'номер паспорта',
    'нп': 'населенный пункт',
    'о': 'отчество',
    'п': 'пол',
    'с': 'серия паспорта',
    'у': 'улица',
    'ф': 'фамилия',
    'фио': 'ФИО'
}  # расшифровка сокращений

order = ['ф', 'и', 'о', 'фио', 'п',
         'г', 'др', 'мр', 'док', 'с',
         'н', 'дв', 'ке', 'кп', 'дп', 'нп',
         'у', 'д', 'ко', 'кв', 'а']
# порядок заполнения последней строки

matches = [('full name', ['ф', 'и', 'о', 'фио']),
           ('date of birth', ['др']),
           ('burn address', ['мр']),
           ('passport details', ['док', 'с', 'н', 'дв', 'ке', 'кп', 'дп']),
           ('registration address', ['нп', 'у', 'д', 'ко', 'кв', 'а'])]

def convert_post(post):
    post = post.replace('оуф мо', 'ОУФМС России по Московской области')
    post = post.replace('оуф м', 'ОУФМС России по гор. Москве')
    post = post.replace('оуф', 'ОУФМС России')
    
    post = post.replace('уф мо', 'УФМС России по Московской области')
    post = post.replace('уф м', 'УФМС России по гор. Москве')
    post = post.replace('уф', 'УФМС России')
    
    post = post.replace('москве', 'Москве')
    post = post.replace('московской', 'Московской')
    post = post.replace(' россии', ' России')

    post = post.replace('гм р', 'ГУ МВД России по')
    post = post.replace('гм мо', 'ГУ МВД России по Московской области')
    post = post.replace('гм м', 'ГУ МВД России по г. Москве')
    post = post[0].upper() + post[1:]
    return post




def convert_address(address):
    replaces = {
        ' кв-л ': ' квартал ',
        'пр-д': 'проезд',
        'пр-кт': 'проспект',
        ' п ': ' пос. ',
        ' д ': ' дер. ',
        'б-р': 'бульвар',
        ' ш ': ' шоссе '
        }
    if address.startswith('обл '):
        index_comma = address.find(',')
        address = address[4:index_comma] + ' обл.' + address[index_comma:]
    if ' р-н ' in address:
        index_district = address.find(' р-н ') + 1
        index_comma = address.find(',', index_district)
        address = address[:index_district] + address[index_district + 4:index_comma] + ' район' + address[index_comma:]
    if ' обл ' in address:
        index_district = address.find(' обл ') + 1
        index_comma = address.find(',', index_district)
        address = address[:index_district] + address[index_district + 4:index_comma] + ' обл.' + address[index_comma:]
    for prefix in ['Респ ', 'г ']:
        if address.startswith(prefix):
            address = f'{prefix.rstrip()}. {address.lstrip(prefix)}'
    for sub in ['г', 'ул', 'мкр', 'с', 'пгт', 'тер', 'х', 'рп', 'дп', 'пос', 'пер', 'двлд']:
        address = address.replace(f' {sub} ', f' {sub}. ')
    for key, val in replaces.items():
        address = address.replace(key, val)
    if address.startswith('г.'):
        return address
    address = address.split(', ')
    for i in range(len(address)):
        if address[i].startswith('д.') or address[i].startswith('двлд.'):
            loc, address = address[i - 2::-1], address[i - 1:]
            print(loc, address)
            address = ' '.join(loc) + ', ' + ', '.join(address)
            return address
    else:
        loc = address[::-1]
        print(loc)
        return ' '.join(loc)


# функция ввода необходимой информации о корректировке (номер, фамилия для поиска файлов и корректирующие строки) 
def get_data(counter):
    while True:
        number = input('Введите номер абонента: ')
        if fullmatch('9[0-9*]{9}', number) is not None:
            number = number.replace('*', '0')
            break
        print('Введен номер, не соответствующий шаблону ------------------------------------')

    print('\n----------------------------------\n')
    print('Расшифровка сокращений:')
    for key, value in sorted(abbreviations.items(), key=lambda x: x[1].lower()):
        print(f'{value} - {key}')
    print()

    while True:
        correction_dict = dict.fromkeys(input('Введите сокращения через пробел: ').lower().split(), 0)
            
        print('Введите исправленные значения: ')
        for key in correction_dict:
            try:
                if key == 'ке':
                    print('Используйте сокращения: оуф, оуф м, оуф мо, уф, уф м, уф мо, гм р, гм м, гм мо')
                value = input(f'{abbreviations[key]} - ')
            except KeyError:
                print('Введите значения, которые есть в словаре')
                break
            if key == 'п':
                value = value.lower()
                if value.startswith('м') or value.startswith('ж'):
                    value = value[0]
            elif key == 'д':
                value = 'д. ' + value
            elif key == 'ко':
                value = 'к. ' + value
            elif key == 'кв':
                value = 'кв. ' + value
            elif key in ['а', 'нп', 'мр', 'у']:
                value = convert_address(value)
                if key == 'у':
                    value = value.title()
            elif key in ['ф', 'и', 'о', 'фио', 'г']:
                value = value.title()
            elif key in ['др', 'дв'] and '.' not in value:
                value = value[:2] + '.' + value[2:4] + '.' + value[4:]
            elif key == 'ке':
                value = convert_post(value)

            correction_dict[key] = value
            surname = ''
        else:
            break

    return number, surname, correction_dict


def form_correction_string(correction_dict):
    correction_string = []
    address = []
    for key in order:
        if key in correction_dict:
            tail = f' ({correction_dict[key]})' if key in ['п', 'г'] else ''
            if key in ['нп', 'у', 'д', 'ко', 'кв']:
                address.append(abbreviations[key])
            else:
                correction_string.append(abbreviations[key] + tail)
    if address:
        address = f'адрес регистрации ({", ".join(address)})'
        correction_string.append(address)
    correction_string = ', '.join(correction_string)
    correction_string = correction_string[0].upper() + correction_string[1:]
    return correction_string


def form_options(correction_dict, labels):
    options = []
    for label in labels:
        if label in correction_dict:
            options.append(correction_dict[label])
    options = ', '.join(options)
    return options if options else '-'


def create_request(counter, path, browser, actions):
    prefix = path if not counter else ''

    number, surname, correction_dict = get_data(counter)
    correction_string = form_correction_string(correction_dict)
    web_wait(10, browser, By.CSS_SELECTOR, '[title="Номер телефона полностью (10 цифр), без префикса 8 или +7"]')
    elem = browser.find_element(By.CSS_SELECTOR, '[title="Номер телефона полностью (10 цифр), без префикса 8 или +7"]')
    elem.click()
    actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
    elem.send_keys(number + '\n')
    web_wait(5, browser, By.CLASS_NAME, 'z-tree-root-close')
    browser.find_elements(By.CLASS_NAME, 'z-tree-ico')[28].click()
    sleep(0.3)
    browser.find_elements(By.CSS_SELECTOR, '[type="checkbox"]')[19].click()
    browser.find_element(By.CSS_SELECTOR, '[title="Зарегистрировать новую заявку абонента"]').click()
    web_wait(2, browser, By.CLASS_NAME, 'tabinputs')
    elem = browser.find_elements(By.CLASS_NAME, 'tabinputs')[5]
    elem.click()
    actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
    elem.send_keys('79777777777')
    browser.find_element(By.CSS_SELECTOR, '[title="Дополнительная информация:"]').send_keys('Классика')
    browser.find_element(By.CSS_SELECTOR, '[selectedindex="0"]').click()
    elem = browser.find_element(By.XPATH, '//option[text()="Администрирование"]')
    elem.click()
    elem.click()
    sleep(0.1)
    
    elems = browser.find_elements(By.CSS_SELECTOR, '[style="width:99%;"]')
    while True:
        try:
            elems[1].send_keys(number)
        except:
            sleep(1)
            pass
        else:
            break
    for j in range(len(matches)):
        labels = matches[j][1]
        options = form_options(correction_dict, labels)
        while True:
            try:
                elems[j + 2].send_keys(options)
            except:
                pass
            else:
                break
    elems[7].send_keys(correction_string)
    kb.wait('esc')   
    
    browser.find_elements(By.CLASS_NAME, 'dblClickProtected')[8].click()

    kb.wait('enter')


def form_requests():
    start = time()
    global PATH, passwd
    dt = date.today()
    year, month, day = map(str, [dt.year, dt.month, dt.day])
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    PATH += f'{month}\\{day}\\'
    print(PATH)
    amount = int(input('Введите количество заявок: '))

    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(options=options, executable_path=r'C:\chromedriver\chromedriver.exe')

    browser.get('https://www.t2wd.tele2.ru/t2wd/login.zul')
    browser.maximize_window()
    browser.find_element(By.NAME, 'j_username').send_keys('makieva_nadezhda')
    browser.find_element(By.NAME, 'j_password').send_keys(passwd)
    browser.find_element(By.XPATH, '//button[text()="Войти"]').click()
    
    web_wait(10, browser, By.CLASS_NAME, 'z-combobox-inp').send_keys('811874')
##    921958
##    811874
    browser.find_element(By.CLASS_NAME, 'z-button-os').click()
    web_wait(10, browser, By.XPATH, '//button[text()="ОК"]').click()
    elem = web_wait(10, browser, By.XPATH, '//button[contains(text(), "Операции")]')
    elem.click()
    elem.click()
    browser.find_elements(By.CLASS_NAME, 'z-menu-item-cnt')[17].click()

    actions = ActionChains(browser)
    for i in range(amount):
        try:
            create_request(i, PATH, browser, actions)
        finally:
            pass
    seconds = time() - start
    print(f'{seconds / 60} seconds passed\n{seconds / 60 / amount}')

try:
	form_requests()
except KeyboardInterrupt:
	print('\nDone')
