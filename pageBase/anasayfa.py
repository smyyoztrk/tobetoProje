from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait #ilgili driverı bekleten yapı
from selenium.webdriver.support import expected_conditions as ec #beklenen koşullar
from selenium.webdriver.common.action_chains import ActionChains
import pytest
import json
import openpyxl
from test_tobeto import Test_Tobeto
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

class classAnasayfa:
    def __init__(self,driver):
        self.driver= driver
    def webdriver_wait(self,sure,element):
        element=WebDriverWait(self.driver,sure).until(ec.visibility_of_element_located((By.CSS_SELECTOR,element)))
        return element
    BASLA_BUTONU = "div[class='details pack-bg-2']>button[class='btn btn-primary w-100 ']"
    def basla_butonuna_bas(self):
        basla_butonu = self.webdriver_wait(10,self.BASLA_BUTONU)
        self.driver.execute_script("arguments[0].scrollIntoView()",basla_butonu) # basla_butonu webelementi görünene kadar sayfayı aşağı kaydırdı
        sleep(3)
        #basla_butonu = WebDriverWait(self.driver,10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,self.BASLA_BUTONU)))
        basla_butonu.click()
    
