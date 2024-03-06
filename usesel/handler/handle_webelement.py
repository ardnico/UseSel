
from .handle_webdriver import handle_webdriver
import glob
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class handle_webelement(handle_webdriver):
    def __init__(
        self,
        **kwargs
    ):
        super().__init__(**kwargs)
    
    def get_elem(
        self,
        driver = None,
        key = '',  #  Search keyword
        method = 'xpath',  #  search method
        num = 3,  #  try count
        actions = [], # action e.g( action='send_keys:text' →　send_keys(text) )
    ):
        webdriver_major_version = int(webdriver.__version__.split(".")[0])
        reitem = None
        errornum = 0
        while errornum < num:
            errornum += 1
            try:
                if webdriver_major_version<4:
                    if method in ["class" ,"class_name","cn","classname"]:
                        reitem = driver.find_element_by_class_name(key)
                    elif method == "id":
                        reitem = driver.find_element_by_id(key)
                    elif method == "name":
                        reitem = driver.find_element_by_name(key)
                    elif method in ["link_text", "link", "lt", "linktext"]:
                        reitem = driver.find_element_by_link_text(key)
                    elif method == "partial_link_text":
                        reitem = driver.find_element_by_partial_link_text(key)
                    elif method in ["tag_name", "tagname", "tag"]:
                        reitem = driver.find_element_by_tag_name(key)
                    elif method == "xpath":
                        reitem = driver.find_element_by_xpath(key)
                    elif method in [ "css_selector", "css_selecter", "css", "cssselector", "cssselecter"]:
                        reitem = driver.find_element_by_css_selector(key)
                    else:
                        self.write_log("no such elements")
                else:
                    if method == "class" or method == "class_name" or method == "cn":
                        reitem = driver.find_element(By.CLASS_NAME,key)
                    elif method == "id":
                        reitem = driver.find_element(By.ID,key)
                    elif method == "name":
                        reitem = driver.find_element(By.NAME,key)
                    elif method == "link_text" or method == "link" or method == "lt":
                        reitem = driver.find_element(By.LINK_TEXT,key)
                    elif method == "partial_link_text":
                        reitem = driver.find_element(By.PARTIAL_LINK_TEXT,key)
                    elif method == "tag_name" or method == "tag":
                        reitem = driver.find_element(By.TAG_NAME,key)
                    elif method == "xpath":
                        reitem = driver.find_element(By.XPATH,key)
                    elif method == "css_selector" or method == "css" :
                        reitem = driver.find_element(By.CSS_SELECTOR,key)
                    else:
                        self.write_log("no such elements")
                for action in actions:
                    if len(action) == 0:
                        continue
                    try:
                        self.done_action(elem=reitem,action=action)
                    except Exception as e:
                        self.write_log(f"[FailedAction]{action}")
                        self.write_log(e)
                    break
                return reitem
            except Exception as e:
                time.sleep(2)
                if errornum > num:
                    raise Exception

    def done_action(self,elem,action):
        if action=="click":
            elem.click()
        elif action.find('send_keys')==0 or action.find('sendkeys')==0:
            keyword = action[action.find(":")+1:]
            print(keyword)
            elem.send_keys(keyword)
        elif action.find('select_by_index')==0:
            keyword = action[action.find(":")+1:]
            elem.select_by_index(keyword)
        elif action.find('select_by_visible_text')==0:
            keyword = action[action.find(":")+1:]
            elem.select_by_visible_text(keyword)
        elif action=='deselect_all':
            elem.deselect_all()
        elif action.find('deselect_by_index')==0:
            keyword = action[action.find(":")+1:]
            elem.deselect_by_index(keyword)
        elif action.find('deselect_by_value')==0:
            keyword = action[action.find(":")+1:]
            elem.deselect_by_value(keyword)
        elif action.find('deselect_by_visible_text')==0:
            keyword = action[action.find(":")+1:]
            elem.deselect_by_visible_text(keyword)
        elif action.find('click_and_hold')==0:
            keyword = action[action.find(":")+1:]
            elem.click_and_hold(keyword)
        elif action.find('move_to_element')==0:
            keyword = action[action.find(":")+1:]
            elem.move_to_element(keyword)
        elif action=='key_down' or action=='down':
            elem.key_down('key_down')
        elif action=='key_up' or action=='up':
            elem.key_down('key_up')
        else:
            print(f"unknown action {action}")
    

    def moveflame(
        self,
        driver = None,
        iflame = "",
        method = 'xpath'
    ):
        """_summary_

        Args:
            iflames (list, optional): iflame xpaths. Defaults to [].
            method (str, optional): Way to get the web elements. Defaults to 'xpath'.

        Returns:
            _type_: _description_
        """
        try:
            driver.switch_to.default_content()
        except:
            pass
        driver.switch_to.frame(iflame)

    def login(
        self,
        driver,
        url,
        set_name,
        paths:list, # specify the xpath(idbox,passwordbox,button,check)
        method="xpath",
        **kwargs
    ):
        if len(paths)!=4:
            waiting = input("specify the xpath(idbox,passwordbox,button,check)")
            raise Exception
        id, psw = self.config.get_id(set_name)
        actions = [
            f"send_keys:{id}",
            f"send_keys:{psw}",
            "click",
            ""
        ]
        driver.get(url)
        for num,action in enumerate(actions):
            self.get_elem(driver=driver,key=paths[num], method = method, actions=[action],**kwargs)
    
    def screenshot(
        self,
        driver = None,
        size = (640,640),
        name = 'ScreenShot',  #  name of screenshot
        expa = '.png'  #  extention
    ):
        try:
            files = glob.glob(fr'{self.config.work_directory}\{name}_*.{expa}')
            if len(files)==0:
                ssnum ="000"
            else:
                latest_num = files[-1].replace(fr"{self.config.work_directory}\{name}",'').replacer(f".{expa}")
                latest_num = int(latest_num)
                if latest_num == 1000:
                    self.write_log("[FailedToGetScreenShot]reached to upper limit")
                    raise Exception
                ssnum = str(latest_num + 1).zfill(3)
        except:
            import traceback
            traceback.print_exc()
            ssnum = '000'
        print("Screenshot number:",ssnum)
        filename = fr'{self.config.work_directory}\{name}_{ssnum}.{expa}'
        driver.set_window_size(size[0] , size[1])
        driver.save_screenshot(filename)

    def printhtml(
        self,
        driver = None,
        file_name = 'print'  #  fille name
    ):
        '''
        write as html file
        '''
        path = f'{file_name}.html'
        with open(path, mode='w', encoding="utf-8") as f:
            f.write(driver.page_source)
        return;
