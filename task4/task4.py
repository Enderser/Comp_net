import re
import time

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import uvicorn

Base = declarative_base()
engine = create_engine("postgresql://wb_user:wb_pass@localhost:5432/wb_db")
SessionLocal = sessionmaker(bind=engine)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    article = Column(String)
    price = Column(String)
    old_price = Column(String)
    wb_card_price = Column(String)
    link = Column(String)

Base.metadata.create_all(bind=engine)


app = FastAPI()


def parse_wb(base_url: str, max_pages: int = 1):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    results = []
    try:
        for page in range(1, max_pages + 1):
            driver.get(f"{base_url}?page={page}")
            time.sleep(5)

            for _ in range(10):
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
                time.sleep(2)

            products = driver.find_elements(By.CSS_SELECTOR, ".product-card__link")
            product_links = [p.get_attribute("href") for p in products]

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

                    results.append({
                        "title": title,
                        "article": product_id,
                        "price": price,
                        "old_price": old_price,
                        "wb_card_price": wb_card_price,
                        "link": link
                    })
                except Exception as e:
                    print(f"Ошибка при обработке товара: {e}")
    finally:
        driver.quit()

    return results

@app.get("/parse")
def parse_endpoint(url: str = Query(...), pages: int = Query(1, ge=1, le=10)):
    session = SessionLocal()
    try:
        parsed_data = parse_wb(url, pages)
        for item in parsed_data:
            session.add(Product(**item))
        session.commit()
        return {"status": "success", "parsed": len(parsed_data)}
    finally:
        session.close()

@app.get("/data")
def get_data():
    session = SessionLocal()
    try:
        products = session.query(Product).all()
        response = []
        for p in products:
            response.append({
                "id": p.id,
                "title": p.title,
                "article": p.article,
                "price": p.price,
                "old_price": p.old_price,
                "wb_card_price": p.wb_card_price,
                "link": p.link
            })
        return JSONResponse(content=response)
    finally:
        session.close()

if __name__ == "__main__":
    uvicorn.run("task4:app", host="127.0.0.1", port=8000, reload=True)

# curl "http://127.0.0.1:8000/parse?url=https://www.wildberries.ru/catalog/elektronika/igry-i-razvlecheniya/aksessuary/garnitury&pages=1"

