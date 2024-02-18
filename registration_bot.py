import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

CRN = input("Enter CRN of course you want to add: ")
EMAIL = input("Enter your email: ")
SENDER_PASSWORD = input("Enter your sender password (it is different from your email password, google it!): ")
SU_USERNAME = input("Enter your SU username: ")
SU_PASSWORD = input("Enter your SU password: ")
remaining = 0
while(remaining == 0):
    try:
        url = "https://suis.sabanciuniv.edu/prod/bwckschd.p_disp_detail_sched?term_in=202302&crn_in=" + CRN

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        html_content = ""
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print("CS449 Title of the page:", soup.title.text)
            html_content = (soup.prettify())
        else:
            print("Failed to retrieve the page. Status code:", response.status_code)


        soup = BeautifulSoup(html_content, 'html.parser')

        target_table = soup.find('table', {'class': 'datadisplaytable', 'summary': 'This layout table is used to present the seating numbers.'})

        if target_table:
            print("Table is found.")
        else:
            print("Table not found.")



        target = target_table.find('tr').find('tr').find_all('td')[2].text

        remaining = int(target)
        print(remaining)
        print(datetime.now())
        #time.sleep(1)
    except:
        continue



# Email configuration
sender_email = EMAIL
sender_password = SENDER_PASSWORD
recipient_email = EMAIL
subject = "Remaining place in" + CRN
body = str(remaining) + " yer kaldı!"

# Compose the email
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = recipient_email
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

# Establish a connection to the SMTP server (in this case, Gmail's SMTP server)
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()  # Enable TLS
    server.login(sender_email, sender_password)
    
    # Send the email
    server.sendmail(sender_email, recipient_email, message.as_string())

print("Email sent successfully!")









while(remaining>0):
    try:
        username = SU_USERNAME
        password = SU_PASSWORD
        url = 'https://suis.sabanciuniv.edu/prod/twbkwbis.P_SabanciLogin'
        

        driver = webdriver.Chrome()
        driver.implicitly_wait(60)
        # Open the website
        driver.get(url)
        username_input = driver.find_element('name', 'sid')
        password_input = driver.find_element('name', 'PIN')

        username_input.send_keys(username)
        password_input.send_keys(password)
        # Submit the form
        password_input.submit()
        #driver.implicitly_wait(100)
        xpath = "/html/body/div[1]/div[2]/span/map/table/tbody/tr[1]/td/table/tbody/tr/td[3]/a"
        element = driver.find_element("xpath", xpath)
        element.click()

        xpath = "/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a"
        element = driver.find_element("xpath", xpath)
        element.click()

        xpath = "/html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a"
        element = driver.find_element("xpath", xpath)
        element.click()


        xpath = "/html/body/div[3]/form/input"
        element = driver.find_element("xpath", xpath)
        element.click()

        xpath = '/html/body/div[3]/form/table/tbody/tr[2]/td[1]/input[@name="CRN_IN"]'
        crn_input = driver.find_element(By.XPATH, xpath)
        crn_input.clear()
        crn_input.send_keys(CRN)

        xpath = "/html/body/div[3]/form/input[19]"
        element = driver.find_element("xpath", xpath)
        element.click()
    except:
        driver.quit()
        continue

    input("Press Enter to close the browser...")
    driver.quit()
    break


