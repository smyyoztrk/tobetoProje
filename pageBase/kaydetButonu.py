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

class ClassKaydetbutonu:
    def __init__(self,driver):
        self.driver= driver
    def webdriver_wait(self,sure,element):
        element=WebDriverWait(self.driver,sure).until(ec.visibility_of_element_located((By.CSS_SELECTOR,element)))
        return element
    
    KAYDET_BUTONU = "button[class='btn btn-primary py-2 mb-3 d-inline-block mobil-btn']"
    BEKLENEN_SONUC = "div[class='toast-body']"

    def kaydet_butonuna_bas(self):
        
        kaydet_butonu= self.webdriver_wait(20,self.KAYDET_BUTONU)
        kaydet_butonu.click()
        # sleep(2)
        # beklenen_sonuc = self.webdriver_wait(10,self.BEKLENEN_SONUC)
        # # gerceklesen_sonuc = "• Eğitim bilgisi eklendi."
        # assert beklenen_sonuc.text == gerceklesen_sonuc