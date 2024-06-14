import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Specify the path to the ChromeDriver
chrome_driver_path = 'C:\\Users\\Medha Agarwal\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe'

# Initialize the ChromeDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# CSV file to store the data
csv_file_path = 'product_details.csv'

try:
    # Open the BigBasket website
    url = "https://www.bigbasket.com/member/sb/?nc=smart_basket"
    driver.get(url)

    # Allow the page to load
    time.sleep(5)

    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Quantity', 'Price', 'Discount'])  # Write the header row

        last_height = driver.execute_script("return document.body.scrollHeight") - 500
        
        while True:
            # Scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait to allow the page to load
            time.sleep(5)
            
            # Get the new page source after scrolling
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            # Find all product container elements
            product_containers = soup.find_all('div', class_='SKUDeck___StyledDiv-sc-1e5d9gk-0 eA-dmzP')
            
            # Extract and write product details
            for container in product_containers:
                title_div = container.find('h3', class_='block m-0 line-clamp-2 font-regular text-base leading-sm text-darkOnyx-800 pt-0.5 h-full')
                price_div = container.find('span', class_='Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi')
                qty_div = container.find('span', class_='Label-sc-15v1nk5-0 PackChanger___StyledLabel-sc-newjpv-1 gJxZPQ cWbtUx')
                disc_div = container.find('span', class_='font-semibold lg:text-xs xl:text-sm leading-xxl xl:leading-md')
                
                if title_div:
                    title = title_div.text.strip()
                    price = price_div.text.strip() if price_div else "Price not available"
                    qty = qty_div.text.strip() if qty_div else "Quantity not available"
                    discount = disc_div.text.strip() if disc_div else "Discount not available"
                    
                    writer.writerow([title, qty, price, discount])
                    print(f"Title: {title}, Quantity: {qty}, Price: {price}, Discount: {discount}")

            # Check if we've reached the bottom of the page
            new_height = driver.execute_script("return document.body.scrollHeight") - 500
            if new_height == last_height:
                break
            last_height = new_height

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the WebDriver
    driver.quit()
