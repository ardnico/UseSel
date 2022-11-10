
from .encrypter import Enc
import os
from glob import glob
from getpass import getpass
from datetime import datetime as dt

class config:
    __enc = Enc()
    
    def __init__(self,
                 id_data_path=fr"{os.getcwd()}\data",
                 work_dir = os.getcwd(),
                 browser = "chrome",
                 ) -> None:
        self.id_data_path = id_data_path
        self.get_id()
        self.work_directory = fr'{work_dir}\{self.get_date_str_ymd()}'
        os.makedirs(self.work_directory,exist_ok=True)
        self.browser = browser
        self.log = fr"{self.work_directory}\usesel_log.log"
        
    def get_date_str_ymd(self) -> str:
        return dt.now().strftime('%Y%m%d')
    
    def get_date_str_ymdhms(self) -> str:    
        return dt.now().strftime('%Y/%m/%d %H:%M:%S')
    
    def set_id(self,set_name) -> None:
        if len(set_name) == 0:
            print("please set the parameter: set_name")
            raise Exception
        id_file = fr"{self.id_data_path}\id_{set_name}.data"
        psw_file = fr"{self.id_data_path}\psw_{set_name}.data"
        if os.path.exists(id_file):
            os.remove(id_file)
        if os.path.exists(psw_file):
            os.remove(psw_file)
        id = input("input ID:")
        psw = getpass("input Password:")
        self.id_data[set_name] = [id,psw]
        tmp_id = self.__enc.encrypt(self.id_data[set_name][0])
        tmp_psw = self.__enc.encrypt(self.id_data[set_name][1])
        with open(id_file,"w") as f:
            f.write(tmp_id)
        with open(psw_file,"w") as f:
            f.write(tmp_psw)
    
    def get_id(self) -> str:
        id_files = glob(fr"{self.id_data_path}\id_*.data")
        self.id_data = {}
        for id_file in id_files:
            tmp_set_name = id_file.replace(fr"{self.id_data_path}\id_","").replace(".data","")
            with open(id_file,"r") as f:
                tmp_id = f.read()
            tmp_id = self.__enc.decrypt(tmp_id)
            psw_file = fr"{self.id_data_path}\psw_{tmp_set_name}.data"
            with open(psw_file,"r") as f:
                tmp_psw = f.read()
            tmp_psw = self.__enc.decrypt(tmp_psw)
            self.id_data[tmp_set_name] = [tmp_id,tmp_psw]
    
    def check_file(self,set_name) -> bool:
        id_file = fr"{self.id_data_path}\id_{set_name}.data"
        return os.path.exists(id_file)
    
    def del_id(self,set_name) -> None:
        id_file = fr"{self.id_data_path}\id_{set_name}.data"
        psw_file = fr"{self.id_data_path}\psw_{set_name}.data"
        if os.path.exists(id_file):
            os.remove(id_file)
        if os.path.exists(psw_file):
            os.remove(psw_file)
        del self.id_data[set_name]
            
    def set_browser(self,browser:str):
        try:
            browser = browser.lower()
        except:
            pass
        self.browser = browser
        
    def get_browser(self) -> str:
        return self.browser  
          
    def set_work_directory(self,work_directory):
        self.work_directory = work_directory
        
    def get_work_directory(self):
        return self.work_directory
    
    def set_log(self,log):
        self.log = log
        
    def get_log(self):
        return self.log  
          