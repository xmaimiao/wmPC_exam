from common.contants import application_dir
from page.basepage import BasePage
from page.examPage.exampage import ExamPage


class Application(BasePage):

    def goto_exam(self, application):
        '''
        進入考试應用
        '''
        self._params["application"] = application
        self.step(application_dir, "goto_exam")
        return ExamPage(self._driver)


