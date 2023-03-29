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

def walkscore_function(file_number):
    start_time=time.time()
    #stworzenie tablicy z pierwszej kolumny pliku excelowego
    file_name='Data'+str(file_number)+'.xlsx'
    df=pd.read_excel(file_name,sheet_name='Sheet1')
    addresses=df[df.columns[0]].to_list()
    #zainicjowanie tablicy, która będzie przechowywała wyniki ze strony walkscore
    walkscore=[]
    print(len(addresses))
    #i=0
    #otwieranie okien w pętli i pobieranie danych do tablicy
    for address in addresses:
        temp_string=address
        site="https://www.walkscore.com/score/"+temp_string
        driver=webdriver.Firefox()
        driver.get(site)
        try:
            WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/div/div[3]/div[3]/div[1]/div/div/img')))
        finally:
            driver.maximize_window()
        element=driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[3]/div[3]/div[1]/div/div/img')
        temp=element.get_attribute('alt')
        score=temp.split(' ', 1)[0]
        walkscore+=[score]
        driver.close()
        #i+=1
        #if i>2:
        #    break
    print(walkscore)

    #zapis danych do utworzonych uprzednio plików excelowych, w drugiej zakładce
    df=pd.DataFrame(walkscore)
    writer=pd.ExcelWriter(file_name,mode='a',engine='openpyxl', if_sheet_exists='replace')
    print("Saving")
    df.to_excel(writer,sheet_name='Sheet2', index=False)
    print("Saved")
    writer.close()
    end_time=time.time()
    process_time=end_time-start_time
    print("Czas procesu to: "+str(process_time)+" [s]")
    print("Przewidywany czas trwania całego procesu w godzinach"+str(file_number)+": "+str(process_time/3*len(addresses)/3600))