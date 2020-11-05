from selenium.webdriver.common.by import By


def handlie_blacklist(func):
    def wrapper(*args, **kwargs):
        _blacklist = [
            # (By.XPATH, '//*[@class="ivu-drawer-wrap we-drawer"]/div/div/div/div[3]/i'),
            # (By.XPATH, '//*[@class="quit-btn ivu-btn ivu-btn-default"]/span'),
            (By.XPATH, '//*[@name="submit"]'),
            # (By.XPATH, '//*[@class="layui-layer-btn0"]'),
            # (By.XPATH, '//*[@id="cboxClose"]')
        ]
        _leave_confirm = (By.XPATH,'//*[@class="subbox"]/input[@class="submit"]')
        _max_err_num = 3
        _error_num = 0
        # 裝飾器會默認把self當第0個參數傳進來
        from page.basepage import BasePage
        instance : BasePage = args[0]
        try:
            result = func(*args, **kwargs)
            _error_num = 0
            # 恢復為等待3s
            instance.set_implicitly_wait(3)
            return result
        except Exception as e:
            # 等待時間過長，先處理為1s
            instance.set_implicitly_wait(1)
            # 如果没找到，就进行黑名单处理
            if _error_num > _max_err_num:
                # 如果 erro 次数大于指定指，清空 error 次数并报异常
                _error_num = 0
                raise e
            _error_num += 1
            for ele in _blacklist:
                eles = instance.finds(*ele)
                if len(eles) > 0:
                    eles[0].click()
                    # 特殊處理，針對請假彈出“在計算請假天數”警告框，點擊確認繼續流程
                    if ele[1] in _blacklist[2][1]:
                        instance.find(*_leave_confirm).click()
                    return wrapper(*args, **kwargs)
            raise ValueError("元素不在黑名單中")
    return wrapper