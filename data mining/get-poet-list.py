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
driver.get("https://tr.wikipedia.org/wiki/%C3%87a%C4%9Fda%C5%9F_T%C3%BCrk_%C5%9Fairler_listesi")
Tr2Eng = str.maketrans("âçğöşüı", "acgosui")
poets=[]
poets2=[]
sairler=[]
result=[]
pList=[]
pList2=[]
deleted=[]
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


elements = driver.find_element(By.XPATH,'//*[@id="mw-content-text"]/div[1]/ul') 
poetList = elements.find_elements(By.TAG_NAME, 'li')

for element in poetList:
    poets.append(element.text)


driver.get("http://www.cs.rpi.edu/~sibel/poetry/sair_listesi.html")
elements2 = driver.find_element(By.XPATH,'/html/body/table/tbody/tr')
poetList2 = elements2.find_elements(By.TAG_NAME, 'dt')

for element in poetList2:
    poets2.append(element.text)


poets= poets + poets2

poets=[cleanList(i) for i in poets]

for poet in poets:
    sairler.append(poet.lower().translate(Tr2Eng))
    
for poet in sairler:
    if(len(poet)<50):
        if poet not in result:
            result.append(poet)

result.sort()
for i in result:
    print(i)

url = "https://www.antoloji.com/"
newUrl = url

dots= '..........'
for p in result:
    newUrl=url + p + "/siirleri"
    driver.get(newUrl)
    time.sleep(0.5)
    control=pageCheck()
    if(boolean(control)):
        print (p + ' sayfası bulunamadı')
        deleted.append(p)
    else:
        poemCountText=getPoemCount()
        print('x'+poemCountText+'x')
        if(int(poemCountText)<15):
            deleted.append(p)
        else:
            while True:
                try:
                    WebDriverWait(driver,5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'list-poem-1'))
                    ).click()
                    pdtext=WebDriverWait(driver,5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'pd-text'))
                    )
                    time.sleep(0.5)
                    pdtext=driver.find_element(By.CLASS_NAME,'pd-text')
                    if  dots in pdtext.text:
                        print(p + ' EKSİK!!!!!!')
                        pList2.append(p)
                        break
                    else:
                        pList.append(p)
                        break
                except:
                    driver.refresh()

for f in poetList2:
    print(f)

with open('poetList','w') as poetTXT:
    for index, item in enumerate(pList):
        poetTXT.write(str(index) + '- ' + item + '\n')

with open('poetList2','w') as poetTXT2:
    for index, item in enumerate(pList2):
        poetTXT2.write(str(index) + '- ' + item + '\n')

driver.quit()

'''
else:
    pList.append(p)
    print(p + ' eklendi')
'''