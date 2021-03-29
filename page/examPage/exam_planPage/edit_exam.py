import shelve

from common.contants import edit_exam_dir
from page.basepage import BasePage


class Edit_Exam(BasePage):
    def wait_sleep(self,sleeps):
        self.sleep(sleeps)
        return self

    def edit_examdate(self,examdate):
        '''
        添加考试日期，不同排考科目編號使用，注意：日期》=当前日期
        :param date: 日期，yyyy-mm-dd
        '''
        self._params["examdate"] =examdate
        self.step(edit_exam_dir,"edit_examdate")
        return self

    def edit_examtime(self,examtime):
        '''
        添加考试时间，不同排考科目編號使用
        :param time: 时间格式15:00 - 16:00
        '''
        self._params["examtime"] = examtime
        self.step(edit_exam_dir,"edit_examtime")
        return self

    def edit_roomCode(self,roomCode):
        '''
        添加考场，不同排考科目編號使用
        :param room: 考室编号
        '''
        self._params["roomCode"] = roomCode
        is_hasroom = (self.step(edit_exam_dir,"is_hasroom")).get_attribute("placeholder")
        if is_hasroom != "請選擇":
            self.step(edit_exam_dir,"clear_roomCode")
        self.step(edit_exam_dir,"edit_roomCode")
        return self

    def edit_invigilate_one(self,invigilate_one):
        '''
        添加监考员1，不同排考科目編號使用
        通过before_invigilate_one判断是否已有监考员，有则删除
        通过invigilate_one判断是否为空，为空则监考员1为空保存
        '''
        db = shelve.open("invigilates")
        before_invigilate_one = db["invigilates"]["invigilate_one"]
        self._params["invigilate_one"] = invigilate_one
        if before_invigilate_one != "--":
            self.step(edit_exam_dir,"delete_invigilate_one")
        if invigilate_one != '':
            self.step(edit_exam_dir,"edit_invigilate_one")
        db.close()
        return self

    def edit_invigilate_two(self,invigilate_two):
        '''
        添加监考员2，不同排考科目編號使用
        '''
        db = shelve.open("invigilates")
        before_invigilate_two = db["invigilates"]["invigilate_two"]
        self._params["invigilate_two"] = invigilate_two
        if before_invigilate_two != "--":
            self.step(edit_exam_dir, "delete_invigilate_two")
        if invigilate_two != '':
            self.step(edit_exam_dir, "edit_invigilate_two")
        db.close()
        return self

    def edit_invigilate_three(self,invigilate_three):
        '''
        添加监考员3，不同排考科目編號使用
        '''
        db = shelve.open("invigilates")
        before_invigilate_three = db["invigilates"]["invigilate_three"]
        self._params["invigilate_three"] = invigilate_three
        if before_invigilate_three != "--":
            self.step(edit_exam_dir, "delete_invigilate_three")
        if invigilate_three != '':
            self.step(edit_exam_dir, "edit_invigilate_three")
        db.close()
        return self

    def edit_invigilate_four(self,invigilate_four):
        '''
        添加监考员4，不同排考科目編號使用
        '''
        db = shelve.open("invigilates")
        before_invigilate_four = db["invigilates"]["invigilate_four"]
        self._params["invigilate_four"] = invigilate_four
        if before_invigilate_four != "--":
            self.step(edit_exam_dir, "delete_invigilate_four")
        if invigilate_four != '':
            self.step(edit_exam_dir, "edit_invigilate_four")
        db.close()
        return self

    def click_save(self):
        '''
        保存表单，不同排考科目編號使用
        '''
        self.step(edit_exam_dir,"click_save")
        return self

    def check_edit_succeed(self):
        '''
        :return: 保存成功
        '''
        result = self.step(edit_exam_dir, "check_edit_succeed")
        self.step(edit_exam_dir, "click_close")
        return result


    def check_edit_failed(self):
        '''
        :return: 保存失敗，獲取提失敗提示語
        '''
        result = self.step(edit_exam_dir, "check_edit_failed")
        print(f"添加考試保存失敗：{result}")
        self.step(edit_exam_dir, "click_close")
        return "保存失敗"

    def close_and_goto_plan_details(self):
        self.step(edit_exam_dir, "click_close")
        from page.examPage.exam_planPage.plan_details import Plan_Details
        return Plan_Details(self._driver)