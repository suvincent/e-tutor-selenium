from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import config
########################################################################
###### Config
E_TUTOR_LOGIN_URL = config.E_TUTOR_LOGIN_URL
ACCOUNT = config.ACCOUNT
PASSWORD = config.PASSWORD
E_TUTOR_HW_URL = config.E_TUTOR_HW_URL
PAGE_NUM = config.PAGE_NUM
OUTPUT_FILE_NAME = config.OUTPUT_FILE_NAME
WITH_WEIGHT = config.WITH_WEIGHT
########################################################################


########################################################################
###### Methods to Crawl the score
def get_score(subId, time, name, result, url):
    chrome.get(url)
    soupTest = BeautifulSoup(chrome.page_source, 'html.parser')
    detail = soupTest.find('div',{'id':'test-result-detail'}).find('p').getText()
    score  = [int(s) for s in detail.split() if s.isdigit()]
    return {
        "Name" : name,
        "SubmitId" : subId,
        "Result" : result,
        "Uploadtime" : time,
        "TotalScore": score[0],
        "TestScore":score[1]
    }

def get_score_with_weight(subId, time, name, result, url):
    chrome.get(url)
    soupTest = BeautifulSoup(chrome.page_source, 'html.parser')
    detailTable = soupTest.find('table',{'id':'test-result-detail-table'})
    dflag = False
    darray = []
    for detail in detailTable.find_all('tr'):
        if not dflag:
            dflag = True
            continue
        ddata = []
        for item in detail.find_all('td'):
            ddata.append(item.getText())
        print(ddata)
        darray.append(ddata)
    TotalScore = 0
    TestScore = 0
    for row in darray:
        TotalScore += int(row[1])
        if (row[11] == '是'):
            TestScore += int(row[1])
    return {
        "Name" : name,
        "SubmitId" : subId,
        "Result" : result,
        "Uploadtime" : time,
        "TotalScore": TotalScore,
        "TestScore": TestScore
    }

def get_class_score(class_data):
    class_score = []
    for student in class_data:
        if WITH_WEIGHT :
            score = get_score_with_weight(student[0],student[1],student[2],student[5],student[10])
        else:
            score = get_score(student[0],student[1],student[2],student[5],student[10])
        class_score.append(score)
    return class_score

def get_page_data(url,pageNum):
    Data = []
    for page in range(pageNum):
        chrome.get(url+str(page))
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        table = soup.find('table', {'id': 'detail-table'})
        flag = False
        for row in table.find_all('tr'):
            if not flag:
                # print(row)
                flag = True
                continue
            person = []
            for d in row.find_all('td'):
                person.append(d.getText())
            for a in row.find_all('a', href=True):
                # print ("Found the URL:", a['href'])
                person.append(a['href'])
            Data.append(person)
    return Data
########################################################################


########################################################################
###### Initialization
options = Options()
options.add_argument("--disable-notifications")
 
chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
chrome.get(E_TUTOR_LOGIN_URL)

email = chrome.find_element_by_id("username")
password = chrome.find_element_by_id("password")
# 請在這十五秒內點完 recapcha
time.sleep(5)
email.send_keys(ACCOUNT)
time.sleep(5)
password.send_keys(PASSWORD)
time.sleep(5)
password.submit()
###### Initialization
########################################################################


########################################################################
###### Execute Crawling and export
PyClass = []
PyClass = get_page_data(E_TUTOR_HW_URL,PAGE_NUM)
class_result = get_class_score(PyClass)
df = pd.DataFrame(class_result)
df.to_csv(OUTPUT_FILE_NAME)
########################################################################