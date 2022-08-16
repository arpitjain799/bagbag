from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.common.by import By as webby
import selenium
from selenium.webdriver.common.keys import Keys as webkeys
from selenium.webdriver.firefox.options import Options as firefoxoptions

import time

import random

try:
    from ..Http import useragents 
except:
    import sys 
    sys.path.append("..")
    from Http import useragents 

# > The seleniumElement class is a wrapper for the selenium.webdriver.remote.webelement.WebElement
# class
class seleniumElement():
    def __init__(self, element:selenium.webdriver.remote.webelement.WebElement, se:seleniumBase):
        self.element = element
        self.se = se
        self.driver = self.se.driver
    
    def Clear(self) -> seleniumElement:
        """
        Clear() clears the text if it's a text entry element
        """
        self.element.clear()
        return self
    
    def Click(self) -> seleniumElement:
        """
        Click() is a function that clicks on an element
        """
        if self.se.browserName == "chrome" and not self.se.browserRemote:
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(useragents)['user_agent']})

        self.element.click()

        # 如果载入页面失败, 有个Reload的按钮
        while self.se.Find("/html/body/div[1]/div[2]/div/button[1]", False):
            self.se.Refresh()
            time.sleep(3)
        return self
    
    def Text(self) -> str:
        """
        The function Text() returns the text of the element
        :return: The text of the element.
        """
        return self.element.text

    def Attribute(self, name:str) -> str:
        """
        This function returns the value of the attribute of the element
        
        :param name: The name of the element
        :type name: str
        :return: The attribute of the element.
        """
        return self.element.get_attribute(name)
    
    def Input(self, string:str) -> seleniumElement:
        """
        The function Input() takes in a string and sends it to the element
        
        :param string: The string you want to input into the text box
        :type string: str
        """
        self.element.send_keys(string)
        return self
    
    def Submit(self) -> seleniumElement:
        """
        Submit() is a function that submits the form that the element belongs to
        """
        if self.se.browserName == "chrome" and not self.se.browserRemote:
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(useragents)['user_agent']})
        
        self.element.submit()

        # 如果载入页面失败, 有个Reload的按钮
        while self.se.Find("/html/body/div[1]/div[2]/div/button[1]", False):
            self.se.Refresh()
            time.sleep(3)
        return self
    
    def PressEnter(self) -> seleniumElement:
        """
        It takes the element that you want to press enter on and sends the enter key to it
        """

        if self.se.browserName == "chrome" and not self.se.browserRemote:
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(useragents)['user_agent']})
        
        self.element.send_keys(webkeys.ENTER)

        # 如果载入页面失败, 有个Reload的按钮
        while self.se.Find("/html/body/div[1]/div[2]/div/button[1]", False):
            self.se.Refresh()
            time.sleep(3)
        return self
    
    def ScrollIntoElement(self) -> seleniumElement:
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)
        return self

class seleniumBase():
    def Find(self, xpath:str, timeout:int=8, scrollIntoElement:bool=True) -> seleniumElement|None:
        """
        > Finds an element by xpath, waits for it to appear, and returns it
        
        :param xpath: The xpath of the element you want to find
        :type xpath: str
        :param timeout: , defaults to 8 second
        :type timeout: int (optional)
        :param scrollIntoElement: If True, the element will be scrolled into view before returning it,
        defaults to True
        :type scrollIntoElement: bool (optional)
        :return: seleniumElement
        """
        waited = 0
        while True:
            try:
                el = self.driver.find_element(webby.XPATH, xpath)
                if scrollIntoElement:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
                return seleniumElement(el, self)
            except selenium.common.exceptions.NoSuchElementException as e: 
                if timeout == 0:
                    return None 
                elif timeout == -1:
                    time.sleep(1)
                elif timeout > 0:
                    time.sleep(1)
                    waited += 1
                    if waited > timeout:
                        return None 

        # import ipdb
        # ipdb.set_trace()
    
    def StatusCode(self) -> int:
        self.driver.stat
    
    def ResizeWindow(self, width:int, height:int):
        """
        :param width: The width of the window in pixels
        :type width: int
        :param height: The height of the window in pixels
        :type height: int
        """
        self.driver.set_window_size(width, height)
    
    def ScrollRight(self, pixel:int):
        """
        ScrollRight(self, pixel:int) scrolls the page to the right by the number of pixels specified in
        the pixel parameter
        
        :param pixel: The number of pixels to scroll by
        :type pixel: int
        """
        self.driver.execute_script("window.scrollBy("+str(pixel)+",0);")
    
    def ScrollLeft(self, pixel:int):
        """
        Scrolls the page left by the number of pixels specified in the parameter.
        
        :param pixel: The number of pixels to scroll by
        :type pixel: int
        """
        self.driver.execute_script("window.scrollBy("+str(pixel*-1)+",0);")

    def ScrollUp(self, pixel:int):
        """
        Scrolls up the page by the number of pixels specified in the parameter.
        
        :param pixel: The number of pixels to scroll up
        :type pixel: int
        """
        self.driver.execute_script("window.scrollBy(0, "+str(pixel*-1)+");")

    def ScrollDown(self, pixel:int):
        """
        Scrolls down the page by the specified number of pixels
        
        :param pixel: The number of pixels to scroll down
        :type pixel: int
        """
        self.driver.execute_script("window.scrollBy(0, "+str(pixel)+");")

    def Url(self) -> str:
        """
        > The `Url()` function returns the current URL of the page
        :return: The current url of the page
        """
        return self.driver.current_url
    
    def Cookie(self) -> list[dict]:
        """
        This function gets the cookies from the driver and returns them as a list of dictionaries
        """
        return self.driver.get_cookies()
    
    def SetCookie(self, cookie_dict:dict):
        """
        This function takes a dictionary of cookie key-value pairs and adds them to the current session
        
        :param cookie_dict: A dictionary object, with mandatory keys as follows:
        :type cookie_dict: dict
        """
        self.driver.add_cookie(cookie_dict)
    
    def Refresh(self):
        """
        Refresh() refreshes the current page
        """
        self.driver.refresh()
    
    def GetSession(self) -> str:
        """
        The function GetSession() returns the session ID of the current driver
        :return: The session ID of the driver.
        """
        return self.driver.session_id
    
    def Get(self, url:str):
        """
        The function Get() takes a string as an argument and uses the driver object to navigate to the
        url.
        
        :param url: The URL of the page you want to open
        :type url: str
        """

        if self.browserName == "chrome":
            if not self.browserRemote:
                self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(useragents)['user_agent']})

        self.driver.get(url)
        # 如果载入页面失败, 有个Reload的按钮
        while self.Find("/html/body/div[1]/div[2]/div/button[1]", False):
            self.Refresh()
            time.sleep(3)
    
    def PageSource(self) -> str:
        """
        It returns the page source of the current page
        :return: The page source of the current page.
        """
        return self.driver.page_source

    def Title(self) -> str:
        """
        The function Title() returns the title of the current page
        :return: The title of the page
        """
        return self.driver.title
    
    def Close(self):
        """
        The function closes the browser window and quits the driver
        """
        self.driver.close()
        self.driver.quit()
    
    def ClearIdent(self):
        if self.browserName == "chrome":
            self.driver.delete_all_cookies()
            self.driver.execute_script("localStorage.clear();")
            self.driver.execute_script("sessionStorage.clear();")
            self.driver.execute_script("const dbs = await window.indexedDB.databases();dbs.forEach(db => { window.indexedDB.deleteDatabase(db.name)});")
        else:
            raise Exception("未实现")

