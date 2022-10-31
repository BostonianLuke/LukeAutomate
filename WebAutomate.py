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
        self.__driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = self.__options)
        
    def openPage(self, url):
        self.__driver.get(url)
        return self
    
    def getCurrentTitle(self):
        return self.__driver.title
    
    def getHTMLSource(self):
        return self.__driver.page_source
        
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

import time
def findHTMLCount(folder):
    return len(
        [
            fileName 
            for fileName 
            in os.listdir(folder) 
            if (fileName.endswith('.html') or fileName.endswith('.htm'))
        ]
    )

def mineNonScrapedWebsites(webAutomate, url, number):
    
    # Go to website
    webAutomate.openPage(url)

    # Wait for end of HTML document to appear
    webAutomate.getElement("/html")
    
    with open(rf"C:\Users\Administrator\Documents\Queries\{number}.html", "w", encoding = "utf-8") as file:
        file.write(webAutomate.getHTMLSource())

from sqlServerConnect import DatabaseConnect
connectionDict = {"server" : "tradedatabase.cqjr8z0s1k6r.us-east-1.rds.amazonaws.com",
                  "database" : "TradebaseDataWarehouse",
                  "username" : "admin",
                  "password" : 'KillLuke$429'}

database = DatabaseConnect(connectionDict)

webAutomate = WebAutomate()

for number, url in enumerate(database.executeQuery("SELECT URL FROM websitesCannotScrap")["URL"].values.tolist()):
    mineNonScrapedWebsites(webAutomate, url, number)
    
del webAutomate
