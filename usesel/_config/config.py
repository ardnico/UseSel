
from .encrypter import Enc
import os
import tkinter as tk
from getpass import getpass
from datetime import datetime as dt
import tkinter as tk
from tkinter import simpledialog

def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    # Get ID input
    user_id = simpledialog.askstring("Input", "Enter your ID:")
    if user_id is None:
        return None  # User canceled input
    # Get password input (masked)
    user_password = simpledialog.askstring("Input", "Enter your password:", show="*")
    if user_password is None:
        return None  # User canceled input
    return user_id, user_password


class config:
    __enc = Enc()
    
    def __init__(self,
                 id_data_path=fr"{os.getcwd()}\data",
                 work_dir = os.getcwd(),
                 browser = "chrome",
                 ) -> None:
        self.id_data_path = id_data_path
        self.work_directory = fr'{work_dir}\{self.get_date_str_ymd()}'
        os.makedirs(self.work_directory,exist_ok=True)
        self.browser = browser
        self.log = fr"{self.work_directory}\usesel_log.log"
    
    def get_date_str_ymd(self) -> str:
        return dt.now().strftime('%Y%m%d')
    
    def get_date_str_ymdhms(self) -> str:    
        return dt.now().strftime('%Y/%m/%d %H:%M:%S')
    
    def set_id(self,set_name,dialogmode=0) -> None:
        if len(set_name) == 0:
            print("please set the parameter: set_name")
            raise Exception
        id_file = fr"{self.id_data_path}\id_{set_name}.data"
        psw_file = fr"{self.id_data_path}\psw_{set_name}.data"
        if os.path.exists(id_file):
            os.remove(id_file)
        if os.path.exists(psw_file):
            os.remove(psw_file)
        if dialogmode == 0:
            id = input("input ID:")
            psw = getpass("input Password:")
        else:
            id,psw = get_user_input()
        tmp_id = self.__enc.encrypt(id)
        tmp_psw = self.__enc.encrypt(psw)
        with open(id_file,"w") as f:
            f.write(tmp_id)
        with open(psw_file,"w") as f:
            f.write(tmp_psw)
    

    def get_id(self,set_name,dialogmode=0) -> str:
        id_path = fr"{self.id_data_path}\id_{set_name}.data"
        if os.path.exists(id_path):
            with open(id_path,"r") as f:
                tmp_id = f.read()
            tmp_id = self.__enc.decrypt(tmp_id)
            psw_file = fr"{self.id_data_path}\psw_{set_name}.data"
            with open(psw_file,"r") as f:
                tmp_psw = f.read()
            tmp_psw = self.__enc.decrypt(tmp_psw)
            return tmp_id, tmp_psw
        else:
            self.set_id(set_name,dialogmode)
            self.get_id(set_name,dialogmode)
    
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
    