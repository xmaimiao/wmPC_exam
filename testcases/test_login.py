import pytest

from page.main import Main


class TestLogin:

    _name = "test11"
    _psd = "123456"

    def setup_class(self):
        self.main = Main()

    def teardown_class(self):
        self.main.close()

    def setup(self):
        self.login = self.main.goto_login().username(self._name).password(self._psd).save()

    def teardown(self):
        self.main.quit()

    @pytest.mark.parametrize("name,psd",[("test12","wemust123"),("test11","123456")])
    @pytest.mark.skip
    def testlogin(self,name,psd):
        '''
        測試登錄功能
        :return:
        '''
        self.main.goto_login().username(name).password(psd).save()

    def test_selectapplication(self):
        '''
        測試打開選擇應用的頁面
        :return:
        '''
        self.login.goto_application()

    def test_gotoapplication(self):
        '''
        測試打開某個應用
        :return:
        '''
        application_name = "課表"
        memu = "教師課表(本科)"
        self.login.goto_application().\
            goto_classtimetable(application_name). \
            goto_teacher_management_degree(memu)

