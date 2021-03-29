from time import sleep

import win32con
import win32gui
from common.contants import add_exists_plan_dir
from page.basepage import BasePage
from page.examPage.exam_planPage.plan_details import Plan_Details


class Add_Exists_Plan(BasePage):
    def plan_name(self,plan_name):
        '''
        输入计划名称
        '''
        self._params["plan_name"] = plan_name
        self.step(add_exists_plan_dir,"plan_name")
        return self

    def term(self,term):
        '''
        选择学期
        '''
        self._params["term"] = term
        self.step(add_exists_plan_dir,"term")
        return self

    def exam_type(self,type):
        '''
        选择考試類型
        '''
        self._params["type"] = type
        self.step(add_exists_plan_dir,"exam_type")
        return self

    def upload_exists_plan_import(self,excel_path):
        '''
        上传附件
        '''
        self._params["excel_path"] = excel_path
        self.step(add_exists_plan_dir,"upload_exists_plan_import")
        sleep(2)
        # 找元素
        # 一级窗口"#32770","打开"
        dialog = win32gui.FindWindow("#32770", "打开")
        # 向下传递
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
        comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)  # 三级
        # 编辑按钮
        edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
        # 打开按钮
        button = win32gui.FindWindowEx(dialog, 0, 'Button', "打开(&O)")  # 二级

        # 输入文件的绝对路径，点击“打开”按钮
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, excel_path)  # 发送文件路径
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
        return self

    def check_upload_result(self):
        '''
        检查上传结果,判断“請通過校驗後提交”是否存在页面中，校驗失敗結果
        '''
        return self.step(add_exists_plan_dir,"check_upload_result")

    def check_upload_warn(self):
        '''
        检查上传结果,判断“警告信息”是否存在页面中，校驗存在N條警告信息
        '''
        return self.step(add_exists_plan_dir,"check_upload_warn")


    def download_result(self):
        '''
        下載錯誤文件
        '''
        try:
            self.step(add_exists_plan_dir,"download_result")
            return self
        except Exception as e:
            return self

    def goto_plan_details(self):
        '''
        点击保存
        进入计划详情页
        '''
        self.step(add_exists_plan_dir,"goto_plan_details")
        return Plan_Details(self._driver)

    def get_upload_fail_toast(self):
        '''
        獲取模板錯誤導入失敗的toast
        '''
        return (self.step(add_exists_plan_dir,"get_upload_fail_toast")).text


