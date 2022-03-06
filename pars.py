from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def exist_parser(part_number):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    exist_url = "https://www.exist.ru/Price/?pcode=164005420R"
    driver.get(exist_url)
    exist_price_body = driver.find_element(By.CLASS_NAME, value='table-body')
    exist_allOffers = exist_price_body.find_element(By.CLASS_NAME, value='allOffers')

    #print(exist_allOffers.text)
    return (exist_allOffers)


    #driver.close()

part_number = '164005420R'
print (exist_parser(part_number).text)
