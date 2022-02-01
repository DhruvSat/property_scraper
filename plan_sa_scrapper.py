import csv
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

# Chrome Drivers
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
TITLE1 = "//*[@id='printablearea']/fieldset[4]/dl/div[1]/dd[1]"
TITLE2 = "//*[@id='printablearea']/fieldset[4]/dl/div[1]/dd[2]"
PLAN_PARCEL1 = "//*[@id='printablearea']/fieldset[4]/dl/div[2]/dd[1]"
PLAN_PARCEL2 = "//*[@id='printablearea']/fieldset[4]/dl/div[2]/dd[2]"
NEXT_BUTTON = "//*/ul[@class = 'pagination simple-pagination']/li/a[@class = 'page-link next']"
SHOW_MORE = "//*[@id='DAPR-content']/div/div[2]/p"

# CSV Header
header = ['Applicant', 'Property Address', 'Description', 'Lodged', 'Direct Link', 'Name', 'Status', 'Descrip', 'Application ID', 'Application number', 'Property Addr', 'Council Area', 'Title', 'Plan Parcel']

# Global Variables
count = 1
dataList = []
hrefList = []

listOfLinks = [line.strip() for line in open('property_links.txt')]
print(len(listOfLinks))

# links = ['https://plan.sa.gov.au/development_application_register#view-21035707-DAP', 'https://plan.sa.gov.au/development_application_register#view-21035173-DAP','https://plan.sa.gov.au/development_application_register#view-21035173-DAP']

# Route Through Founded Links
for url in listOfLinks:
    try: 
        # Route Through URL's
        driver.get(url)
        print(f"Getting data from link {count}: {url}")
        time.sleep(7)

        # Click on Show More Description if available
        try:
            driver.find_element(By.XPATH, SHOW_MORE).click()
            time.sleep(1)
        except:
            pass

        # Find Property Details
        try: 
            applicantName = driver.find_element(By.XPATH, APPLICANT).text
        except:
            applicantName = ""
        try:
            propertyAddress = driver.find_element(By.XPATH, PROPERTY_ADDRESS).text
        except:
            propertyAddress = ""
        try:
            description = driver.find_element(By.XPATH, DESCRIPTION).text
        except:
            description = ""
        try:
            lodged = driver.find_element(By.XPATH, LODGED).text
        except:
            lodged = ""
        try:
            status = driver.find_element(By.XPATH, STATUS).text
        except: 
            status = ""
        try: 
            appli_ID = driver.find_element(By.XPATH, APPLICATION_ID).text
        except:
            appli_ID = ""
        try:     
            appliNumber = driver.find_element(By.XPATH, APPLICATION_NUMBER).text
        except:
            appliNumber = ""
        try:
            councilArea = driver.find_element(By.XPATH, COUNCIL_AREA).text
        except:
            councilArea = ""
        try: 
            title = driver.find_element(By.XPATH, TITLE1).text
            if len(title) > 3:
                title = title
            else:
                title = driver.find_element(By.XPATH, TITLE2).text
        except:
            title = ""
        try:
            planParcel = driver.find_element(By.XPATH, PLAN_PARCEL1).text
            if len(planParcel) > 3:
                planParcel = planParcel
            else:
                planParcel = driver.find_element(By.XPATH, PLAN_PARCEL2).text
        except:
            planParcel = ""

        # Create Data Object
        data = {
                'Applicant': applicantName,
                'Property Address': propertyAddress,
                'Description': description,
                'Lodged': lodged,
                'Direct Link': url,
                'Name': propertyAddress,
                'Status': status,
                'Descrip': description,
                'Application ID': appli_ID,
                'Application number': appliNumber,
                'Property Addr': propertyAddress,
                'Council Area': councilArea,
                'Title': title,
                'Plan Parcel': planParcel
            }

        # Append Data Object To List
        dataList.append(data)
        count += 1
        dataObject = json.dumps(dataList)   
            
        # Saving Data into .json file
        with open("Property2.json", "w") as outfile:
            outfile.write(dataObject)

    except:
        print("LINK ERROR...")
        count += 1
        continue

# Writing Into Csv File
with open("Applicant2.csv", 'w', encoding="UTF8", newline='') as f:
    writer = csv.DictWriter(f, fieldnames= header)
    writer.writeheader()
    writer.writerows(dataList)

# Driver Quit
driver.quit()