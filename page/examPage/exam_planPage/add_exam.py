from selenium.webdriver.common.by import By

from common.contants import add_exam_dir
from page.basepage import BasePage


class Add_Exam(BasePage):
    def add_examCode(self,examCode):
        '''
        填写排考编号
        :param examCode: 排考编号
        '''
        self._params["examCode"] = examCode
        self.step(add_exam_dir,"add_examCode")
        return self

    def add_course_1(self,course_1):
        '''
        填写科目编码、科目名称
        :param course:科目编码、科目名称
        '''
        self._params["course_1"] = course_1
        self.step(add_exam_dir,"add_course_1")
        return self

    def add_course_2(self,course_2):
        '''
        添加第二门科目用
        :param course:科目编码、科目名称
        '''
        self._params["course_2"] = course_2
        self.step(add_exam_dir,"add_course_2")
        return self


    def add_teacher_1(self,teacher_1):
        '''
        填写授课教师
        :param teacher: 授课教师，传进来数组
        '''
        for teacher in teacher_1:
            self._params["teacher"] = teacher
            self.step(add_exam_dir,"add_teacher_1")
        return self

    # def add_teacher_2(self,teacher_2):
    #     '''
    #     添加第二门科目用
    #     :param teacher2: 授课教师，传进来数组
    #     '''
    #     self._params["teacher_2"] = teacher_2
    #     for t in teacher_2:
    #         self.step(add_exam_dir,"add_teacher_2")
    #     return self

    def add_class(self,classdatas):
        '''
        添加班别
        :param classdata: 班别，传进来数组
        '''
        for classdata in classdatas:
            self.step(add_exam_dir, "add_class_click_input")
            try:
                self._params["classdata"] = classdata
                # 根據文本text查找元素會存在多個xxxE1xx元素
                eles = self.step(add_exam_dir,"add_class")
                for ele in eles:
                    # 其中某些元素不可操作，故要判斷，加異常處理抛出異常，繼續執行
                    if ele.is_displayed():
                        try:
                            ele.click()
                        except Exception as e:
                            pass
                    continue
            except Exception as e:
                print("該考試科目已存在，無班別")
                raise e
        return self

    # def add_class2(self,classdata2):
    #     '''
    #     添加第二门科目用，班别
    #     :param classdata: 班别，传进来数组
    #     '''
    #     self._params["classdata2"] = classdata2
    #     for c in classdata2:
    #         self.step()
    #     return self

    def add_student_exam(self,num):
        '''
        分配考试人数，不同排考編號科目使用
        :param num: 人数
        '''
        self._params["num"] = num
        self.step(add_exam_dir,"add_student_exam")
        return self

    def add_grade(self,grade):
        '''
        添加年级,不同排考科目編號使用
        :param grade:年级
        '''
        self._params["grade"] = grade
        self.step(add_exam_dir,"add_grade")
        return self

    def add_examdate(self,examdate):
        '''
        添加考试日期，不同排考科目編號使用
        :param date: 日期，yyyy-mm-dd
        '''
        self._params["examdate"] =examdate
        self.step(add_exam_dir,"add_examdate")
        return self

    def add_examdate_same_examCode(self,examdate):
        '''
        添加考试日期,同排考編號和睦用
        :param date: 日期，yyyy-mm-dd
        '''
        self._params["examdate"] =examdate
        self.step(add_exam_dir,"add_examdate_same_examCode")
        return self

    def add_examtime(self,examtime):
        '''
        添加考试时间，不同排考科目編號使用
        :param time: 时间格式15:00 - 16:00
        '''
        self._params["examtime"] = examtime
        self.step(add_exam_dir,"add_examtime")
        return self

    def add_roomCode(self,roomCode):
        '''
        添加考场，不同排考科目編號使用
        :param room: 考室编号
        '''
        self._params["roomCode"] = roomCode
        self.step(add_exam_dir,"add_roomCode")
        return self

    def add_roomCode_same_examCode(self,roomCode):
        '''
        添加考场，同排考科目編號使用
        :param room: 考室编号
        '''
        self._params["roomCode"] = roomCode
        self.step(add_exam_dir,"add_roomCode_same_examCode")
        return self

    def add_invigilate_one(self,invigilate_one):
        '''
        添加监考员1，不同排考科目編號使用
        '''
        self._params["invigilate_one"] = invigilate_one
        self.step(add_exam_dir,"add_invigilate_one")
        return self

    def add_invigilate_two(self,invigilate_two):
        '''
        添加监考员2，不同排考科目編號使用
        '''
        self._params["invigilate_two"] = invigilate_two
        self.step(add_exam_dir,"add_invigilate_two")
        return self

    def add_invigilate_three(self,invigilate_three):
        '''
        添加监考员3，不同排考科目編號使用
        '''
        self._params["invigilate_three"] = invigilate_three
        self.step(add_exam_dir,"add_invigilate_three")
        return self

    def add_invigilate_four(self,invigilate_four):
        '''
        添加监考员4，不同排考科目編號使用
        '''
        self._params["invigilate_four"] = invigilate_four
        self.step(add_exam_dir,"add_invigilate_four")
        return self

    def add_invigilate_one_same_examCode(self, invigilate_one):
        '''
        添加监考员1，不同排考科目編號使用
        '''
        self._params["invigilate_one"] = invigilate_one
        self.step(add_exam_dir, "add_invigilate_one_same_examCode")
        return self

    def add_invigilate_two_same_examCode(self, invigilate_two):
        '''
        添加监考员2，不同排考科目編號使用
        '''
        self._params["invigilate_two"] = invigilate_two
        self.step(add_exam_dir, "add_invigilate_two_same_examCode")
        return self

    def add_invigilate_three_same_examCode(self, invigilate_three):
        '''
        添加监考员3，不同排考科目編號使用
        '''
        self._params["invigilate_three"] = invigilate_three
        self.step(add_exam_dir, "add_invigilate_three_same_examCode")
        return self

    def add_invigilate_four_same_examCode(self, invigilate_four):
        '''
        添加监考员4，不同排考科目編號使用
        '''
        self._params["invigilate_four"] = invigilate_four
        self.step(add_exam_dir, "add_invigilate_four_same_examCode")
        return self

    def add_exam_ruletype_open_book(self):
        '''
        修改考試形式：開卷，不同排考科目編號使用
        '''
        self.step(add_exam_dir,"add_exam_ruletype_open_book")
        return self

    def click_save(self):
        '''
        保存表单，不同排考科目編號使用
        '''
        self.step(add_exam_dir,"click_save")
        return self

    def click_save_same_examCode(self):
        '''
        保存表单
        '''
        self.step(add_exam_dir,"click_save_same_examCode")
        return self

    def check_add_succeed(self):
        '''
        :return: 保存成功
        '''
        result = self.step(add_exam_dir, "check_add_succeed")
        self.step(add_exam_dir, "click_close")
        return result


    def check_add_failed(self):
        '''
        :return: 保存失敗，獲取提失敗提示語
        '''
        result = self.step(add_exam_dir, "check_add_failed")
        self.step(add_exam_dir, "click_close")
        return result

    def get_same_examCode_end_toast(self):
        '''
        存在排考編號科目A，已結束考試，創建同科目A的排考編號考試，獲取警告toast
        '''
        return self.step(add_exam_dir, "get_same_examCode_end_toast")

    def close_and_goto_plan_details(self):
        self.step(add_exam_dir, "click_close")
        from page.examPage.exam_planPage.plan_details import Plan_Details
        return Plan_Details(self._driver)