class Firefox(seleniumBase):
    def __init__(self, seleniumServer:str=None, PACFileURL:str=None, sessionID:str=None):
        options = firefoxoptions()

        if PACFileURL:
            options.set_preference("network.proxy.type", 2)
            options.set_preference("network.proxy.autoconfig_url", PACFileURL)

        if seleniumServer:
            if not seleniumServer.endswith("/wd/hub"):
                seleniumServer = seleniumServer + "/wd/hub"
            self.driver = webdriver.Remote(
                command_executor=seleniumServer,
                options=options,
            )
        else:
            self.driver = webdriver.Firefox(options=options)
        
        if sessionID:
            self.Close()
            self.driver.session_id = sessionID
        
        self.browserName = "firefox"
        self.browserRemote = seleniumServer != None 

class Chrome(seleniumBase):
    def __init__(self, seleniumServer:str=None, sessionID=None):
        options = webdriver.ChromeOptions()

        # 防止通过navigator.webdriver来检测是否是被selenium操作
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        options.add_argument('--user-agent=' + random.choice(useragents)['user_agent'] + '')

        if seleniumServer:
            if not seleniumServer.endswith("/wd/hub"):
                seleniumServer = seleniumServer + "/wd/hub"
            self.driver = webdriver.Remote(
                command_executor=seleniumServer,
                options=options
            )
        else:
            self.driver = webdriver.Chrome(
                options=options,
            )

        if sessionID:
            self.Close()
            self.driver.session_id = sessionID
        
        self.browserName = "chrome"
        self.browserRemote = seleniumServer != None 

if __name__ == "__main__":
    # Local 
    se = Chrome()

    # Remote 
    # se = Selenium("http://127.0.0.1:4444")

    # With PAC 
    # se = Firefox(PACFileURL="http://192.168.1.135:8000/pac")
    # se = Selenium("http://127.0.0.1:4444", PACFileURL="http://192.168.1.135:8000/pac")

    # Example of PAC file
    # function FindProxyForURL(url, host)
    # {
    #     if (shExpMatch(host, "*.onion"))
    #     {
    #         return "SOCKS5 192.168.1.135:9150";
    #     }
    #     if (shExpMatch(host, "ipinfo.io"))
    #     {
    #         return "SOCKS5 192.168.1.135:7070";
    #     }
    #     return "DIRECT";
    # }
    
    # PAC test 
    se.Get("http://ipinfo.io/ip")
    print(se.PageSource())

    # se.Get("https://ifconfig.me/ip")
    # print(se.PageSource())
    
    # se.Get("http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/")
    # print(se.PageSource())

    # Function test
    se.Get("https://find-and-update.company-information.service.gov.uk/")
    inputBar = se.Find("/html/body/div[1]/main/div[3]/div/form/div/div/input")
    inputBar.Input("ade")
    button = se.Find('//*[@id="search-submit"]').Click()
    
    print(se.PageSource())

    se.Close()

    