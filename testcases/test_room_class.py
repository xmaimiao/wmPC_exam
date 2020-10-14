from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class TestRoomClass:

    chrome_options = Options()
    # 和瀏覽器打開的調試端口進行通信
    # 瀏覽器要使用 --remote-debugging-port=9222 開啟調試
    chrome_options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=chrome_options)
    # self._driver = webdriver.Chrome()
    # driver.maximize_window()
    driver.implicitly_wait(3)

    driver.find_element(By.XPATH,'//div[@class="we-sider-menu app-sider-menu"]//span[contains(text(),"課室課表(本科)")]').click()
    ele = driver.find_element(By.XPATH,'//*[@class="content"]/div[2]/div//span')
    ActionChains(driver).move_to_element(ele).perform()
    driver.find_element(By.XPATH,'//i[@class="ivu-icon ivu-icon-ios-close-circle ivu-select-arrow"]').click()

    driver.implicitly_wait(5)
    driver.find_element(By.XPATH,'//*[@class="date-picker-icon"]/img').click()
    driver.find_element(By.XPATH,'//*[@class="ivu-date-picker-header-label"][1]').click()
    driver.find_element(By.XPATH,'//*[@class="ivu-picker-panel-content"]//*[contains(text(),"2020")]').click()
    driver.find_element(By.XPATH,'//*[@class="ivu-picker-panel-content"]//*[contains(text(),"9")]').click()
    driver.find_element(By.XPATH,'//*[@class="ivu-picker-panel-content"]//*[contains(text(),"20")]').click()
    driver.find_element(By.XPATH,'//*[@class="ivu-input ivu-input-default"]').send_keys("BP12107")
    driver.find_element(By.XPATH,'//*[@class="ivu-input-group-append ivu-input-search"]/i').click()
    sleep(2)
    # driver.find_element(By.XPATH,'//span[contains(text(),"D1")]/..//*[contains(text(),"BP12107")]').click()

if __name__ == '__main__':
    TestRoomClass()