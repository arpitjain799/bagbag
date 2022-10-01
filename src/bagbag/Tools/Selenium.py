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
    from .URL import URL
except:
    import sys 
    sys.path.append("..")
    from Http import useragents 
    import Lg 
    from Thread import Thread
    from URL import URL

def retryOnError(func):
    def ware(self, *args, **kwargs): # self是类的实例
        if self.browserName == "chrome":
            while True:
                try:
                    res = func(self, *args, **kwargs)

                    try:
                        NeedRefresh = False
                        # 如果载入页面失败, 有个Reload的按钮
                        if hasattr(self, "Find"):
                            if self.Find("/html/body/div[1]/div[2]/div/button[1]", 0):
                                if self.Find("/html/body/div[1]/div[2]/div/button[1]").Text() == "Reload":
                                    NeedRefresh = True
                        elif hasattr(self, "se") and hasattr(self.se, "Find"):
                            if self.se.Find("/html/body/div[1]/div[2]/div/button[1]", 0):
                                if self.se.Find("/html/body/div[1]/div[2]/div/button[1]").Text() == "Reload":
                                    NeedRefresh = True

                        if hasattr(self, "PageSource"):
                            page = self.PageSource()
                        elif hasattr(self, "se") and hasattr(self.se, "PageSource"):
                            page = self.se.PageSource()
                        
                        if hasattr(self, "Url"):
                            url = self.Url()
                        elif hasattr(self, "se") and hasattr(self.se, "Url"):
                            url = self.se.Url()

                        chklists = [
                            [
                                'This page isn’t working',
                                'ERR_EMPTY_RESPONSE',
                                'didn’t send any data',
                                URL(url).Parse().Host,
                            ],
                            [
                                'This site can’t be reached',
                                'unexpectedly closed the connection',
                                'ERR_CONNECTION_CLOSED',
                                URL(url).Parse().Host,
                            ],
                            [
                                "This site can’t be reached",
                                "took too long to respond",
                                "ERR_TIMED_OUT",
                                URL(url).Parse().Host,
                            ],
                            [
                                "No internet",
                                "There is something wrong with the proxy server, or the address is incorrect",
                                "ERR_PROXY_CONNECTION_FAILED",
                            ],
                            [
                                'ERR_CONNECTION_RESET',
                                'This site can’t be reached',
                                'The connection was reset',
                                URL(url).Parse().Host,
                            ]
                        ]
                        for chklist in chklists:
                            if False not in map(lambda x: x in page, chklist):
                                NeedRefresh = True 
                        
                        if NeedRefresh:
                            if hasattr(self, "Refresh"):
                                self.Refresh()
                            elif hasattr(self, "se") and hasattr(self.se, "Refresh"):
                                self.se.Refresh()
                            time.sleep(5)
                        else:
                            return res

                    except Exception as e:
                        if hasattr(self, "closed") and self.closed:
                            break 
                        elif hasattr(self, "se") and hasattr(self.se, "closed") and self.se.closed:
                            break
                        else:
                            raise e
                    time.sleep(1)
                except Exception as e:
                    chklist = [
                        'ERR_CONNECTION_CLOSED',
                        'ERR_EMPTY_RESPONSE',
                        'ERR_TIMED_OUT',
                        'ERR_PROXY_CONNECTION_FAILED',
                        'ERR_CONNECTION_RESET',
                    ]
                    if True in map(lambda x: x in str(e), chklist):
                        Lg.Trace("有错误, 自动刷新")
                        if hasattr(self, "Refresh"):
                            self.Refresh()
                        elif hasattr(self, "se") and hasattr(self.se, "Refresh"):
                            self.se.Refresh()
                        time.sleep(5)
                    else:
                        raise e

        elif self.browserName == "firefox":
            res = func(self, *args, **kwargs)
            return 

    return ware

