#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

class WebAutomate:
    
    def __init__(self):
        self.__options = webdriver.ChromeOptions()
        self.arguments(["--ignore-certificate-errors", "--start-maximized"])
        prefs = {"download.default_directory" : "C:/Users/Luke Therieau/Documents/Luke's Repository"}
        self.__options.add_experimental_option("prefs", prefs)
        
        self.__driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = self.__options)
        
    def openPage(self, url):
        self.__driver.get(url)
        return self
    
    def getCurrentTitle(self):
        return self.__driver.title
    
    def waitForChrome(self):
        self.__driver.WebDriverWait()
        
    def arguments(self, arguments):
        for argument in arguments:
            self.__options.add_argument(argument)
        return self
    
    def getElement(self, xPath):
        elementNotFound = True
        while elementNotFound:
            try:
                element = ActionChains(self.__driver).move_to_element(self.__driver.find_element(by = By.XPATH, value = xPath))
                elementNotFound = False
            except NoSuchElementException:
                elementNotFound = True
        return element
    
    def getURL(self):
        return self.__driver.current_url
    
    def __del__(self):
        self.__driver.quit()


# In[2]:


import pyautogui
import pyperclip
import pandas as pd
import os


def mineRelatedSearches(webAutomate, query):
    # Go to Google
    webAutomate.openPage("https://www.google.com")

    # Type query into Google
    webAutomate.getElement("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(query).perform()

    # Press Enter, to start Google Search
    webAutomate.getElement("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(Keys.RETURN).perform()

    # Wait for end of HTML document to appear
    webAutomate.getElement("/html")

    # Select and copy site's content
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    # Website content
    return [
        query 
        for query 
        in pyperclip.paste().partition("Related searches")[-1].partition("1\t")[0].split("\r\n") 
        if query != ""
    ]

def mineNewQueries(queries):
    webAutomate = WebAutomate()

    foundRelatedSearches = pd.Series([relatedQuery for query in [mineRelatedSearches(webAutomate, query) for query in queries] for relatedQuery in query], name = "queries")

    del webAutomate
    
    return foundRelatedSearches


# In[8]:


# queries = ["Trading Algorithm", "AI", "Fin Tech", "AI Trading"]
# mineNewQueries(queries)


# In[22]:





# In[27]:


def findHTMLCount(folder):
    return len(
        list(
            filter(
                lambda fileName: fileName.endswith('.html'), 
                os.listdir(folder)
            )
        )
    )

def mineNonScrapedWebsites(webAutomate, url):
    
    folder = r"C:\Users\Luke Therieau\Downloads"
    beforeCount = findHTMLCount(folder)
    
    # Go to website
    webAutomate.openPage(url)

    # Wait for end of HTML document to appear
    webAutomate.getElement("/html")

    # Select and copy site's content
    pyautogui.hotkey('ctrl', 's')
    
    while beforeCount == findHTMLCount(folder):
        pyautogui.press('enter')


# In[28]:


from sqlServerConnect import DatabaseConnect
connectionDict = {"server" : "tradedatabase.cqjr8z0s1k6r.us-east-1.rds.amazonaws.com",
                  "database" : "TradebaseDataWarehouse",
                  "username" : "admin",
                  "password" : 'KillLuke$429'}

database = DatabaseConnect(connectionDict)

webAutomate = WebAutomate()

for url in database.executeQuery("SELECT URL FROM websitesCannotScrap")["URL"].values.tolist():
    mineNonScrapedWebsites(webAutomate, url)

del webAutomate


# In[ ]:


# Export to csv
        pd.Series(
            [
                query 
                for query 
                in content.partition("Related searches")[-1].partition("1\t")[0].split("\r\n") 
                if query != ""
            ], 
            name = "queries"
        ).to_csv(f"{folder}/{query}.csv", 
                 index = None)


# In[30]:


import os 
for file in os.listdir(folder):
    test = pd.read_csv(f"{folder}/{file}")


# In[19]:





# In[16]:


os.listdir(r"C:\Users\Luke Therieau\Downloads")


# In[15]:


import requests
s = requests.Session()
r = s.get("https://algorithmictrading.net/algorithmic-trading-information/?utm_source=GoogleAdwords&utm_medium=PPC&utm_campaign=AlgorithmicTradingEXACT&utm_term=Stock%20market%20algorithms&utm_content=textlink&utm_campaign=A-QS10-Algorithmic-Trading-EXACT&utm_source=google&utm_medium=cpc&utm_content=algo-stock-market-EXACT&utm_term=stock%20market%20algorithms&gclid=EAIaIQobChMIluWS4dyP-AIVz__jBx2AFggTEAAYASAAEgKaPPD_BwE")


# In[21]:


#r.content


# In[ ]:


# i = 1
# action(driver, f"/html/body/div[7]/div/div[10]/div[1]/div[1]/div[3]/div/div[{i}]/div/div/div/div[1]/a/div[1]/span").click().perform()
html/body/div[7]/div/div[10]/div[1]/div[1]/div[3]/div/div[1]/div/div/div/div[1]/a/div[1]/span()
html/body/div[7]/div/div[10]/div[1]/div[1]/div[3]/div/div[2]/div/div/div/div[1]/a/div[1]/span()
html/body/div[7]/div/div[10]/div[1]/div[1]/div[3]/div/div[3]/div/div/div/div[1]/a/div[1]/span()


# In[42]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time

def action(driver, xPath):
    elementFound = False
    while elementFound == False:
        try:
            element = ActionChains(driver).move_to_element(driver.find_element_by_xpath(xPath))
            elementFound = True
        except NoSuchElementException:
            elementFound == False
    return element
    




options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--start-maximized")



#class="yuRUbf"


driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(), options = options)
driver.get("https://www.google.com")

query = "Trading Algorithm"
action(driver, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(query).perform()
action(driver, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(Keys.RETURN).perform()
action(driver, "/html/body/div[7]/div/div[10]/div[1]/div[1]/div[3]/div/div[1]/div/div/div/div[1]/a/div[1]/span").click().perform()
articleURL = driver.current_url
driver.quit()

import requests
from bs4 import BeautifulSoup


result = requests.get(articleURL).content
soup = BeautifulSoup(result, "html.parser")
soup


# In[20]:


import pandas as pd
import datetime as dt

s = requests.Session()
r = s.get("http://smei.ucsd.edu/new_smei/data&images/stars/handlers.php/v__bet_lyr/friendlycsv")

soup = BeautifulSoup(r.content, "html.parser")
Beta_Lyrae = pd.DataFrame([row.replace('</p>','').split(",") for row in str(soup.findAll('p')).replace('[','').replace(']','').strip('').replace('<p>','').replace(' ','').split("</p>,")],columns=['DateTime','Magnitude'])
Beta_Lyrae['Magnitude'] = Beta_Lyrae['Magnitude'].apply(lambda x: float(x))
Beta_Lyrae = Beta_Lyrae.reset_index()
Beta_Lyrae['DateTime'] = Beta_Lyrae['DateTime'].apply(lambda x: dt.datetime.strptime(f"{x}", "%Y-%m-%d%H:%M:%S"))


# In[21]:


Beta_Lyrae


# In[1]:


# import module
from bs4 import BeautifulSoup
import requests

url = "https://google.com/search"

headers = {
'User-agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}

params = {
'q': 'Hello World',
'gl': 'us',
'hl': 'en',
}
response = requests.request("GET", url, params = params, headers = headers)

#class="egMi0 kCrYT"



# parse html content
soup = BeautifulSoup(response.text, 'html.parser')

soup.find_all("div", {"class": "egMi0 kCrYT"})

#print(response.text)


# In[5]:


import boto3

region = 'us-east-1'

instances = ['i-087adaa4c3bbd8ce2']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))
lambda_handler()


# In[ ]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

class WebAutomate:

def __init__(self):
self.__options = webdriver.ChromeOptions()
self.addArguments(["--ignore-certificate-errors", "--start-maximized"])
self.__options = self.__options.add_argument("--start-maximized")
self.__driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(),
options = self.__options)
for i in range(4):
self.__driver.maximize_window()
#self.__driver.switch_to_window(self.__driver.current_window_handle)


def addArguments(self, arguments):
for argument in arguments:
self.__options.add_argument(argument)

def openPage(self, url):
self.__driver.get(url)
return self

def getElement(self, xPath):
elementNotFound = True
element = ""
while elementNotFound:
try:
element = ActionChains(self.__driver).move_to_element(self.__driver.find_element(by = By.XPATH, value = xPath))
elementNotFound = False
except NoSuchElementException:
elementNotFound = True
return element

def findAllLinks(self):
return self.__driver.find_elements(by = By.TAG_NAME, value = "href")

def getURL(self):
return self.__driver.current_url

def __del__(self):
self.__driver.quit()


import time
from selenium.webdriver.common.keys import Keys
import pyautogui

query = "Trading Algorithm"

actionDict = {"Enter Google Search Text" : "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input",
"Click Google Result" : "/html/body/div[7]/div/div[10]/div[1]/div[1]/div[3]/div/div[Replace]/div/div/div/div[1]/a/div[1]/span"}

queryArray = ["Trading Algorithm"]

urls = []

webAutomate = WebAutomate()
webAutomate.openPage(r"https://www.google.com/")
webAutomate.getElement(actionDict["Enter Google Search Text"]).send_keys(query).perform()
pyautogui.press('enter')

webAutomate.getElement("//div[@class='g']//div[@class='r']//a[not(@class)]").click().perform()

# array = webAutomate.findAllLinks()
# for links in webAutomate.findAllLinks():
# links.click().perform()
# urls.append(webAutomate.getURL())
# pyautogui.hotkey('alt', 'left')

# del webAutomate

# for i in range(1,20):
# print(i)
# webAutomate.getElement(actionDict["Click Google Result"].replace("Replace", str(3))).click().perform()
# urls.append(webAutomate.getURL())
# pyautogui.hotkey('alt', 'left')
# del webAutomate

# import module


# In[ ]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

class WebAutomate:

def __init__(self):
    self.__options = webdriver.ChromeOptions()
    self.addArguments(["--ignore-certificate-errors", "--start-maximized"])
    self.__options = self.__options.add_argument("--start-maximized")
    self.__driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(),
                                     options = self.__options)
