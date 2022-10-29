
import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime as dt


todate = dt.now().strftime('%Y%m%d')

def serch_key(key,line):
    return re.search(key,line, flags=re.IGNORECASE)

class handle_webdriver(object):
    def __init__(
        self,
        work_directory = fr'{os.getcwd()}\{todate}'
        ):
        """_summary_

        Args:
            work_directory (str, optional): work directory for browser. Defaults to '<CurentDirectory>\<YYYYMMDD>'.
        """
        self.work_directory = work_directory
        os.makedirs(self.work_directory,exist_ok=True)
        self.browser = "chrome"
        self.log = fr"{self.work_directory}\usesel_log.log"
        
    def set_browser(self,browser):
        self.browser = browser
        
    def get_browser(self):
        return self.browser  
          
    def set_work_directory(self,work_directory):
        self.work_directory = work_directory
        
    def get_work_directory(self):
        return self.work_directory
    
    def set_log(self,log):
        self.log = log
        
    def get_log(self):
        return self.log  
          
    def write_log(self,text):
        tmp_time = dt.now().strftime('%Y/%m/%d %H:%M:%S')
        try:
            with open(self.log,"a",encoding="utf-8") as f:
                f.write(f"[{tmp_time}]{text}\n")
        except:
            with open(self.log,"a",encoding="shift-jis") as f:
                f.write(f"[{tmp_time}]{text}\n")            
    
    def call_driver(
        self,
        size=(700,700),
        **kwargs
    ):
        """_summary_

        Args:
            size (tuple, optional): browser size. Defaults to (700,700).
        """
        try:
            browser = browser.lower()
        except:
            pass
        options = Options()
        webdriver_major_version = int(webdriver.__version__.split(".")[0])
        if serch_key("chrome",self.browser):
            # Google Chrome
            if webdriver_major_version==4:
                from selenium.webdriver.chrome.service import Service as ChromeService
                from webdriver_manager.chrome import ChromeDriverManager
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),**kwargs)
            elif webdriver_major_version<4:
                from webdriver_manager.chrome import ChromeDriverManager
                self.driver = webdriver.Chrome(ChromeDriverManager().install(),**kwargs)
            else:
                self.write_log("Not Conpatible Selenium Version")
        elif serch_key("headless_chrome",self.browser):
            # Google (HeadlessMode))
            options.add_argument('--headless')
            options.add_argument('--allow-insecure-localhost')
            options.add_argument('--ignore-certificate-errors')
            if webdriver_major_version==4:
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service as ChromeService
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=options,**kwargs)
            elif webdriver_major_version<4:
                from webdriver_manager.chrome import ChromeDriverManager
                self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options,**kwargs)
            else:
                self.write_log("Not Conpatible Selenium Version")
            return
        elif serch_key("firefox",self.browser) or serch_key("ff",self.browser) or serch_key("fox",self.browser):
            # firefox
            fp = webdriver.FirefoxProfile()
            fp.set_preference("browser.download.dir", self.work_directory)
            for i in range(int(len(kwargs)/2)):
                fp.set_preference(kwargs[i*2],kwargs[i*2+1])
            if webdriver_major_version==4:
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from webdriver_manager.firefox import GeckoDriverManager
                self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),firefox_profile=fp,**kwargs)
            elif webdriver_major_version<4:
                from webdriver_manager.firefox import GeckoDriverManager
                self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),firefox_profile=fp,**kwargs)
            else:
                self.write_log("Not Conpatible Selenium Version")
        elif serch_key("brave",self.browser):
            # Brave
            if webdriver_major_version==4:
                from selenium.webdriver.chrome.service import Service as BraveService
                from webdriver_manager.chrome import ChromeDriverManager
                from webdriver_manager.core.utils import ChromeType
                self.driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),**kwargs)
            elif webdriver_major_version<4:
                from webdriver_manager.chrome import ChromeDriverManager
                from webdriver_manager.core.utils import ChromeType
                self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(),**kwargs)                
            else:
                self.write_log("Not Conpatible Selenium Version")
        elif serch_key("chromium",self.browser):
            # Chromium
            if webdriver_major_version==4:
                from selenium.webdriver.chrome.service import Service as ChromiumService
                from webdriver_manager.chrome import ChromeDriverManager
                from webdriver_manager.core.utils import ChromeType
                self.driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),**kwargs)
            elif webdriver_major_version<4:
                from webdriver_manager.chrome import ChromeDriverManager
                from webdriver_manager.core.utils import ChromeType
                self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),**kwargs)
            else:
                self.write_log("Not Conpatible Selenium Version")
        elif serch_key("edge",self.browser):
            # Edge
            if webdriver_major_version==4:
                from selenium.webdriver.edge.service import Service as EdgeService
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),**kwargs)
            elif webdriver_major_version<4:
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                self.driver = webdriver.Edge(EdgeChromiumDriverManager().install(),**kwargs)
            else:
                self.write_log("Not Conpatible Selenium Version")
        elif serch_key("ie",self.browser):
            # IE
            if webdriver_major_version==4:
                from selenium.webdriver.ie.service import Service as IEService
                from webdriver_manager.microsoft import IEDriverManager
                self.driver = webdriver.Ie(service=IEService(IEDriverManager().install()),**kwargs)
            elif webdriver_major_version<4:
                from webdriver_manager.microsoft import IEDriverManager
                self.driver = webdriver.Ie(IEDriverManager().install(),**kwargs)
            else:
                self.write_log("Not Conpatible Selenium Version")
        elif serch_key("opera",self.browser):
            # Opera
            try:
                from webdriver_manager.opera import OperaDriverManager
                self.driver = webdriver.Opera(executable_path=OperaDriverManager().install(),**kwargs)
            except:
                from webdriver_manager.opera import OperaDriverManager
                options = webdriver.ChromeOptions()
                options.add_argument('allow-elevated-browser')
                options.binary_location = "C:\\Users\\USERNAME\\FOLDERLOCATION\\Opera\\VERSION\\opera.exe"
                self.driver = webdriver.Opera(executable_path=OperaDriverManager().install(), options=options,**kwargs)
        else:
            self.write_log(f"Not Conpatible browser: {self.browser}")
            return
        self.driver.set_window_position(0,0)
        self.driver.set_window_size(size[0],size[1])

    def get_handle(
        self,
        num = -1  #  number of WindowHandle
    ):
        '''
        '''
        if num < 0:
            num = len(self.driver.window_handles) - 1 # latest handler
        self.driver.switch_to_window(self.driver.window_handles[num])
