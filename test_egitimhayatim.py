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
class Test_egitimHayatimClass:
    
    
    def setup_method(self):   #her test başlangıcında çalışacak fonk.
        self.driver = webdriver.Chrome()
        self.driver.get("https://tobeto.com/giris")
        self.driver.maximize_window()

    def teardown_method(self):  # her testin btiminde çalışacak fonk
        self.driver.quit()

    def webdriver_wait(self,sure,element):
        element=WebDriverWait(self.driver,sure).until(ec.visibility_of_element_located((By.CSS_SELECTOR,element)))
        return element
    
    def readbasariliegitimveriFromJson():
        file = open("basarili_egitim_verileri.json") 
        data = json.load(file)
        parameter = []

        for user in data['veriler']:
            egitim_duzeyi = user["egitim_duzeyi"]
            okul = user["okul"]
            bolum = user["bolum"]
            baslangic_yili =user["baslangic_yili"]
            mezuniyet_yili = user["mezuniyet_yili"]
            parameter.append((egitim_duzeyi,okul,bolum,baslangic_yili,mezuniyet_yili))

        return parameter
    def readdevamediyorumveriFromJson():
        file = open("devam_ediyorum_verileri.json") 
        data = json.load(file)
        parameter = []

        for user in data['veriler']:
            egitim_duzeyi = user["egitim_duzeyi"]
            okul = user["okul"]
            bolum = user["bolum"]
            baslangic_yili =user["baslangic_yili"]
            parameter.append((egitim_duzeyi,okul,bolum,baslangic_yili))

        return parameter

    BEKLENEN_SONUC = "div[class='toast-body']"

    @pytest.mark.parametrize("egitim_duzeyi,okul,bolum,baslangic_yili,mezuniyet_yili",readbasariliegitimveriFromJson())
    def test_egitimHayatim_basarili_kayit(self,egitim_duzeyi,okul,bolum,baslangic_yili,mezuniyet_yili,gerceklesen_sonuc="• Eğitim bilgisi eklendi."):
        testTobetoClass=Test_Tobeto(self.driver)
        testTobetoClass.test_basarili_giris()
        sleep(3)
        anasayfaClass = classAnasayfa(self.driver)
        anasayfaClass.basla_butonuna_bas()
        sleep(2)
        profilbilgilerimClass = classProfilbilgilerimsayfasi(self.driver)
        profilbilgilerimClass.egitim_hayatim_linkine_tikla()
        profilbilgilerimClass.egitim_bilgilerini_doldur(egitim_duzeyi,okul,bolum,baslangic_yili,mezuniyet_yili)
        sleep(2)

        kaydetButonuClass = ClassKaydetbutonu(self.driver)
        kaydetButonuClass.kaydet_butonuna_bas()
        beklenen_sonuc = self.webdriver_wait(10,self.BEKLENEN_SONUC)
        # gerceklesen_sonuc = "• Eğitim bilgisi eklendi."
        assert beklenen_sonuc.text == gerceklesen_sonuc

    @pytest.mark.parametrize("egitim_duzeyi,okul,bolum,baslangic_yili",readdevamediyorumveriFromJson())
    def test_devam_ediyorum_sec_ile_kayit(self,egitim_duzeyi,okul,bolum,baslangic_yili,gerceklesen_sonuc="• Eğitim bilgisi eklendi."):
        testTobetoClass=Test_Tobeto(self.driver)
        testTobetoClass.test_basarili_giris()
        sleep(3)

        anasayfaClass = classAnasayfa(self.driver)
        anasayfaClass.basla_butonuna_bas()
        sleep(2)
        profilbilgilerimClass = classProfilbilgilerimsayfasi(self.driver)
        profilbilgilerimClass.egitim_hayatim_linkine_tikla()
        profilbilgilerimClass.devam_ediyorum_egitim_bilgileri(egitim_duzeyi,okul,bolum,baslangic_yili)
        sleep(2)

        kaydetButonuClass = ClassKaydetbutonu(self.driver)
        kaydetButonuClass.kaydet_butonuna_bas()
        beklenen_sonuc = self.webdriver_wait(10,self.BEKLENEN_SONUC)
        # gerceklesen_sonuc = "• Eğitim bilgisi eklendi."
        assert beklenen_sonuc.text == gerceklesen_sonuc

    def test_alanlar_bos_birakilarak_basarisiz_kayit(self,gerceklesen_sonuc="Doldurulması zorunlu alan*"):
        testTobetoClass=Test_Tobeto(self.driver)
        testTobetoClass.test_basarili_giris()
        sleep(3)

        anasayfaClass = classAnasayfa(self.driver)
        anasayfaClass.basla_butonuna_bas()
        sleep(2)

        profilbilgilerimClass = classProfilbilgilerimsayfasi(self.driver)
        profilbilgilerimClass.egitim_hayatim_linkine_tikla()

        kaydetButonuClass = ClassKaydetbutonu(self.driver)
        kaydetButonuClass.kaydet_butonuna_bas()

        beklenen_sonuc = WebDriverWait(self.driver,20).until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR,"span[class='text-danger']")))
        sleep(1)
        for i in beklenen_sonuc:
            i=beklenen_sonuc[0]
            assert i.text == gerceklesen_sonuc







        
        

        
       
        
       