# for i in range(4):
# self.__driver.maximize_window()
# #self.__driver.switch_to_window(self.__driver.current_window_handle)


def addArguments(self, arguments):
    for argument in arguments:
        self.__options.add_argument(argument)

def openPage(self, url):
    self.__driver.get(url)
    return self

def getElement(self, xPath):
    elementNotFound = True
element = ""
while elementNotFound:
try:
element = ActionChains(self.__driver).move_to_element(self.__driver.find_element(by = By.XPATH, value = xPath))
elementNotFound = False
except NoSuchElementException:
elementNotFound = True
return element

def findAllLinks(self):
return self.__driver.find_elements(by = By.TAG_NAME, value = "href")

def getURL(self):
return self.__driver.current_url

def __del__(self):
self.__driver.quit()


import time
from selenium.webdriver.common.keys import Keys
import pyautogui

query = "Trading Algorithm"

actionDict = {"Enter Google Search Text" : "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input",
"Click Google Result" : "/html/body/div[7]/div/div[10]/div[1]/div[1]/div[3]/div/div[Replace]/div/div/div/div[1]/a/div[1]/span"}

queryArray = ["Trading Algorithm"]

urls = []

webAutomate = WebAutomate()
webAutomate.openPage(r"https://www.google.com/")
webAutomate.getElement(actionDict["Enter Google Search Text"]).send_keys(query).perform()
pyautogui.press('enter')

