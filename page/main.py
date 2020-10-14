from common.contants import exampage_dir
from page.basepage import BasePage
from page.index import Index
from page.loginpage import Login


class Main(BasePage):
    '''
    首頁面po
    '''
    # _base_url = "http://wmstaff-entry.doocom.net/home"
    # _base_url = "https://oa.must.edu.mo/home/"
    # _base_url = "https://oa-wmtest.must.edu.mo:10443/home/"

    def goto_login(self):
        '''
        進去登錄頁面
        :return:
        '''
        return Login(self._driver)

    def goto_index(self):
        '''
        打開首頁
        :return:
        '''
        return Index(self._driver)



    def goto_exam_plan(self):
        '''
        測試入口，打開考試
        '''
        self.set_implicitly_wait(5)
        self.step(exampage_dir,"goto_exam_plan")
        from page.examPage.exam_planPage.exam_plan import Exam_Plan
        return Exam_Plan(self._driver)
