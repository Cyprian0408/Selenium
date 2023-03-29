import os 
import numpy as np
import pandas as pd
import csv
import time
import math

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def web_scraping(floor):
    temp=[[0 for x in range(6)] for y in range(36)]
    data=temp
    start_time=time.time()
    #pobranie liczby iteracji
    temporary="https://www.domiporta.pl/mieszkanie/sprzedam/mazowieckie/warszawa?"+"Pietro.From="+str(floor)+"&Pietro.To="+str(floor)+"&Rynek=Wtorny"
    driver = webdriver.Firefox()
    driver.get(temporary)
    #poczekanie na pojawienie się okna akceptacji plików cookies
    try:
        elem=WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.ID,'onetrust-accept-btn-handler'))).click()
    finally: 
        driver.maximize_window()
    lim_string=driver.find_element(By.XPATH,'.//span[@class="search__button-counter"]').text
    driver.close()
    lim_temp_string=lim_string.replace(",","")
    lim=int(lim_temp_string)
    print("Dla piętra nr",floor,"znaleziono ",lim,' ofert')
  
    #rozpoczęcie procesu gromadzenia danych
    for i in range(math.ceil(lim/36)-1):
        if i==0:
            #string="https://www.domiporta.pl/mieszkanie/sprzedam/mazowieckie/warszawa?Rynek=Wtorny"
            string="https://www.domiporta.pl/mieszkanie/sprzedam/mazowieckie/warszawa?"+"Pietro.From="+str(floor)+"&Pietro.To="+str(floor)+"&Rynek=Wtorny"
        else:
            #string="https://www.domiporta.pl/mieszkanie/sprzedam/mazowieckie/warszawa?Rynek=Wtorny"
            string="https://www.domiporta.pl/mieszkanie/sprzedam/mazowieckie/warszawa?"+"Pietro.From="+str(floor)+"&Pietro.To="+str(floor)+"&Rynek=Wtorny"
            p2="&PageNumber="
            p3=str(i+1)
            string=string+p2+p3
        #otworzenie okna firefox
        driver = webdriver.Firefox()
        driver.get(string)
        #poczekanie na pojawienie się okna akceptacji plików cookies
        try:
            elem=WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.ID,'onetrust-accept-btn-handler'))).click()
        finally: 
            driver.maximize_window()
        list=driver.find_elements(By.XPATH,'/html/body/div[1]/main/div[2]/div/div/div/div[1]/div[2]/div[1]/ul')
        pow=[]
        num=[]
        prices=[]
        prices_per_sqm=[]
        addresses=[]
        descriptions=[]
        for n in list:
            #możliwe rozwiązanie - wypisze wszystko na stronie 
            #print(n.text)
            #pozyskanie powierzchni mieszkania
            area=driver.find_elements(By.XPATH,'.//span[@class="sneakpeak__details_item sneakpeak__details_item--area"]')
            for value in area:
                pow+=[value.text]
            #pozyskanie liczby pokoi
            number_of_rooms=driver.find_elements(By.XPATH,'.//span[@class="sneakpeak__details_item sneakpeak__details_item--room"]')
            for value in number_of_rooms:
                num+=[value.text]
            #pozyskanie ceny za metr kwadratowy mieszkania
            price_per_sqm=driver.find_elements(By.XPATH,'.//span[@class="sneakpeak__details_item sneakpeak__details_item--price"]')
            for value in price_per_sqm:
                prices_per_sqm+=[value.text]
            #pozyskanie adresu mieszkania
            address=driver.find_elements(By.XPATH,'.//span[@class="sneakpeak__title--inblock"]')
            for value in address:
                addresses+=[value.text]
            #pozyskanie ceny całkowitej za mieszkanie
            sum=driver.find_elements(By.XPATH,'.//span[@class="sneakpeak__price_value"]')
            for value in sum:
                prices+=[value.text]
            #pozyskanie krókiego opisu mieszkania
            desc=driver.find_elements(By.XPATH,'.//p[@class="sneakpeak__description"]')
            for value in desc:
                descriptions+=[value.text]

        #usunięcie białych znaków jako elementów tablicy
        while '' in prices:
            prices.remove('')
        while '' in num:
            num.remove('')
        while '' in pow:
            pow.remove('')
        while '' in prices_per_sqm:
            prices_per_sqm.remove('')
        while '' in addresses:
            addresses.remove('')
        while '' in descriptions:
            descriptions.remove('')

        #usunięcie znaków nowej linii z komórek tablicy
        p_rices=[]
        for val in prices:
            p_rices.append(val.replace("\n",""))
        n_umber_of_rooms=[]
        for val in num:
            n_umber_of_rooms.append(val.replace("\n",""))
        p_ow=[]
        for val in pow:
            p_ow.append(val.replace("\n",""))
        p_rice_per_sqm=[]
        for val in prices_per_sqm:
            p_rice_per_sqm.append(val.replace("\n",""))

        #stworzenie z wektorów danych kolumn tablicy wielowymiarowej

        if i==0:
            if len(addresses)!=36 or len(p_rices)!=36 or len(p_ow)!=36 or len(n_umber_of_rooms)!=36 or len(descriptions)!=36 or len(p_rice_per_sqm)!=36:
                driver.close()
                continue
            else:
                results=np.column_stack((addresses,p_rices,p_rice_per_sqm ,p_ow,n_umber_of_rooms,descriptions))
                data=results
                driver.close()
        else:
            if len(addresses)!=36 or len(p_rices)!=36 or len(p_ow)!=36 or len(n_umber_of_rooms)!=36 or len(descriptions)!=36 or len(p_rice_per_sqm)!=36:
                driver.close()
                continue
            else:
                temp=data
                results=np.column_stack((addresses,p_rices,p_rice_per_sqm ,p_ow,n_umber_of_rooms,descriptions))
                if results.shape[0]==36:
                    data=np.row_stack((temp,results))
                    driver.close()
                else:
                    driver.close()
                    continue
                
    import xlsxwriter
    file_name="Data"+str(floor)+".xlsx"
    Workbook=xlsxwriter.Workbook(file_name)
    worksheet=Workbook.add_worksheet()
    col=0
    for row, i in enumerate(data):
        worksheet.write_row(row,col,i)
    Workbook.close()        
