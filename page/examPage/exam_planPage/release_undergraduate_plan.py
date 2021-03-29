from common.contants import release_undergraduate_plan_dir
from page.basepage import BasePage


class Release_Undergraduate_Plan(BasePage):
    def wait_sleep(self,sleeps):
        self.sleep(sleeps)
        return self

    def release_for_date(self,date_list):
        '''
        通過考試日期定位要發佈的考試
        '''
        for date in date_list:
            self._params["date"] = date
            self.step(release_undergraduate_plan_dir,"release_for_date")
        return self

    def teacher_view_date(self,date_t):
        '''
        選擇教師可看到發佈考試科目的日期
        '''
        self._params["date_t"] = date_t
        self.step(release_undergraduate_plan_dir,"teacher_view_date")
        return self

    def student_view_date(self,date_s):
        '''
        選擇學生可看到發佈考試科目的日期
        '''
        self._params["date_s"] = date_s
        self.step(release_undergraduate_plan_dir,"student_view_date")
        return self

    def release_all(self):
        '''
        發佈全部的考試計劃
        '''
        self.step(release_undergraduate_plan_dir,"release_all")
        return self

    def click_release(self):
        '''
        點擊”發佈“按鈕
        '''
        self.step(release_undergraduate_plan_dir,"click_release")
        from page.examPage.exam_planPage.exam_plan import Exam_Plan
        return Exam_Plan(self._driver)