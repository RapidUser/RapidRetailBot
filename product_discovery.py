
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
import csv

def launch_browser():
    options = Options()
    options.add_argument("--headless")
    return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

def scrape_amazon_best_sellers():
    print("🌐 Scraping Amazon Best Sellers...")
    driver = launch_browser()
    driver.get("https://www.amazon.com/Best-Sellers/zgbs")
    time.sleep(5)

    products = []

    try:
        items = driver.find_elements(By.CSS_SELECTOR, "div.p13n-sc-uncoverable-faceout")
        for item in items[:10]:
            try:
                title_el = item.find_element(By.CSS_SELECTOR, "span.a-size-medium")
                title = title_el.text.strip()

                link_el = item.find_element(By.CSS_SELECTOR, "a.a-link-normal")
                link = link_el.get_attribute("href")

                rating_el = item.find_elements(By.CSS_SELECTOR, "span.a-icon-alt")
                rating = rating_el[0].text if rating_el else "N/A"

                reviews_el = item.find_elements(By.CSS_SELECTOR, "span.a-size-small")
                reviews = reviews_el[0].text if reviews_el else "N/A"

                price_el = item.find_elements(By.CSS_SELECTOR, "span.a-price > span.a-offscreen")
                price = price_el[0].text if price_el else "N/A"

                products.append({
                    "title": title,
                    "link": link,
                    "price": price,
                    "rating": rating,
                    "reviews": reviews
                })
            except Exception as e:
                continue
    finally:
        driver.quit()

    return products

def save_to_csv(products):
    keys = ["title", "link", "price", "rating", "reviews"]
    with open("amazon_product_discovery.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)
    print("✅ Saved product data to amazon_product_discovery.csv")

if __name__ == "__main__":
    data = scrape_amazon_best_sellers()
    if data:
        for i, product in enumerate(data, 1):
            print(f"{i}. {product['title']} - {product['price']}")
        save_to_csv(data)
    else:
        print("❌ No products found.")
