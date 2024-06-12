import time
import csv
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# URL to scrape
base_url = "https://500.co/companies?industry=all&region=all&stage=all&country=all&bModel=all&batch=all&&page="

# Set up the Selenium WebDriver
driver = webdriver.Chrome()
companies = []

for page_number in range(1, 166):
    driver.get(f"{base_url}{page_number}")
    time.sleep(5)
    try:
        wait = WebDriverWait(driver, 20)
        div_element = wait.until(EC.presence_of_element_located((By.ID, 'companies-table')))
        logging.debug("Companies Table found")

        company_elements = div_element.find_elements(By.TAG_NAME, "a")
        logging.debug("The <a> tag is found")

        # Extract the text from each 'a' tag
        for element in company_elements:
            if element.get_attribute('href'):
                company_name = element.get_attribute("innerText").strip()
                url = element.get_attribute('href').strip(' ')

                if(company_name):
                    companies.append((company_name, url))

    except Exception as e:
        print("Error happened!", e)

driver.quit()

# Save the result to a csv file
with open('companies.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name", "URL"])
    writer.writerows(companies)

print("Data saved to companies.csv")
