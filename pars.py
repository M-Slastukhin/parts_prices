from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



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
    exist_catalog = driver.find_element(By.CLASS_NAME, value='catalogs')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    hah = soup.h1
    catalogs = soup.find_all(class_ = 'catalogs')
    #links = catalogs.find_all('a')
    #for link in soup.find_all(ul class_ = 'catalogs'):
    print(hah)
    #return links

def exist_parser(part_number):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    exist_url = "https://www.exist.ru/"
    driver.get(exist_url)
    driver.find_element(By.ID, value='pcode').send_keys(part_number + Keys.ENTER)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    header = soup.h1
    header = header.text.strip()
    if header.find('Предложения для') != -1:
        exist_result = ex_price(driver)
    elif header.find('Выберите каталог') != -1:
        exist_result = catalog(driver)
    else:
        exist_result = 'По вашему запросу ничего не найдено'
    return exist_result


part_number = ''
print('примеры для отладки')
print('фильтр топливный 16 40 054 20R')
print('лампа 9117175')
print('------------------------------')

print('введите номер для поиска:')
part_number =input()
print(exist_parser(part_number))
