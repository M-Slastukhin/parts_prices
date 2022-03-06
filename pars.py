from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def exist_parser(part_number):
    exist_result = {}
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    exist_url = "https://www.exist.ru/"
    driver.get(exist_url)
    driver.find_element(By.ID, value='pcode').send_keys(part_number + Keys.ENTER)
    exist_price_body = driver.find_element(By.CLASS_NAME, value='table-body')
    exist_allOffers = exist_price_body.find_element(By.CLASS_NAME, value='allOffers')
    exist_delivery = exist_allOffers.find_element(By.CLASS_NAME, value='statis')
    exist_price = exist_allOffers.find_element(By.CLASS_NAME, value='price')
    exist_result[exist_price.text] = exist_delivery.text
    print(exist_result)
    return (exist_allOffers)


    #driver.close()

part_number = '164005420R'
print(exist_parser(part_number).text)
