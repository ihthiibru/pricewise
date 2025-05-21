import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()

# Explicitly specify the ChromeDriver path
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


# Set headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Configure Selenium WebDriver
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={HEADERS['User-Agent']}")
    
    service = Service(ChromeDriverManager().install())  # Auto-install ChromeDriver
    return webdriver.Chrome(service=service, options=options)

# Scraper function
def scrape_price(url, platform):
    print(f"\n🔍 Scraping {platform} for URL: {url}")

    # Use BeautifulSoup for static pages
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            if platform == "amazon":
                price = soup.select_one("span.a-price-whole")
                return price.text if price else "Price not found"

            elif platform == "flipkart":
                price = soup.select_one("div._30jeq3")  # Flipkart's price class
                return price.text if price else "Price not found"

            elif platform == "ebay":
                price = soup.select_one("div.x-price-primary span")
                return price.text if price else "Price not found"

            elif platform == "walmart":
                price = soup.select_one("span.price-characteristic")
                return price.text if price else "Price not found"

    except Exception as e:
        print(f"⚠️ Error using BeautifulSoup: {e}")

    # If BeautifulSoup fails, use Selenium for JavaScript-rendered prices
    print("🔄 Switching to Selenium...")
    driver = get_driver()
    driver.get(url)

    try:
        if platform == "amazon":
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole"))
            )
        
        elif platform == "flipkart":
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_30jeq3"))
            )
        
        elif platform == "ebay":
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "x-price-primary"))
            )
        
        elif platform == "walmart":
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "price-characteristic"))
            )
        
        else:
            driver.quit()
            return "❌ Unsupported Platform"
        
        price = price_element.text
    except Exception as e:
        price = "❌ Price not found (Selenium failed)"
        print(f"⚠️ Selenium Error: {e}")

    driver.quit()
    return price

# Test URLs (Replace with actual product links)
urls = {
    "amazon": "https://www.amazon.com/dp/B09G3HRMVB",
    "flipkart": "https://www.flipkart.com/some-product-url",
    "ebay": "https://www.ebay.com/itm/some-product-id",
    "walmart": "https://www.walmart.com/ip/some-product-id"
}

# Run scraper for each platform
for platform, url in urls.items():
    price = scrape_price(url, platform)
    print(f"✅ {platform.capitalize()} Price: {price}")
