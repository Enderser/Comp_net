import csv
import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


base_url = 'https://www.wildberries.ru/catalog/elektronika/igry-i-razvlecheniya/aksessuary/garnitury'
mx_pages = int(input("Сколько страниц парсим?\n"))
flag_art_outputs = True if input("Выводить прогресс сохранения товаров?(y/n)\n").lower() == 'y' else False
driver = webdriver.Firefox()
with open("res.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Название товара", "Артикул", "Цена", "Цена без скидки", "Цена с картой WB", "Ссылка"])

for page in range(1, mx_pages + 1):
    print(f"Загрузка {page} страницы")
    driver.get(f"{base_url}?page={page}")
    time.sleep(5)

    for _ in range(10):  
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    products = driver.find_elements(By.CSS_SELECTOR, ".product-card__link")
    if not products:
        print("Тут ничего нет, можно отдыхать")
        continue
    product_links = [product.get_attribute("href") for product in products]
    for link in product_links:
        driver.get(link)
        try:
            wait = WebDriverWait(driver, 10)
            title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))).text

            product_id = re.search(r"/catalog/(\d+)/", link)
            product_id = product_id.group(1) if product_id else "Не найден"

            price_elem = driver.find_elements(By.CSS_SELECTOR, ".price-block__final-price")
            price = price_elem[0].text if price_elem else "Нет цены"

            old_price_elem = driver.find_elements(By.CSS_SELECTOR, ".price-block__old-price")
            old_price = old_price_elem[0].text if old_price_elem else "Нет цены без скидки"

            wb_card_price_elem = driver.find_elements(By.CSS_SELECTOR, ".price-block__wallet-price")
            wb_card_price = wb_card_price_elem[0].text if wb_card_price_elem else "Нет цены с картой"

            with open("res.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([title, product_id, price, old_price, wb_card_price, link])

            if flag_art_outputs:
                print(f"Сохранено: Артикул {product_id}")

        except Exception as e:
            print("Ошибка:", e)

    print("Найдено товаров на странице:", len(product_links))
driver.quit()
