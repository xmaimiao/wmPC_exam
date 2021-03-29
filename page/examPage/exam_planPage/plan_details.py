import re
import shelve
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from common.contants import plan_details_dir
from page.basepage import BasePage
from page.examPage.exam_planPage.add_exam import Add_Exam
from page.examPage.exam_planPage.edit_exam import Edit_Exam
from page.examPage.exam_planPage.exam_studenttable import Exam_Studenttable


class Plan_Details(BasePage):

    def wait_sleep(self,sleeps):
        self.sleep(sleeps)
        return self

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

    def edit_exam_of_num(self,num):
        '''
        通过传入的序号“num“定位编辑第N调数据
        '''
        try:
            self._params["num"] = num
            self.step(plan_details_dir,"edit_exam_of_num")
            return Edit_Exam(self._driver)
        except NoSuchElementException as e:
            print('該考试已結束，沒有“编辑"按鈕')
            raise e


    def get_plan_name(self):
        '''
        :return: 返回text "當前計劃:"
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

    def goto_the_first_exam_studenttable(self):
        '''
        打開第一行的考試，進入學生清單
        '''
        self.step(plan_details_dir,"goto_the_first_exam_studenttable")
        return Exam_Studenttable(self._driver)

    def del_plan(self):
        '''
        進入計劃詳情，刪除該計劃
        先判斷”刪除“按鈕仍在，在即刪除，否則抛出錯誤
        '''
        try:
            self.step(plan_details_dir,"del_plan")
            from page.examPage.exam_planPage.exam_plan import Exam_Plan
            return Exam_Plan(self._driver)
        except Exception as e:
            print("該頁面沒有刪除按鈕！")
            raise e

    def del_exam(self,num):
        '''
        進入計劃詳情，根據num定位第N條數據的“刪除”按鈕
        先判斷”刪除“按鈕仍在，在即刪除，否則抛出錯誤
        '''
        self._params["num"] = num
        # 獲取當前考試科目數據量,存入數據庫中
        db = shelve.open("exam_total")
        result = self.step(plan_details_dir,"get_current_data_total")
        exam_total = int(re.search('(\d+).*?(\d+).*',result).group(2))
        db["exam_total"] = exam_total
        db.close()
        try:
            self.step(plan_details_dir,"del_exam")
            return self
        except Exception as e:
            print("該頁面沒有刪除按鈕！")
            raise e

    def get_invigilate(self, num):
        '''
        通过参数：计划名称，打开该计划详情
        '''
        self._params["num"] = num
        invigilates={}
        invigilates["invigilate_one"] = self.step(plan_details_dir, "get_invigilate_one")
        invigilates["invigilate_two"] = self.step(plan_details_dir, "get_invigilate_two")
        invigilates["invigilate_three"] = self.step(plan_details_dir, "get_invigilate_three")
        invigilates["invigilate_four"] = self.step(plan_details_dir, "get_invigilate_four")
        db = shelve.open("invigilates")
        db["invigilates"] = invigilates
        db.close()
        return self

