import re
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from common.contants import plan_details_dir
from page.basepage import BasePage
from page.examPage.exam_planPage.add_exam import Add_Exam


class Plan_Details(BasePage):
    def goto_add_exam(self):
        '''
        点击“添加”按钮
        '''
        try:
            self.step(plan_details_dir,"goto_add_exam")
            return Add_Exam(self._driver)
        except NoSuchElementException as e:
            print('該計劃已結束，沒有“添加"按鈕')
            raise e


    def get_plan_name(self):
        '''
        :return: 返回計劃名稱
        '''
        sleep(2)
        try:
            return self.step(plan_details_dir,"get_plan_name")
        except NoSuchElementException as e:
            print("已排計劃存在錯誤數據，上傳失敗！")
            raise e

    def get_current_exam_total(self):
        '''
        獲取當前考試科目數據量
        '''
        result = self.step(plan_details_dir,"get_current_data_total")
        return int(re.search('(\d+).*?(\d+).*',result).group(2))

    def get_same_examdate_courses(self,examdate):
        '''
        獲取相同考試時間的科目
        '''
        self._params["examdate"] = examdate
        return self.step(plan_details_dir,"get_same_examdate_courses")

