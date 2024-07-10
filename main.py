from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib

def send_email_notification():
    HOST = "smtp-mail.outlook.com"
    PORT = 587
    FROM_EMAIL = "vtgymnotifier@outlook.com"
    TO_EMAIL = "jainsidd333@gmail.com"
    MESSAGE = """Subject: VT Gym occupancy is Low

Hello, the Occupancy of the VT Gym is low so if you want to workout with minimal crowd, now is the time! Enjoy your workout,
VT Gym Notifier"""

    server = smtplib.SMTP(HOST, PORT)
    server.starttls()
    server.login(FROM_EMAIL, 'ej9LrC_?u_hKEnA')
    server.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE)
    server.quit()
    print('Email Sent Successfully')

def check_headcount():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://google.com")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    input_element = driver.find_element(By.NAME, "q")
    input_element.clear()
    input_element.send_keys("https://connect.recsports.vt.edu/facilityoccupancy" + Keys.ENTER)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Facility Occupancy"))
    )
    link = driver.find_element(By.PARTIAL_LINK_TEXT, "Facility Occupancy")
    link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-occupancy]'))
    )
    headcount_element = driver.find_element(By.CSS_SELECTOR, '[data-occupancy]')
    headcount = int(headcount_element.get_attribute('data-occupancy'))
    
    driver.quit()
    return headcount

def main():
    headcount_threshold = 50 
    headcount = check_headcount()
    print(f'Current headcount: {headcount}')
    
    if headcount < headcount_threshold:
        send_email_notification()

if __name__ == '__main__':
    main()
