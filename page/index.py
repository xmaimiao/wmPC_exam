from common.contants import index_dir
from page.application import Application
from page.basepage import BasePage


class Index(BasePage):

    def goto_application(self):
        self.step(index_dir,"goto_application")
        return Application(self._driver)
