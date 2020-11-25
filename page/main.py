import yaml

from common.contants import exampage_dir, main1_dir, basepage_dir
from page.basepage import BasePage, _get_working
from page.examPage.search_of_student.search_of_student import Search_Of_Student
from page.index import Index
from page.loginpage import Login


class Main(BasePage):
    '''
    首頁面po
    '''
    _working = _get_working()

    with open(basepage_dir, encoding="utf-8") as f:
        env = yaml.safe_load(f)
        if _working != "port":
            _base_url = env["docker_env"][env["default"]]

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

    def back_to_index(self):
        '''
        在其他應用回到首頁
        :return:
        '''
        self.step(main1_dir,"back_to_index")
        return Index(self._driver)



    def goto_exam_plan(self):
        '''
        測試入口，打開考試計劃
        '''
        self.set_implicitly_wait(5)
        self.step(exampage_dir,"goto_exam_plan")
        from page.examPage.exam_planPage.exam_plan import Exam_Plan
        return Exam_Plan(self._driver)

    def goto_room_setting(self):
        '''
        打开考室分配
        '''
        self.step(exampage_dir,"goto_room_setting")
        from page.examPage.room_setting.room_setting import Room_Setting
        return Room_Setting(self._driver)

    def goto_search_of_student(self):
        '''
        打開“按學生查詢”菜單
        '''
        self.step(exampage_dir, "goto_search_of_student")
        return Search_Of_Student(self._driver)


