import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Specify the path to the ChromeDriver
chrome_driver_path = 'C:\\Users\\Medha Agarwal\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe'

# Initialize the ChromeDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    # Open the Blinkit website
    url = "https://www.bigbasket.com/member/sb/?nc=smart_basket"
    driver.get(url)

    # Allow the page to load
    time.sleep(5)

    # Get the page source
    html = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all product container elements
    product_containers = soup.find_all('div', class_='break-words h-10 w-full') 

    # Print the top ten product titles
    count = 0
    for container in product_containers:
        # Find the title within each product container
        title = container.find('h3', class_='block m-0 line-clamp-2 font-regular text-base leading-sm text-darkOnyx-800 pt-0.5 h-full')  # Update with the correct class name for product titles
        if title:
            title = title.text.strip()
            print(title)
            count += 1
            if count == 10:
                break

    if count == 0:
        print("Product titles not found.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the WebDriver
    driver.quit()
