#coding=utf-8
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class DynamicJSHandler(object):
    
    def __init__(self,**kwargs):
        
        self.driver = self.init_chrome_headless()
        
        #传入的参数
        for k,v in kwargs.items():
            setattr(self,k,v)
    
    #设置chrome headless
    def init_chrome_headless(self):
        #设置谷歌浏览器的选项
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("lang=zh_CN.UTF-8")
        #驱动的路径
        exe_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"driver","chromedriver")
#         print exe_path
        #声明浏览器
        return webdriver.Chrome(executable_path=exe_path,chrome_options=chrome_options)
    
    
    def test_method(self):
        self.driver.get("https://www.baidu.com/")
        #获得整个访问页面
        page_source = self.driver.page_source
        #当前url
        current_url = self.driver.current_url
        #
        current_window_handle = self.driver.current_window_handle
        
        #查找元素：方法很多
        elements_a = self.driver.find_elements_by_tag_name("a")
        for a in elements_a:
            print(a.text,a.get_property("href"))
    
    def handle_iframe(self,data_container):
        try:
            elements_iframe = self.driver.find_elements_by_tag_name("iframe")
            for i,iframe in enumerate(elements_iframe,0):
                self.driver.switch_to.frame(i)
                elements_a = self.driver.find_elements_by_tag_name("a")
                for a in elements_a:
                    temp_count = 3
                    while temp_count > 0:
                        try:
                            data_container.append((a.text,a.get_attribute("title"),a.get_attribute("href")))
                            break
                        except:
                            temp_count -= 1
    #                         self.driver.implicitly_wait(3)
                            try:
                                WebDriverWait(self.driver,3).until(EC.visibility_of(a))
                            except: 
                                time.sleep(3)
                        
    #             self.handle_iframe(data_container)
                
                #返回默认frame
                self.driver.switch_to.default_content()
        except Exception as e:
            print(e)
            
    def get_label_a(self,url):
        try:
            try:
                self.driver.get(url)
            except TimeoutException:
                return []
            elements_a = self.driver.find_elements_by_tag_name("a")
            data_container = []
            self.driver.maximize_window()
    #         self.driver.implicitly_wait(8)
            for a in elements_a:
    #             print(a.text,a.get_property("href"))
    #             try:
    #                 WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located(a.text))
    #                 data_container.append((a.text,a.get_attribute("title"),a.get_attribute("href")))
    #                 #print driver.find_element_by_link_text('CSDN').get_attribute('href')
    #             except:
    #                 continue 
                temp_count = 3
                while temp_count > 0:
                    try:   
                        data_container.append((a.text,a.get_attribute("title"),a.get_attribute("href")))
                        break
                    except:
                        temp_count -= 1
    #                         self.driver.implicitly_wait(3)
                        try:
                            WebDriverWait(self.driver,3).until(EC.visibility_of(a))
                        except: 
                            time.sleep(3)
                    
            
            self.handle_iframe(data_container)
        except Exception as e:
            print(e)
            
        return data_container
        
    #with 方式使用的实现
    def __enter__(self):
        
        return self
    
    def __exit__(self,*args,**kwargs):
        
        self.driver.quit()