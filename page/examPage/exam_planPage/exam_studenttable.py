from common.contants import exam_studenttable_dir
from page.basepage import BasePage


class Exam_Studenttable(BasePage):

    def get_course_text(self):
        '''
        獲取“科目”字段文本
        '''
        result =  self.step(exam_studenttable_dir,"get_course_text")
        return self


    def get_the_first_student_courseCode(self):
        '''
        獲取第一行學生的科目編號
        '''
        return self.step(exam_studenttable_dir,"get_the_first_student_courseCode")

    def get_exam_title(self):
        '''
        獲取當前頁面的考試名稱（科目編號）
        '''
        result =  self.step(exam_studenttable_dir,"get_exam_title")
        return self