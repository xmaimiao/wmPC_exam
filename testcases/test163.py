# from selenium import webdriver
# import os
# class Test163:
#     def test163(self):
#         chrome_driver = os.path.abspath("D:\Program Files (x86)\Google Chrome\chromedriver.exe")
#         os.environ["webdriver.chrome.driver"] = chrome_driver
#         chrome_capabilities = {
#             "browserName": "chrome",
#             "version": "",
#             "platform": "ANY",
#             "javascriptEnabled": True,
#             "webdriver.chrome.driver": chrome_driver
#         }
#         browser = webdriver.Remote("http://192.168.100.99:5555/wd/hub", desired_capabilities=chrome_capabilities)
#         browser.get("http://www.163.com")
#         print(browser.title)
#         browser.get_screenshot_as_file(r"d:/chrome.png")
#         browser.quit()
import pytest


@pytest.fixture()
def login(request):
    print("登录成功")
    print(request.param)

@pytest.mark.parametrize('a', ['user1', 'user2'])
@pytest.mark.parametrize('login', [(1, 2), (3, 4)], indirect=True)
def test_cart3(login,a):
    print("购物车用例3")