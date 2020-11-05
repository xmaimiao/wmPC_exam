from common.contants import exampage_dir
from page.basepage import BasePage
from page.examPage.exam_planPage.exam_plan import Exam_Plan
from page.examPage.room_setting.room_setting import Room_Setting


class ExamPage(BasePage):
    def goto_exam_plan(self):
        '''
        打开排考计划
        '''
        self.step(exampage_dir,"goto_exam_plan")
        return Exam_Plan(self._driver)

    def goto_room_setting(self):
        '''
        打开考室分配
        '''
        self.step(exampage_dir,"goto_room_setting")
        return Room_Setting(self._driver)

    def get_memu_num(self):
        '''
        用於權限測試，獲取考試應用的菜單數量
        '''
        return len(self.step(exampage_dir,"get_memu_num"))