# > The seleniumElement class is a wrapper for the selenium.webdriver.remote.webelement.WebElement
# class
class seleniumElement():
    def __init__(self, element:selenium.webdriver.remote.webelement.WebElement, se:seleniumBase):
        self.element = element
        self.se = se
        self.driver = self.se.driver
        self.browserName = self.se.browserName
        self.browserRemote = self.se.browserRemote
    
    def Clear(self) -> seleniumElement:
        """
        Clear() clears the text if it's a text entry element
        """
        self.element.clear()
        return self
    
    @retryOnError
    def Click(self) -> seleniumElement:
        """
        Click() is a function that clicks on an element
        """
        if self.browserName == "chrome" and not self.browserName:
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
    
    @retryOnError
    def Submit(self) -> seleniumElement:
        """
        Submit() is a function that submits the form that the element belongs to
        """
        if self.browserName == "chrome" and not self.browserName:
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(useragents)['user_agent']})
        
        self.element.submit()

        return self
    
    @retryOnError
    def PressEnter(self) -> seleniumElement:
        """
        It takes the element that you want to press enter on and sends the enter key to it
        """

        if self.browserName == "chrome" and not self.browserName:
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(useragents)['user_agent']})
        
        self.element.send_keys(webkeys.ENTER)

        return self
    
    def ScrollIntoElement(self) -> seleniumElement:
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)
        return self

class seleniumBase():
    def Find(self, xpath:str, timeout:int=60, scrollIntoElement:bool=True) -> seleniumElement|None:
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
    
    @retryOnError
    def Get(self, url:str):
        """
        The function Get() takes a string as an argument and uses the driver object to navigate to the
        url.
        
        :param url: The URL of the page you want to open
        :type url: str
        """

        if self.browserName == "chrome" and self.randomUA:
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
            try:
                self.driver.delete_all_cookies()
            except:
                pass 
            try:
                self.driver.execute_script("localStorage.clear();")
            except:
                pass 
            try:
                self.driver.execute_script("sessionStorage.clear();")
            except:
                pass 
            try:
                self.driver.execute_script("const dbs = await window.indexedDB.databases();dbs.forEach(db => { window.indexedDB.deleteDatabase(db.name)});")
            except:
                pass
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
        if type(xpath[0]) == list:
            xpath = xpath[0]
            
        for _ in range(timeout*2):
            for x in range(len(xpath)):
                if self.Find(xpath[x], 0, scrollIntoElement=False):
                    return x
            time.sleep(0.5)

        return None 
    
    def SwitchTabByID(self, number:int):
        """
        SwitchTabByID(self, number:int) switches to the tab with the given ID, start from 0
        
        :param number: The number of the tab you want to switch to
        :type number: int
        """
        self.driver.switch_to.window(self.driver.window_handles[number])
    
    def SwitchTabByIdent(self, ident:str):
        self.driver.switch_to.window(ident)

    def Tabs(self) -> list[str]:
        return self.driver.window_handles
    
    def NewTab(self) -> str:
        """
        It opens a new tab, and returns the ident of the new tab
        :return: The new tab's ident.
        """
        tabs = self.driver.window_handles
        self.driver.execute_script('''window.open();''')
        for i in self.driver.window_handles:
            if i not in tabs:
                return i
    
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
    def __init__(self, seleniumServer:str=None, PACFileURL:str=None, httpProxy:str=None, sessionID=None, randomUA:bool=True):
        options = webdriver.ChromeOptions()

        # 防止通过navigator.webdriver来检测是否是被selenium操作
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        if randomUA:
            options.add_argument('--user-agent=' + random.choice(useragents)['user_agent'] + '')
        self.randomUA = randomUA

        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        if PACFileURL:
            options.add_argument("--proxy-pac-url=" + PACFileURL)
        elif httpProxy:
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

if __name__ == "__main__":
    # Local 
    # with Chrome() as se:
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
        # se.Get("http://ipinfo.io/ip")
        # print(se.PageSource())

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

    with Chrome(httpProxy="http://192.168.1.186:8899", randomUA=True) as se:
        se.Get("https://twitter.com/TommyBeFamous/status/1571969221919404032")
        import ipdb
        ipdb.set_trace()
    