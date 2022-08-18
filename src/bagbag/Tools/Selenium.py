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
    from .. import Lg
    from ..Thread import Thread
except:
    import sys 
    sys.path.append("..")
    from Http import useragents 
    import Lg 
    from Thread import Thread

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

        return self
    
    def PressEnter(self) -> seleniumElement:
        """
        It takes the element that you want to press enter on and sends the enter key to it
        """

        if self.se.browserName == "chrome" and not self.se.browserRemote:
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(useragents)['user_agent']})
        
        self.element.send_keys(webkeys.ENTER)

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
    
    def SetCookie(self, cookie:dict|list[dict]):
        """
        If the cookie is a dictionary, add it to the driver. If it's a list of dictionaries, add each
        dictionary to the driver
        
        :param cookie: dict|list[dict]
        :type cookie: dict|list[dict]
        """
        if type(cookie) == dict:
            self.driver.add_cookie(cookie)
        else:
            for i in cookie:
                self.driver.add_cookie(i)
    
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
        self.closed = True
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
    
    def Except(self, *xpath:str, timeout:int=30) -> int | None:
        """
        It waits for some certain elements to appear on the screen.
        
        :param : xpath:str - The xpaths of the element you want to find
        :type : str
        :param timeout: The number of seconds to wait for the element to appear, defaults to 30
        :type timeout: int (optional)
        :return: The index of the xpath that is found.
        """
        for _ in range(timeout*2):
            for x in range(len(xpath)):
                if self.Find(x, False):
                    return x
            time.sleep(0.5)
    
    def __enter__(self):
        return self 
    
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.Close()
        except:
            pass

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
    def __init__(self, seleniumServer:str=None, httpProxy:str=None, sessionID=None):
        options = webdriver.ChromeOptions()

        # 防止通过navigator.webdriver来检测是否是被selenium操作
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        options.add_argument('--user-agent=' + random.choice(useragents)['user_agent'] + '')

        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        if httpProxy:
            options.add_argument('--proxy-server=' + httpProxy)

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
        self.closed = False

        Thread(self.autoRealodOnErrorChrome)
    
    def autoRealodOnErrorChrome(self):
        # 如果载入页面失败, 有个Reload的按钮
        while True:
            #Lg.Trace("查找")
            try:
                if self.Find("/html/body/div[1]/div[2]/div/button[1]", 1):
                    if self.Find("/html/body/div[1]/div[2]/div/button[1]").Text() == "Reload":
                        #Lg.Trace("Refresh")
                        self.Refresh()
                        time.sleep(10)
            except:
                if self.closed:
                    break
                else:
                    Lg.Error("查找页面加载失败的Reload按钮出错", exc=True)
            time.sleep(1)

if __name__ == "__main__":
    # Local 
    with Chrome() as se:
    # Remote 
    # with Chrome("http://127.0.0.1:4444") as se:

    # With PAC 
    # with Firefox(PACFileURL="http://192.168.1.135:8000/pac") as se:
    # with Chrome("http://127.0.0.1:4444", PACFileURL="http://192.168.1.135:8000/pac") as se:

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

    # With Proxy
    # with Chrome("http://192.168.1.229:4444", httpProxy="http://192.168.168.54:8899") as se:
        
        # PAC test 
        se.Get("http://ipinfo.io/ip")
        print(se.PageSource())

        # se.Get("https://ifconfig.me/ip")
        # print(se.PageSource())
        
        # se.Get("http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/")
        # print(se.PageSource())

        # Function test
        # se.Get("https://find-and-update.company-information.service.gov.uk/")
        # inputBar = se.Find("/html/body/div[1]/main/div[3]/div/form/div/div/input")
        # inputBar.Input("ade")
        # button = se.Find('//*[@id="search-submit"]').Click()
        # print(se.PageSource())


    