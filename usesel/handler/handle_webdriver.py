
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .._config import config

webdriver_minor_version = int(webdriver.__version__.split(".")[1])
if webdriver_minor_version<10:
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.microsoft import IEDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager

webdriver_major_version = int(webdriver.__version__.split(".")[0])
if webdriver_major_version>=4:
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from selenium.webdriver.edge.service import Service as EdgeService
    from selenium.webdriver.ie.service import Service as IEService

def serch_key(key,line):
    return re.search(key,line, flags=re.IGNORECASE)

class handle_webdriver(object):
    config = config()
    def __init__(
        self,
        **kwargs
        ):
        """_summary_

        Args:
            work_directory (str, optional): work directory for browser. Defaults to '<CurentDirectory>\<YYYYMMDD>'.
        """
        super().__init__()
        
    def write_log(self,text):
        tmp_time = self.config.get_date_str_ymdhms()
        try:
            with open(self.config.log,"a",encoding="utf-8") as f:
                f.write(f"[{tmp_time}]{text}\n")
        except:
            with open(self.config.log,"a",encoding="shift-jis") as f:
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
        options = Options()
        if serch_key("chrome",self.config.browser):
            # Google Chrome
            if webdriver_major_version==4:
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),**kwargs)
            elif webdriver_major_version<4:
                if webdriver_minor_version > 9:
                    driver = webdriver.Chrome(**kwargs)
                else:
                    driver = webdriver.Chrome(ChromeDriverManager().install(),**kwargs)
            else:
                self.write_log("Not Conpatible Selenium Version")
        elif serch_key("headless_chrome",self.config.browser):
            # Google (HeadlessMode))
            options.add_argument('--headless')
            options.add_argument('--allow-insecure-localhost')
            options.add_argument('--ignore-certificate-errors')
            if webdriver_major_version==4:
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=options,**kwargs)
            elif webdriver_major_version<4:
                driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options,**kwargs)
            else:
                self.write_log("Not Conpatible Selenium Version")
            return
        elif serch_key("firefox",self.config.browser) or serch_key("ff",self.config.browser) or serch_key("fox",self.config.browser):
            # firefox
            fp = webdriver.FirefoxProfile()
            fp.set_preference("browser.download.dir", self.config.work_directory)
            for i in range(int(len(kwargs)/2)):
                fp.set_preference(kwargs[i*2],kwargs[i*2+1])
            if webdriver_major_version==4:
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),firefox_profile=fp,**kwargs)
            elif webdriver_major_version<4:
                if webdriver_minor_version > 9:
                    driver = webdriver.Firefox(**kwargs)
                else:
                    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),firefox_profile=fp,**kwargs)
            else:
                self.write_log("Not Conpatible Selenium Version")
        elif serch_key("edge",self.config.browser):
            # Edge
            if webdriver_major_version==4:
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),**kwargs)
            elif webdriver_major_version<4:
                if webdriver_minor_version > 9:
                    driver = webdriver.Edge(**kwargs)
                else:
                    driver = webdriver.Edge(EdgeChromiumDriverManager().install(),**kwargs)
            else:
                self.write_log("Not Conpatible Selenium Version")
        elif serch_key("ie",self.config.browser):
            # IE
            if webdriver_major_version==4:
                driver = webdriver.Ie(service=IEService(IEDriverManager().install()),**kwargs)
            elif webdriver_major_version<4:
                if webdriver_minor_version > 9:
                    driver = webdriver.Ie()
                else:
                    driver = webdriver.Ie(IEDriverManager().install(),**kwargs)
            else:
                self.write_log("Not Conpatible Selenium Version")
        else:
            self.write_log(f"Not Conpatible browser: {self.config.browser}")
            return
        driver.set_window_position(0,0)
        driver.set_window_size(size[0],size[1])
        return driver

    def get_handle(
        self,
        driver = None,
        name = "", # title
    ):
        '''
        '''
        if driver is None:
            print("please specify the web driver")
            raise Exception
        if name == "":
            driver.switch_to_window(driver.window_handles[-1])
            return
        
        if driver.title == name:
            return

        for handle in driver.window_handles:
            driver.switch_to_window(handle)
            if driver.title == name:
                return
        
