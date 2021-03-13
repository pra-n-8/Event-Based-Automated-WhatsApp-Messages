from datetime import date
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from model import Person

def sendTextMessage(birthday_people):
    c_options = webdriver.ChromeOptions()
    c_options.add_argument("user-data-dir=C:/Users/%UserName%/AppData/Local/Google/Chrome/User Data/Default")
    driver = webdriver.Chrome(executable_path=r'G:/Projects/Python/chromedriver.exe',options=c_options)

    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 600)
    for human in birthday_people:
        group_title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div._3U29Q")))
        search = driver.find_elements_by_xpath('//*[@id="side"]/div[1]/div/label/div')[0]
        search.click()
        time.sleep(10)
        find = driver.find_elements_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')[0]
        find.send_keys(human.name)
        x_arg = '//span[@title=\''+ human.name +'\']'
        # print (x_arg)
        contact = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
        contact.click()
        message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
        if human.message :
            message.send_keys(human.message)
        else :
            message.send_keys("Happy Birthday, ", human.name,'!!')
            time.sleep(10)
        message.send_keys(Keys.RETURN)
    driver.close()
