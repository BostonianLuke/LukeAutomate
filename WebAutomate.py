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
                lambda fileName: fileName.endswith('.htm'), 
                os.listdir(folder)
            )
        )
    )

def mineNonScrapedWebsites(webAutomate, url):
    
    folder = r"C:\Users\Administrator\Downloads"
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
