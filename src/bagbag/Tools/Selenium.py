from selenium import webdriver

class Selenium():
    def __init__(self, SeleniumServer:str=None):
        if SeleniumServer:
            if not SeleniumServer.endswith("/wd/hub"):
                SeleniumServer = SeleniumServer + "/wd/hub"

            chrome_options = webdriver.ChromeOptions()
            self.driver = webdriver.Remote(
                command_executor=SeleniumServer,
                options=chrome_options
            )
        else:
            self.driver = webdriver.Chrome()
    
    def Get(self, url:str):
        self.driver.get(url)
    
    def PageSource(self) -> str:
        return self.driver.page_source

    def Title(self) -> str:
        return self.driver.title
    
    def Close(self):
        self.driver.close()

if __name__ == "__main__":
    # se = Selenium()
    se = Selenium("http://127.0.0.1:4444")
    se.Get("http://google.com")
    print(se.PageSource())
    se.Close()

