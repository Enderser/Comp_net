from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get('https://www.wildberries.ru/catalog/elektronika/igry-i-razvlecheniya/aksessuary/garnitury')
elems  =  driver.find_elements(By.CLASS_NAME,  'div > div.product-card__middle-wrap > div.product-card__price > span.price__wrap > ins')
print(elems)