from common.contants import exampage_dir
from page.basepage import BasePage
from page.examPage.exam_planPage.exam_plan import Exam_Plan


class ExamPage(BasePage):
    def goto_exam_plan(self):
        '''
        打开排考计划
        '''
        self.step(exampage_dir,"goto_exam_plan")
        return Exam_Plan(self._driver)

