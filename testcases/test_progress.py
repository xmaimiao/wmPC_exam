from page.main import Main


class TestProgress:
    def setup(self):
        self.main = Main()

    def test_event_student_stutas(self):
        staffNo="0409853A-S011-0911"
        result = self.main.goto_registration().\
            goto_progress().simple_search().\
            goto_firstevent_stulist().\
            simple_search(staffNo).\
            event_stutas(staffNo)
        assert result == "未完成"

    def test_history_operation_num(self):
        staffNo = "0409853A-S011-0911"
        result = self.main.goto_registration(). \
            goto_progress().simple_search(). \
            goto_firstevent_stulist(). \
            simple_search(staffNo).\
            goto_detail(staffNo).\
            operation_history()
        assert result == 1