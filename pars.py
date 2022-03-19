import time
from telnetlib import EC

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging


from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext



def ex_price(driver):
    exist_result = []
    driver.find_element(By.ID, value='priceBody')
    exist_price_body = driver.find_element(By.CLASS_NAME, value='table-body')
    exist_allOffers = exist_price_body.find_element(By.CLASS_NAME, value='allOffers')
    exist_brand = exist_price_body.find_element(By.CLASS_NAME, value='art')
    exist_type = exist_price_body.find_element(By.CLASS_NAME, value='descr')
    exist_delivery = exist_allOffers.find_element(By.CLASS_NAME, value='statis')
    exist_price = exist_allOffers.find_element(By.CLASS_NAME, value='price')
    exist_result.append(exist_brand.text)
    exist_result.append(exist_type.text)
    exist_result.append(exist_price.text)
    exist_result.append(exist_delivery.text)

    return (exist_result)

def catalog(driver):
    brands_catalogs = []
    options = []
    links = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    catalogs = soup.find(class_ = 'catalogs')
    all_catalogs = catalogs.find_all('a')
    for catalog in all_catalogs:
        links.append(catalog.get('href'))
    all_b = catalogs.find_all('b')
    for b in all_b:
        brands_catalogs.append(b.text.strip())
    all_dd = catalogs.find_all('dd')
    for dd in all_dd:
        options.append(dd.text.strip())
    return brands_catalogs, options, links

def change_office(driver, city):
    # options = Options()                             запуск Chromedriver
    # options.add_argument('--headless')
    driver = webdriver.Chrome()  # (options=options)
    exist_url = "https://www.exist.ru/"
    driver.get(exist_url)
    # выберем нужный город
    # офис выбраный автоматически загружается позже основной страницы
    # ожидание 10секунд, частота проверки 1с, игнорируем ошибки
    wait = WebDriverWait(driver, 10, poll_frequency=1,
                         ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,
                                             StaleElementReferenceException])
    office = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                    '/html/body/div[1]/header/section[1]/div/div[2]/span/div[1]/span/a')))  # ждать пока элемент выбора офиса станет доступным
    office.click()  # нажать на выбор офиса
    driver.switch_to.frame(0)  # перейти на модальное окно
    change = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                    '/html/body/form/table/tbody/tr/td/div/div[1]/a[1]')))  # ждать пока элемент "изменить" станет доступным
    change.click()  # нажать изменить
    city_search = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                         '/html/body/form/table/tbody/tr/td/div[2]/div[6]/ymaps/ymaps[5]/ymaps[1]/ymaps[2]/ymaps/ymaps/ymaps[1]/ymaps/ymaps/ymaps/ymaps[1]/ymaps/ymaps[2]/input')))
    city_search.send_keys(city + Keys.ENTER) # найти поле ввода и ввести туда название города
    time.sleep(11)
    driver.switch_to.default_content() # переключиться на основную страницу
    return exist_parser(driver, part_number)

def exist_parser(driver, part_number):
    driver.find_element(By.ID, value='pcode').send_keys(part_number + Keys.ENTER)   #поиск part_number на сайте
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    header = soup.h1                                                                #поиск заголовка на полученой странице
    header = header.text.strip()
    if header.find('Предложения для') != -1:                                        # если part_number найден запускаем ex_price() для получения цены, наименования и сроков поставки
        exist_result = ex_price(driver)
    elif header.find('Выберите каталог') != -1:                                     # если part_number существует в нескольких каталогах запускаем catalog() для выбора каталога
        possible_catalogs = catalog(driver)
    else:
        exist_result = 'По вашему запросу ничего не найдено'                        # если part_number не найден
    return exist_result

city = 'Самара'
part_number = '164005420R'
print('примеры для отладки')
print('фильтр топливный 16 40 054 20R')
print('лампа 9117175 выбор каталога' )
print('------------------------------')
#print('введите ваш город:')
#city = input ()
#print('введите номер для поиска:')
#part_number =input()
print(change_office(part_number, city))
