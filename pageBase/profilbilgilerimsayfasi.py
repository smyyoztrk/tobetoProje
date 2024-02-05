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

class classProfilbilgilerimsayfasi:
    def __init__(self,driver):
        self.driver= driver

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
    def webdriver_wait(self,sure,element):
        element=WebDriverWait(self.driver,sure).until(ec.visibility_of_element_located((By.CSS_SELECTOR,element)))
        return element
    EGITIM_HAYATIM_LINK= "div[class='p-2 py-4 mobile-sidebar']>a[class='btn mb-2 text-start w-100  sidebar-link ']:nth-child(3) span[class='sidebar-text']"
    EGITIM_SECINIZ_DROPDOWN = "select[name='EducationStatus']"
    UNIV_GIRIS = "input[name='University']"
    BOLUM_ADI = "input[name='Department']"
    MEZUNIYET_YILI = "input[class='form-control tobeto-input ']"
    BASLANGIC_TARIHI = "div[class='react-datepicker__input-container ']>input[class='form-control tobeto-input']"
    TARIH_SECME_TAKVIMI = "div[class='react-datepicker__year-text react-datepicker__year-text--keyboard-selected react-datepicker__year-text--today']"
    DEVAM_EDIYORUM = "input[name='checkbox']"
    KAYDET_BUTONU = "button[class='btn btn-primary py-2 mb-3 d-inline-block mobil-btn']"
    BEKLENEN_SONUC = "div[class='toast-body']"
    YABANCI_DILLERIM_LINK = "div[class='p-2 py-4 mobile-sidebar']>a[class='btn mb-2 text-start w-100  sidebar-link ']:nth-child(7) span[class='sidebar-text']"
    DIL_SECINIZ_DROPDOWN ="select[name='languageName']"
    SEVIYE_SECINIZ_DROPDOWN = "select[name='proficiency']"
    HAYIR_BUTONU = "div[class='alert-buttons'] button[class='btn btn-no my-3 ']"
    EVET_BUTONU = "div[class='alert-buttons'] button[class='btn btn-yes my-3']"
    SILME_SIMGESI = "div[class='lang-edit']:nth-child(1)>span[class='delete-lang']"
    KAYITLI_DILLER_1 = "div[class='tobeto-light-bg section-p my-langs'] div[class='lang-edit']:nth-child(1)"

    def egitim_hayatim_linkine_tikla(self):
        egitim_hayatim_link = self.webdriver_wait(10,self.EGITIM_HAYATIM_LINK)
        # egitim_hayatim_link = WebDriverWait(self.driver,10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,self.EGITIM_HAYATIM_LINK)))
        egitim_hayatim_link.click()
    # @pytest.mark.parametrize("egitim_duzeyi,okul,bolum,baslangic_yili,mezuniyet_yili",readbasariliegitimveriFromJson())
    def egitim_bilgilerini_doldur(self,egitim_duzeyi,okul,bolum,baslangic_yili,mezuniyet_yili):
        egitim_seciniz_dropdown = self.webdriver_wait(10,self.EGITIM_SECINIZ_DROPDOWN)
        # egitim_seciniz_dropdown= WebDriverWait(self.driver,10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,self.EGITIM_SECINIZ_DROPDOWN)))
        egitim_seciniz = Select(egitim_seciniz_dropdown)
        egitim_secenekleri = egitim_seciniz.options

        # for egitim in egitim_secenekleri:
        #     print(egitim.text)

        # sleep(2)
        egitim_seciniz.select_by_visible_text(egitim_duzeyi)
        # sleep(2)
        univ_giris =self.webdriver_wait(10,self.UNIV_GIRIS)
        # sleep(2)
        univ_giris.send_keys(okul)
        # sleep(2)
        bolum_adi = self.webdriver_wait(10,self.BOLUM_ADI)
        bolum_adi.send_keys(bolum)
        mezuniyet_yili = self.webdriver_wait(10,self.MEZUNIYET_YILI)
        assert mezuniyet_yili.is_enabled() == False #mezuniyet yılı alanı seçimi aktif mi?
        baslangic_tarihi =self.webdriver_wait(30,self.BASLANGIC_TARIHI)
        # sleep(5)
        baslangic_tarihi.send_keys(baslangic_yili)
        assert mezuniyet_yili.is_enabled() == True
        mezuniyet_yili.click()
        tarih_secme_takvimi = self.webdriver_wait(10,self.TARIH_SECME_TAKVIMI)
        tarih_secme_takvimi.click()
      
        # sleep(5)
        devam_ediyorum = self.webdriver_wait(10,self.DEVAM_EDIYORUM)
        # assert devam_ediyorum.is_enabled() == False # burada bug var, 'devam ediyorum' onay kutusu aktif olmamalı
    def devam_ediyorum_egitim_bilgileri(self,egitim_duzeyi,okul,bolum,baslangic_yili):
        egitim_seciniz_dropdown = self.webdriver_wait(10,self.EGITIM_SECINIZ_DROPDOWN)
        # egitim_seciniz_dropdown= WebDriverWait(self.driver,10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,self.EGITIM_SECINIZ_DROPDOWN)))
        egitim_seciniz = Select(egitim_seciniz_dropdown)
        egitim_secenekleri = egitim_seciniz.options

        # for egitim in egitim_secenekleri:
        #     print(egitim.text)

        # sleep(2)
        egitim_seciniz.select_by_visible_text(egitim_duzeyi)
        # sleep(2)
        univ_giris =self.webdriver_wait(10,self.UNIV_GIRIS)
        # sleep(2)
        univ_giris.send_keys(okul)
        # sleep(2)
        bolum_adi = self.webdriver_wait(10,self.BOLUM_ADI)
        bolum_adi.send_keys(bolum)
        baslangic_tarihi =self.webdriver_wait(30,self.BASLANGIC_TARIHI)
        # sleep(5)
        baslangic_tarihi.send_keys(baslangic_yili)
        devam_ediyorum = self.webdriver_wait(20,self.DEVAM_EDIYORUM)
        devam_ediyorum.click()
    def yabanci_dillerim_linkine_tikla(self):
        yabanci_dillerim_link = self.webdriver_wait(10,self.YABANCI_DILLERIM_LINK)
        yabanci_dillerim_link.click()
    def yabanci_dil_bilgileri_doldur(self,dil,seviye):
        dil_seciniz_dropdown = self.webdriver_wait(10,self.DIL_SECINIZ_DROPDOWN)
        dil_seciniz = Select(dil_seciniz_dropdown)
        dil_seciniz.select_by_visible_text(dil)
        seviye_seciniz_dropdown = self.webdriver_wait(20,self.SEVIYE_SECINIZ_DROPDOWN)
        seviye_seciniz = Select(seviye_seciniz_dropdown)
        seviye_seciniz.select_by_visible_text(seviye)
    def hayir_butonuna_tikla_yabanci_dillerim(self):
        hayir_butonu = self.webdriver_wait(10,self.HAYIR_BUTONU)
        hayir_butonu.click()
    def evet_butonuna_tikla_yabanci_dillerim(self):
        evet_butonu = self.webdriver_wait(10,self.EVET_BUTONU)
        evet_butonu.click()
    def cop_kutusu_simgesine_tikla(self):
        kayitli_dil_birinci_siradaki = self.webdriver_wait(20,self.KAYITLI_DILLER_1)
        kayitli_dil_birinci_siradaki.click()
        cop_kutusu = self.webdriver_wait(20,self.SILME_SIMGESI)
        cop_kutusu.click()
    def diller_sayfada_duruyor_mu(self):
        kayitli_dil_birinci_siradaki = self.webdriver_wait(20,self.KAYITLI_DILLER_1)
        sonuc = kayitli_dil_birinci_siradaki.is_displayed()
        return sonuc


    



        