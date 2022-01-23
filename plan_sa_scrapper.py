import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Chrome Drivers
PROXY = "103.92.114.2:443"
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver_win32\chromedriver.exe")
driver.maximize_window()

# X_PATHS
SEARCH_BUTTON = "//*[@id='DAPR-content']/div/div[1]/p[3]/a[1]"
LISTMORE = "//*[@id='loadmessage']/div[5]/div[1]/p/span[3]/a"
CONTENT = "//*[@class='full-width']"
TBODY_HREF = "//*[@id='dapr']/tbody/tr/td/a[1]"
APPLICANT = "//*[@id='applicant_details']/tbody/tr/td[1]"
PROPERTY_ADDRESS = "//*[@id='printablearea']/fieldset[3]/dl/div[1]/dd[1]"
DESCRIPTION = "//*/div[strong = 'Description']"
LODGED = "//*[@id='printablearea']/fieldset[2]/dl/div[2]/dd"
STATUS = "//*[@id='DAPR-content']/div/div[1]/span"
APPLICATION_ID = "//*[@id='printablearea']/fieldset[2]/dl/div[1]/dd"
APPLICATION_NUMBER = "//*[@id='printablearea']/fieldset[2]/dl/div[3]/dd"
COUNCIL_AREA = "//*[@id='printablearea']/fieldset[3]/dl/div[2]/dd[1]"
TITLE = "//*[@id='printablearea']/fieldset[4]/dl/div[1]/dd[1]"
PLAN_PARCEL = "//*[@id='printablearea']/fieldset[4]/dl/div[2]/dd[1]"

# CSV Header
header = ['Applicant', 'Property Address', 'Description', 'Lodged', 'Direct Link', 'Name', 'Status', 'Description', 'Application ID', 'Application number', 'Property Address', 'Council Area', 'Title', 'Plan Parcel']

# Main URL Load
MAIN_URL = "https://plan.sa.gov.au/development_application_register"
driver.get(MAIN_URL)

# Global Variables
count = 1
dataList = []
hrefList = []

# Click on More Applications
driver.find_element(By.XPATH, SEARCH_BUTTON).click()
time.sleep(15)

# Click on Load 100 Per Page Applications
driver.find_element(By.XPATH, LISTMORE).click()
time.sleep(15)

# Find URL's From Page 
tableHref = driver.find_elements(By.XPATH, TBODY_HREF)
for link in tableHref:
    links = link.get_attribute('href')
    hrefList.append(links)

# Route Through Founded Links
for url in hrefList:
    try: 
        # Route Through URL's
        driver.get(url)
        print(f"Getting data from link {count}: {url}")
        time.sleep(5)

        # Find Property Details
        applicantName = driver.find_element(By.XPATH, APPLICANT).text
        propertyAddress = driver.find_element(By.XPATH, PROPERTY_ADDRESS).text
        description = driver.find_element(By.XPATH, DESCRIPTION).text
        lodged = driver.find_element(By.XPATH, LODGED).text
        status = driver.find_element(By.XPATH, STATUS).text
        appli_ID = driver.find_element(By.XPATH, APPLICATION_ID).text
        appliNumber = driver.find_element(By.XPATH, APPLICATION_NUMBER).text
        councilArea = driver.find_element(By.XPATH, COUNCIL_AREA).text
        title = driver.find_element(By.XPATH, TITLE).text
        planParcel = driver.find_element(By.XPATH, PLAN_PARCEL).text

        desc = description.replace("Description","").replace("Show more.","").replace("\n","")

        # Create Data Object
        data = {
                'Applicant': applicantName,
                'Property Address': propertyAddress,
                'Description': desc,
                'Lodged': lodged,
                'Direct Link': url,
                'Name': propertyAddress,
                'Status': status,
                'Description': description,
                'Application ID': appli_ID,
                'Application number': appliNumber,
                'Property Address': propertyAddress,
                'Council Area': councilArea,
                'Title': title,
                'Plan Parcel': planParcel
            }

        # Append Data Object To List
        dataList.append(data)
        count += 1

    except:
        print("LINK ERROR...")
        continue

# Writing Into Csv File
with open("Applicant.csv", 'w', encoding="UTF8", newline='') as f:
    writer = csv.DictWriter(f, fieldnames= header)
    writer.writeheader()
    writer.writerows(dataList)

# Driver Quit
driver.quit()