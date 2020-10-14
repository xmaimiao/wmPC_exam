from selenium.webdriver.common.by import By

from page.index import Index
from page.main import Main


class TestAuthsNewStuList:
    name = "test12"
    pas = "wemust123"
    application_name = "入學"
    staffNo = "1102853A-S011-0262"

    def setup_class(self):
        self.main = Main()

    def teardown_class(self):
        self.main.quit()

    def setup(self):
        self.index = self.main.goto_index()

    def teardown(self):
        self.index.backto_index()

    def test_menus_noexist(self):
        result = self.main.goto_login().\
            username(self.name).password(self.pas).save().\
            goto_application().\
            goto_registration(self.application_name).\
            goto_newstulist()
        assert result == False

    def test_export(self):
        result = self.main.goto_login(). \
            username(self.name).password(self.pas).save(). \
            goto_application(). \
            goto_registration(self.application_name).\
            goto_newstulist().\
            export()
        assert result == False

    def test_detail(self):
        result = self.main.goto_login(). \
            username(self.name).password(self.pas).save(). \
            goto_application(self.application_name). \
            goto_result = self.main.goto_login(). \
            username(self.name).password(self.pas).save(). \
            goto_application(). \
            goto_registration(self.application_name).\
            goto_newstulist().goto_detail_nosearch()
        print(f"打印result：{result}")
        assert result == "-"

    def test_student_detail(self):
        result = self.main.goto_login(). \
            username(self.name).password(self.pas).save(). \
            goto_application(self.application_name). \
            goto_result = self.main.goto_login(). \
            username(self.name).password(self.pas).save(). \
            goto_application(). \
            goto_registration(self.application_name). \
            goto_newstulist(). \
            simple_search(self.staffNo). \
            goto_details(self.staffNo).\
            goto_event_detail()
        assert result == False

    def test_eventdetail_edit(self):
        result = self.main.goto_login(). \
            username(self.name).password(self.pas).save(). \
            goto_application(self.application_name). \
            goto_result = self.main.goto_login(). \
            username(self.name).password(self.pas).save(). \
            goto_application(). \
            goto_registration(self.application_name). \
            goto_newstulist(). \
            simple_search(self.staffNo). \
            goto_details(self.staffNo).\
            edit_dress()
        assert result == False






