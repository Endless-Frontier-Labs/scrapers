'''
This program is for scrapping the Y Combinator site for information about startups from the S24 and W24
batch. Site structure can change in the future and code will need to be modified. This version deals with 
a site that has company info cards which load in batches on scroll - need to scroll to the bottom to load 
all cards. To get the website link we navigate to the company information page. Code can be adapted for 
other websites with similar structure by changing the relevant class names.
'''

import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
# Set up the Selenium webdriver
driver = webdriver.Chrome()

# Open the webpage
url = "https://www.ycombinator.com/companies?batch=S24&batch=W24"
driver.get(url)


# Find the div element with class name "table-rows"
div_element = driver.find_element(By.CLASS_NAME,"_rightCol_99gj3_576")

# Prepare the data to be saved as a CSV
data = []
last_height = driver.execute_script("return document.body.scrollHeight")

# Scroll the entire page to load all companies
while True:

    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load the page
    time.sleep(2)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # Break the loop if no new content is loaded
    last_height = new_height
    
# Find all the company elements within the div element
wait = WebDriverWait(driver, 10)
company_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_company_99gj3_339")))

# Scrape each company in the list
for company_element in company_elements:
    # Extract company name
    company_name = company_element.find_element(By.CLASS_NAME,"_coName_99gj3_454").text.strip()
    # Extract Description
    company_description = company_element.find_element(By.CLASS_NAME,"_coDescription_99gj3_479").text.strip()
    # Extract Industry
    industry_elements = company_element.find_elements(By.CSS_SELECTOR, "a._tagLink_99gj3_1024 span.pill")
    industries = [industry.text for industry in industry_elements if industry.text not in ('S24', 'W24')] 

    href_link = company_element.get_attribute("href")

    # Navigate to Company page
    driver.get(href_link)
    try:

        # XPath to find the link element
        link_xpath = "//div[@class='group flex flex-row items-center px-3 leading-none text-linkColor ']//a"

        # Find the link element using XPath
        link_element = driver.find_element(By.XPATH, link_xpath)

        # Extract the website link from the 'href' attribute
        website = link_element.get_attribute("href")

    # Handle Missing links
    except StaleElementReferenceException:
        website = ''
        
    # Navigate back to the original page
    driver.back()

    # Append the extracted data to the list
    data.append([company_name, website, company_description, ', '.join(industries)])

# Save the data as a CSV file
csv_file = "company_data.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name", "Website", "Description", "Industries"])  # Write header row
    writer.writerows(data)  # Write data rows

# Close the webdriver
driver.quit()