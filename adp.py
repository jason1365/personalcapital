from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import os
import sys

if not "ADP_USER" in os.environ:
    sys.exit("Missing ADP_USER environment variable")
    
if not "ADP_PASS" in os.environ:
    sys.exit("Missing ADP_PASS environment variable")

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Get to ADP login page
driver.get("https://my.adp.com/static/redbox/login.html")

# the page is ajaxy so the title is originally this:
print driver.title

# find the element that's name attribute is 'user' for the form
inputElement = driver.find_element_by_name("user")
inputElement.send_keys(os.environ["ADP_USER"])

inputElement = driver.find_element_by_name("password")
inputElement.send_keys(os.environ["ADP_PASS"])

# Login to ADP
inputElement.submit()

try:
    # This is the 'Go To Pay' button
    WebDriverWait(driver, 15).until(
        #EC.presence_of_element_located((By.XPATH, '//*[@id="yourPay"]/div/pay-summary-tile/div/div[2]/div/div[5]/div/button/span'))
        EC.presence_of_element_located((By.ID, 'yourPay'))
    )

    # You should see a title !
    print driver.title

finally:
    driver.quit()