webAutomate.getElement("//div[@class='g']//div[@class='r']//a[not(@class)]").click().perform()

# array = webAutomate.findAllLinks()
# for links in webAutomate.findAllLinks():
# links.click().perform()
# urls.append(webAutomate.getURL())
# pyautogui.hotkey('alt', 'left')

# del webAutomate

# for i in range(1,20):
# print(i)
# webAutomate.getElement(actionDict["Click Google Result"].replace("Replace", str(3))).click().perform()
# urls.append(webAutomate.getURL())
# pyautogui.hotkey('alt', 'left')
# del webAutomate



# In[9]:


from bs4 import BeautifulSoup
import requests
import unicodedata

def WebScrape(url):
    headers = {
        'User-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
    }
    
    params = {
        'gl': 'us',
        'hl': 'en',
    }
    
    response = requests.request("GET", url, params = params, headers = headers)
    
    # parse html content
    soup = BeautifulSoup(response.text, 'html.parser')
    content = [[tag.name, unicodedata.normalize("NFKD",tag.text.strip())]
               for tag
               in soup.find_all(["p", "h1", "h2", "h3"])]
    return content

urls = ["https://www.investopedia.com/articles/active-trading/101014/basics-algorithmic-trading-concepts-and-examples.asp",
        "https://www.investopedia.com/articles/active-trading/090815/picking-right-algorithmic-trading-software.asp",
        "https://en.wikipedia.org/wiki/Algorithmic_trading",
        "https://www.wsj.com/graphics/journey-inside-a-real-life-trading-algorithm/",
        "https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/what-are-algorithms-algos/",
        "https://www.quantconnect.com/"]

results = {url : WebScrape(url) for url in urls}


# In[27]:


results


# In[26]:


import pandas as pd
#pd.DataFrame(results[list(results.keys())[0]],columns = ["Tag", "Text"])
results[list(results.keys())[4]]


# In[ ]:




