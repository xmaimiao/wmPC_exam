import json
import logging
from time import sleep

import yaml
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page.handle_black import handlie_blacklist


class BasePage:
    _driver = None
    _params={}
    _base_url = ""
    _index_ele = (By.XPATH,'//*[@class="common-app-header environment-dev"]/div[2]/div[1]/a[1]')
    _menber_ele = (By.XPATH,'//*[@class="link-button user-info"]/span')
    _quit_ele = (By.XPATH,'//*[@class="link-button user-info"]/../../div[2]//li[last()]')
    logging.basicConfig(level=logging.INFO)

    def __init__(self,driver:WebDriver = None):
        if driver is None:

            # 和瀏覽器打開的調試端口進行通信，瀏覽器要使用 --remote-debugging-port=9222 開啟調試
            chrome_options = Options()
            chrome_options.debugger_address = "127.0.0.1:9222"
            self._driver = webdriver.Chrome(options=chrome_options)

            # 普通方式打开浏览器
            # self._driver = webdriver.Chrome()

            #Docker+Selenium Grid+Python搭建分布式测试环境
            # chrome_driver = os.path.abspath("D:\Program Files (x86)\Google Chrome\chromedriver.exe")
            # os.environ["webdriver.chrome.driver"] = chrome_driver
            # chrome_capabilities = {
            #     "browserName": "chrome",
            #     "version": "",
            #     "platform": "ANY",
            #     "javascriptEnabled": True,
            #     "webdriver.chrome.driver": chrome_driver
            # }
            # self._driver = webdriver.Remote(
            #     command_executor='http://192.168.99.100:5555/wd/hub',
            #     desired_capabilities=chrome_capabilities)

            self._driver.maximize_window()
            self._driver.implicitly_wait(3)
        else:
            self._driver = driver

        if self._base_url != "":
            self._driver.get(self._base_url)

    @handlie_blacklist
    def find(self,by,locator):
        logging.info(f"find：{locator}")
        if by == None:
            result=self._driver.find_element(*locator)
        else:
            result = self._driver.find_element(by,locator)
        return result

    def finds(self,by,locator):
        logging.info(f"find_eles：{locator}")
        return self._driver.find_elements(by,locator)

    def move_to_ele(self,by,locator):
        '''
        模擬鼠標懸停
        '''
        return ActionChains(self._driver).move_to_element(self.find(by,locator)).perform()

    def find_and_click(self,by,locator):
        logging.info(f"click：{locator}")
        self.find(by,locator).click()

    def find_and_sendkeys(self,by,locator,value):
        logging.info(f"sendkeys：{value}")
        self.find(by,locator).send_keys(value)

    def action_click(self,by,locator):
        ActionChains(self._driver).click(self.find(by,locator)).perform()

    def webdriver_wait(self,by,locator,timeout=10):
        '''
        等待元素出現
        '''
        logging.info(f"webdriver_wait：{locator},timeout：{timeout}")
        WebDriverWait(self._driver, timeout).until(lambda x:x.find_element(by,locator))

    def wait_for_click(self,by,locator,timeout=10):
        ''''
        等待元素可出現且可點擊
        '''
        logging.info(f"wait_for_click：{locator},timeout：{timeout}")
        WebDriverWait(self._driver,timeout).until(expected_conditions.element_to_be_clickable((by,locator)))

    # def click_until_next_ele_display(self,by,locator,by_next,locator_next,timeout=10):
    #     '''
    #     不斷點擊當前元素直到下一個元素出現，停止點擊
    #     '''
    #     logging.info(f"click_until_next_ele_display：{locator},timeout：{timeout}")
    #     elements_len = len(self.finds(by_next,locator_next))
    #     if elements_len <= 0:
    #         self.find_and_click(by,locator)
    #     return elements_len >0

    def wait_for_display(self,by,locator,timeout=10):
        '''
        等待元素出現，一旦出現就不斷查找元素，用於獲取toast
        '''
        logging.info(f"wait_for_display：{locator},timeout：{timeout}")
        stutas = WebDriverWait(self._driver, timeout).until(expected_conditions.visibility_of_element_located((by,locator)))
        if stutas:
            ele= self.find(by,locator)
            return ele
        return ValueError("元素不存在")

    def find_ele_status(self,by,locator):
        '''
        用来判断元素标签是否存在
        '''
        logging.info(f"find_ele_status：{locator}")
        try:
            self.find(by, locator)
        except Exception as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True

    def sleep(self,time):
        sleep(time)

    # def execute_script_sendkeys(self,script):
    #     '''
    #     通过js查找元素，并传入sendkeys
    #     '''
    #     self._driver.execute_script(f'{script}')
    #
    # def execute_script_click(self,script):
    #     '''
    #     通过js查找元素，并click
    #     '''
    #     ele = self._driver.execute_script(f'{script}')
    #     ele.click()


    def wait_for_condition(self,condition,timeout=10):
        '''
        等待直到xxx條件成立
        '''
        logging.info(f"wait_for_condition：{condition}")
        WebDriverWait(self._driver, timeout).until(condition)

    def set_implicitly_wait(self,second):
        '''
        顯性等待
        '''
        self._driver.implicitly_wait(second)

    def backto_index(self):
        logging.info(f"backto_index")
        self.find_and_click(*self._index_ele)

    def quit(self):
        self.find_and_click(*self._menber_ele)
        self.find_and_click(*self._quit_ele)

    def close(self):
        self._driver.quit()

    def step(self,path,name):
        with open(path, encoding="utf-8") as f:
            steps = yaml.safe_load(f)[name]
        # ${}的參數轉化
        raw_data = json.dumps(steps)
        for key,value in self._params.items():
            raw_data = raw_data.replace("${"+key+"}",str(value))
        steps = json.loads(raw_data)
        for step in steps:
            if "action" in step.keys():
                action = step["action"]
                if "wait_click" == action:
                    self.wait_for_click(step["by"],step["locator"])
                if "wait" == action:
                    self.webdriver_wait(step["by"], step["locator"])
                if "send" == action:
                    self.find_and_sendkeys(step["by"], step["locator"], step["value"])
                if "click" == action:
                    self.find_and_click(step["by"],step["locator"])
                if "len" == action:
                    eles = self.finds(step["by"], step["locator"])
                    return len(eles)
                if "text" == action:
                    text = self.find(step["by"], step["locator"]).text
                    return text
                if "clear" == action:
                    self.find(step["by"], step["locator"]).clear()
                if "wait_display" == action:
                    ele = self.wait_for_display(step["by"], step["locator"])
                    return ele
                if "move" == action:
                    self.move_to_ele(step["by"], step["locator"])
                if "ele_status" == action:
                    return self.find_ele_status(step["by"], step["locator"])
                if "sleep" == action:
                    sleep(step["locator"])
                if "action_click" == action:
                    self.action_click(step["by"], step["locator"])
                if "eles" == action:
                    return self.finds(step["by"], step["locator"])


