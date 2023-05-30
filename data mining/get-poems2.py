from xmlrpc.client import boolean
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
PATH = "C:\Program Files (x86)\chromedriver.exe"
path=f'C:\\Users\\yukse\\OneDrive\\Masaüstü\\siirler\\'
driver= webdriver.Chrome(PATH)
Tr2Eng = str.maketrans("âçğöşüı", "acgosui")
def cleanList(text):
    text=re.sub(r',.*', '', text)
    text=re.sub(r'\(.*', '', text)
    text=text.rstrip()
    text=text.replace(" ","-")
    text=text.replace("İ","i")
    return text

denemee=[]
url = "https://siir.sitesi.web.tr/"
newUrl = url

with open('poetList2') as f:
    poetList=[line.split()[-1] for line in f]

for e in poetList:
    try:  
        i=1
        newUrl=url+ (e) + '/'
        txt=open(os.path.join(path, e), "w")
        driver.get(newUrl)
        time.sleep(0.5)
        deneme = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div/div/div[3]/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/table/tbody/tr')
        poems=deneme.find_elements(By.TAG_NAME,'a')
        for m in poems:
            denemee.append(m.get_attribute("href"))
        
        for y in denemee:
            driver.get(y)
            time.sleep(0.5)
            poem=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.CLASS_NAME,'text'))
            )
            poemTitle=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/div/div/div[3]/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div[1]/div[1]/h3/a'))
            )
            txt.write(i + '- ' + poemTitle.text + '\n')
            txt.write(poem.text + '\n')
            txt.write('******************** + \n')
            i+=1
            time.sleep(1)
    except:
        pass
    denemee.clear()
    
