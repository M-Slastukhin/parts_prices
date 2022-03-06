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
    #code = driver.read()
    exist_catalog = driver.find_element(By.CLASS_NAME, value='catalogs')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.findAll('a')

    return links

def exist_parser(part_number):
    #exist_result = {}
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    exist_url = "https://www.exist.ru/"
    driver.get(exist_url)
    driver.find_element(By.ID, value='pcode').send_keys(part_number + Keys.ENTER)
    exist_content_inner = driver.find_element(By.CLASS_NAME, value='content')
    content_inner = exist_content_inner.text
    found = content_inner.find('Предложения для')
    choose_catalog = content_inner.find('Выберите каталог')
    not_found = content_inner.find('По вашему запросу ничего не найдено')
    if not_found != -1:
        exist_result = 'По вашему запросу ничего не найдено'
    elif choose_catalog != -1:
        exist_result = catalog(driver)
    elif found != -1:
        exist_result = ex_price(driver)
    return exist_result




part_number = '164005420R'
print(exist_parser(part_number))
