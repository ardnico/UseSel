
from .handle_webdriver import handle_webdriver
from .util import Enc
import os
import glob
import time
from selenium import webdriver
from datetime import datetime as dt
from getpass import getpass



class handle_webelement(handle_webdriver):
    def __init__(
        self,
        id_data_path=fr"{os.getcwd()}\data",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.id_data_path = id_data_path
        id_files = glob.glob(fr"{id_data_path}\id_*.data")
        self.id_data = {}
        enc = Enc()
        for id_file in id_files:
            tmp_set_name = id_file.replace(id_data_path,"").replace(".data","").replace("id_","")
            with open(id_file,"r") as f:
                tmp_id = f.read()
            tmp_id = enc.decrypt(tmp_id)
            psw_file = fr"{id_data_path}\psw_{tmp_set_name}.data"
            with open(psw_file,"r") as f:
                tmp_psw = f.read()
            tmp_psw = enc.decrypt(tmp_psw)
            self.id_data[tmp_set_name] = [tmp_id,tmp_psw]
    
    def set_id(self,set_name):
        if len(set_name) == 0:
            print("please set the parameter: set_name")
            raise Exception
        id_file = fr"{self.id_data_path}\data\id_{set_name}.data"
        psw_file = fr"{self.id_data_path}\data\psw_{set_name}.data"
        if os.path.exists(id_file):
            os.remove(id_file)
        if os.path.exists(psw_file):
            os.remove(psw_file)
        id = input("input ID:")
        psw = getpass("input Password:")
        self.id_data[set_name] = [id,psw]
        enc = Enc()
        tmp_id = enc.encrypt(self.id)
        tmp_psw = enc.encrypt(self.pssw)
        with open(self.id_file,"w") as f:
            f.write(tmp_id)
        with open(self.psw_file,"w") as f:
            f.write(tmp_psw)
    
    def del_id(self,set_name):
        id_file = fr"{self.id_data_path}\data\id_{set_name}.data"
        psw_file = fr"{self.id_data_path}\data\psw_{set_name}.data"
        if os.path.exists(id_file):
            os.remove(id_file)
        if os.path.exists(psw_file):
            os.remove(psw_file)
        del self.id_data[set_name]
    
    def done_action(elem,action):
        if action=="click":
            elem.click()
        elif action.find('send_keys')==0 or action.find('sendkeys')==0:
            tmp_key = action.split(":")[0]
            keyword = action.replace(f"{tmp_key}:","")
            elem.sendkeys(keyword)
        elif action.find('select_by_index')==0:
            keyword = action.replace('select_by_index:',"")
            elem.select_by_index(keyword)
        elif action.find('select_by_visible_text')==0:
            keyword = action.replace('select_by_visible_text:',"")
            elem.select_by_visible_text(keyword)
        elif action=='deselect_all':
            elem.deselect_all()
        elif action.find('deselect_by_index')==0:
            keyword = action.replace('deselect_by_index:',"")
            elem.deselect_by_index(keyword)
        elif action.find('deselect_by_value')==0:
            keyword = action.replace('deselect_by_value:',"")
            elem.deselect_by_value(keyword)
        elif action.find('deselect_by_visible_text')==0:
            keyword = action.replace('deselect_by_visible_text:',"")
            elem.deselect_by_visible_text(keyword)
        elif action.find('click_and_hold')==0:
            keyword = action.replace('click_and_hold:',"")
            elem.click_and_hold(keyword)
        elif action.find('move_to_element')==0:
            keyword = action.replace('move_to_element:',"")
            elem.move_to_element(keyword)
        elif action=='key_down' or action=='down':
            elem.key_down('key_down')
        elif action=='key_up' or action=='up':
            elem.key_down('key_up')
        else:
            print(f"unknown action {action}")
    
    
    def get_elem(
        self,
        key = '',  #  Search keyword
        method = 'xpath',  #  search method
        num = 3,  #  try count
        actions = [], # action e.g( action='send_keys:text' →　send_keys(text) )
    ):
        webdriver_major_version = int(webdriver.__version__.split(".")[0])
        reitem = None
        errornum = 0
        while errornum < num:
            try:
                if webdriver_major_version<4:
                    if method == "class" or method == "class_name" or method == "cn":
                        reitem = self.driver.find_element_by_class_name(key)
                    elif method == "id":
                        reitem = self.driver.find_element_by_id(key)
                    elif method == "name":
                        reitem = self.driver.find_element_by_name(key)
                    elif method == "link_text" or method == "link" or method == "lt":
                        reitem = self.driver.find_element_by_link_text(key)
                    elif method == "partial_link_text":
                        reitem = self.driver.find_element_by_partial_link_text(key)
                    elif method == "tag_name" or method == "tag":
                        reitem = self.driver.find_element_by_tag_name(key)
                    elif method == "xpath":
                        reitem = self.driver.find_element_by_xpath(key)
                    elif method == "css_selector" or method == "css" :
                        reitem = self.driver.find_element_by_css_selector(key)
                    else:
                        self.write_log("no such elements")
                else:
                    from selenium.webdriver.common.by import By
                    if method == "class" or method == "class_name" or method == "cn":
                        reitem = self.driver.find_elements(By.CLASS_NAME,key)
                    elif method == "id":
                        reitem = self.driver.find_elements(By.ID,key)
                    elif method == "name":
                        reitem = self.driver.find_elements(By.NAME,key)
                    elif method == "link_text" or method == "link" or method == "lt":
                        reitem = self.driver.find_elements(By.LINK_TEXT,key)
                    elif method == "partial_link_text":
                        reitem = self.driver.find_elements(By.PARTIAL_LINK_TEXT,key)
                    elif method == "tag_name" or method == "tag":
                        reitem = self.driver.find_elements(By.TAG_NAME,key)
                    elif method == "xpath":
                        reitem = self.driver.find_elements(By.XPATH,key)
                    elif method == "css_selector" or method == "css" :
                        reitem = self.driver.find_elements(By.CSS_SELECTOR,key)
                    else:
                        self.write_log("no such elements")
                for action in actions:
                    try:
                        self.done_action(reitem,action)
                    except Exception as e:
                        self.write_log(f"[FailedAction]{action}")
                        self.write_log(e)
                    break
            except:
                time.sleep(2)
                errornum += 1
                if errornum > num:
                    raise Exception
        return reitem;

    def moveflame(
        self,
        iflames:list = [],
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
            self.driver.switch_to.default_content()
        except:
            pass
        for flame in iflames:
            iframe = self.get_elem(
                key=flame,
                method=method
            )
            self.driver.switch_to.frame(iframe)

    def login(
        self,
        url,
        set_name,
        id_path,
        psw_path,
        button_path,
        check_path,
        method="xpath",
        **kwargs
    ):
        tmp_id_data = self.id_data[set_name]
        paths = [
            id_path,
            psw_path,
            button_path,
            check_path,
        ]
        actions = [
            f"send_keys:{tmp_id_data[0]}",
            f"send_keys:{tmp_id_data[1]}",
            "click",
            ""
        ]
        self.driver.get(url)
        for num,action in enumerate(actions):
            self.get_elem(key=paths[num], method = method, actions=[action],**kwargs)
    
    def screenshot(
        self,
        size = (640,640),
        name = 'ScreenShot',  #  name of screenshot
        expa = '.png'  #  extention
    ):
        todate = dt.now().strftime('%Y%m%d')
        os.makedirs(todate,exist_ok=True)
        
        try:
            files = glob.glob(fr'{self.work_directory}\{todate}\{name}_*.{expa}')
            if len(files)==0:
                ssnum ="000"
            else:
                latest_num = files[-1].replace(fr"{self.work_directory}\{todate}\{name}",'').replacer(f".{expa}")
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
        filename = fr'{self.work_directory}\{todate}\{name}_{ssnum}.{expa}'
        self.driver.set_window_size(size[0] , size[1])
        self.driver.save_screenshot(filename)

    def printhtml(
        self,
        file_name = 'print'  #  fille name
    ):
        '''
        write as html file
        '''
        path = f'{file_name}.html'
        with open(path, mode='w', encoding="utf-8") as f:
            f.write(self.driver.page_source)
        return;
