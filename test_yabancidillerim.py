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
from pageBase.anasayfa import classAnasayfa
from pageBase.profilbilgilerimsayfasi import classProfilbilgilerimsayfasi 
from pageBase.kaydetButonu import ClassKaydetbutonu

class Test_yabanciDillerimClass:
    def setup_method(self):   #her test başlangıcında çalışacak fonk.
        self.driver = webdriver.Chrome()
        self.driver.get("https://tobeto.com/giris")
        self.driver.maximize_window()

    def teardown_method(self):  # her testin btiminde çalışacak fonk
        self.driver.quit()

    def webdriver_wait(self,sure,element):
        element=WebDriverWait(self.driver,sure).until(ec.visibility_of_element_located((By.CSS_SELECTOR,element)))
        return element
    def readyabancidilveriFromJson():
        file = open("yabancidil_verileri.json") 
        data = json.load(file)
        parameter = []

        for user in data['veriler']:
            dil = user["dil"]
            seviye = user["seviye"]
            
            parameter.append((dil,seviye))

        return parameter
    BEKLENEN_SONUC = "div[class='toast-body']"
    SILME_SIMGESI = "div[class='lang-edit']:nth-child(1)>span[class='delete-lang']"
    KAYITLI_DILLER_1 = "div[class='tobeto-light-bg section-p my-langs'] div[class='lang-edit']:nth-child(1)"
    HAYIR_BUTONU = "div[class='alert-buttons'] button[class='btn btn-no my-3 ']"
    EVET_BUTONU = "div[class='alert-buttons'] button[class='btn btn-yes my-3']"

    DOLDURULMASI_ZORUNLU_ALAN_DIL = "div[class='row mb-2 mt-4']>div[class='col-md-6 col-12']:nth-child(1) p[style='text-align: start; color: red;']"
    DOLDURULMASI_ZORUNLU_ALAN_SEVIYE = "div[class='row mb-2 mt-4']>div[class='col-md-6 col-12']:nth-child(2) p[style='text-align: start; color: red;']"
    @pytest.mark.parametrize("dil,seviye",readyabancidilveriFromJson())
    def test_yabanciDilBasariliKayit(self,dil,seviye):
        testTobetoClass=Test_Tobeto(self.driver)
        testTobetoClass.test_basarili_giris()
        sleep(3)
        anasayfaClass = classAnasayfa(self.driver)
        anasayfaClass.basla_butonuna_bas()
        sleep(2)
        profilbilgilerimClass = classProfilbilgilerimsayfasi(self.driver)
        profilbilgilerimClass.yabanci_dillerim_linkine_tikla()
        sleep(2)
        profilbilgilerimClass.yabanci_dil_bilgileri_doldur(dil,seviye)
        kaydetButonuClass = ClassKaydetbutonu(self.driver)
        kaydetButonuClass.kaydet_butonuna_bas()
        beklenen_sonuc = self.webdriver_wait(20,self.BEKLENEN_SONUC)
        gerceklesen_sonuc = "• Yabancı dil bilgisi eklendi."
        assert beklenen_sonuc.text == gerceklesen_sonuc
    def test_eklenen_dilin_silinmesi(self):
        testTobetoClass=Test_Tobeto(self.driver)
        testTobetoClass.test_basarili_giris()
        sleep(3)
        anasayfaClass = classAnasayfa(self.driver)
        anasayfaClass.basla_butonuna_bas()
        sleep(2)
        profilbilgilerimClass = classProfilbilgilerimsayfasi(self.driver)
        profilbilgilerimClass.yabanci_dillerim_linkine_tikla()
        sleep(2)
        profilbilgilerimClass.cop_kutusu_simgesine_tikla()
        sleep(2)
        profilbilgilerimClass.hayir_butonuna_tikla_yabanci_dillerim()
        assert profilbilgilerimClass.diller_sayfada_duruyor_mu() == True
        profilbilgilerimClass.cop_kutusu_simgesine_tikla()
        profilbilgilerimClass.evet_butonuna_tikla_yabanci_dillerim()
        beklenen_sonuc = self.webdriver_wait(20,self.BEKLENEN_SONUC)
        assert beklenen_sonuc.text == "• Yabancı dil kaldırıldı."
    def test_yabanci_dil_ekleme_basarisiz(self):
        testTobetoClass=Test_Tobeto(self.driver)
        testTobetoClass.test_basarili_giris()
        sleep(3)
        anasayfaClass = classAnasayfa(self.driver)
        anasayfaClass.basla_butonuna_bas()
        sleep(2)
        profilbilgilerimClass = classProfilbilgilerimsayfasi(self.driver)
        profilbilgilerimClass.yabanci_dillerim_linkine_tikla()
        sleep(2)
        kaydetButonuClass = ClassKaydetbutonu(self.driver)
        kaydetButonuClass.kaydet_butonuna_bas()
        doldurulmasi_zorunlu_alan_dil = self.webdriver_wait(10,self.DOLDURULMASI_ZORUNLU_ALAN_DIL)
        doldurulmasi_zorunlu_alan_seviye = self.webdriver_wait(10,self.DOLDURULMASI_ZORUNLU_ALAN_DIL)
        assert doldurulmasi_zorunlu_alan_dil.text == "Doldurulması zorunlu alan*"
        assert doldurulmasi_zorunlu_alan_seviye.text == "Doldurulması zorunlu alan*"
        


        

        
        


