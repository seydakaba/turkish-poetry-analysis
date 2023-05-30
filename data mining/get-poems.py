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
driver= webdriver.Chrome(PATH)
driver.implicitly_wait(5)

Tr2Eng = str.maketrans("âçğöşüı", "acgosui")
poetList=[]
path=f'C:\\Users\\yukse\\OneDrive\\Masaüstü\\siirler'
if not os.path.exists(path):
    os.makedirs(path)

def cleanList(text):
    text=text.replace("(Ran)","Ran")
    text=re.sub(r',.*', '', text)
    text=re.sub(r'\(.*', '', text)
    text=text.rstrip()
    text=text.replace(" ","-")
    text=text.replace("İ","i")
    return text

def pageCheck():
    try:
        return(boolean(driver.find_element(By.CLASS_NAME,'title-404')))
    except:
        return False

def getPoemCount():
    poemCount=driver.find_element(By.CSS_SELECTOR,'div.content > div:nth-child(3) > div.poet-bar > div.pb-detail > div.pbd-poems')
    poemCountText=poemCount.text
    poemCountText=poemCountText=re.sub(r'\s.*','',str(poemCountText))
    poemCountText.strip()
    return poemCountText

url = "https://www.antoloji.com/"
newUrl = url
deletedPoets=[]
poems=[]


with open('poetList') as f:
    poetList=[line.split()[-1] for line in f]

for e in poetList:
    i=1
    k=0
    txt=open(os.path.join(path, e), "w")
    newUrl=url + (e) + "/siirleri"
    driver.get(newUrl)
    time.sleep(0.5)
    poemCountText=getPoemCount()
    driver.find_element(By.CLASS_NAME, 'list-poem-1').click()
    while(i<int(poemCountText)):
        try:
            pdtextclass = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'pd-text'))
            )
            pdtext = WebDriverWait(pdtextclass,10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'p'))
            )
            pdtitle = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'pd-title-a'))
            )
            txt.write(str(i) + '- '+ pdtitle.text + "\n")
            for t in pdtext:
                txt.write(t.text + '\n')
            time.sleep(0.5)
            txt.write('\n \n ************************** \n \n')
            time.sleep(0.5)
            WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.content > div:nth-child(6) > div.content-bar > div.poem-detail.box > div.pd-title > div.after-poem > a'))
            ).click()
            i+=1
            time.sleep(0.5)
        except:
            if(i!=(int(poemCountText)-1)):
                driver.refresh()
            else:
                txt.close()
                break

driver.quit()