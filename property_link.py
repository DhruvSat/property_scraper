import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome Drivers
driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver_win32\chromedriver.exe")
driver.maximize_window()

# X_PATHS
SEARCH_BUTTON = "//*[@id='DAPR-content']/div/div[1]/p[3]/a[1]"
LISTMORE = "//*[@id='loadmessage']/div[5]/div[1]/p/span[3]/a"
NEXT_BUTTON = "//*/ul[@class = 'pagination simple-pagination']/li/a[@class = 'page-link next']"
SHOW_MORE = "//*[@id='DAPR-content']/div/div[2]/p"
TBODY_HREF = "//*[@id='dapr']/tbody/tr/td/a[1]"

# Main URL Load
MAIN_URL = "https://plan.sa.gov.au/development_application_register"
driver.get(MAIN_URL)

# Continue on user resposne
user = input("Press 'y' or 'Y' To Continue: ")
if user == "y":

    # Find URL's From Multiple Page
    for i in range (99):
        user = input("Press 'y' or 'Y' To Continue: ")
        if user == "y":
            print(i)
            if i != 0 :
                driver.find_element(By.XPATH, NEXT_BUTTON).click()
            time.sleep(5)
            tableHref = driver.find_elements(By.XPATH, TBODY_HREF)
            for links in tableHref:
                link = links.get_attribute('href')
                with open("property_links.txt", "a") as f:
                    f.write(link+'\n')