import sys
sys.path.append('..')
import pytest
from page.main import Main


class TestNewStuList:
    staffNo = "1909853E-B311-0011"
    # staffNo = "1909853E-B211-0048"

    def setup(self):
        self.main = Main()


    def test_gotoregistration(self):

        staffNo="1209853A-S011-0193"
        self.main.goto_registration().goto_newstulist().simple_search(staffNo)

    def test_guideresult(self):

        result= self.main.goto_registration().goto_newstulist().\
            simple_search(self.staffNo).search_result_guide(self.staffNo)
        result = result
        assert "0/1" == result

    def test_group(self):
        # staffNo = "1102853A-S011-0262"
        result = self.main.goto_registration().goto_newstulist(). \
            simple_search(self.staffNo).search_result_groupinsurance(self.staffNo)
        assert "未完成" == result


    def test_progress(self):
        # staffNo = "1102853A-S011-0262"
        result = self.main.goto_registration().goto_newstulist(). \
            simple_search(self.staffNo).search_result_progress(self.staffNo)
        assert "4/5" == result


    def test_status(self):
        # staffNo = "1102853A-S011-0262"
        result = self.main.goto_registration().goto_newstulist(). \
            simple_search(self.staffNo).search_result_progress_status(self.staffNo)
        assert "完成 " == result

    def test_export(self):
        result = self.main.goto_registration().goto_newstulist().export()
        assert "數據導出中，請稍後..." == result


    def test_detail_firstevent(self):
        # staffNo = "1102853A-S011-0262"
        result = self.main.goto_registration().goto_newstulist(). \
            simple_search(self.staffNo).goto_details(self.staffNo).first_event()
        assert "拍照" == result


    def test_detail_lastevent(self):
        # staffNo = "1102853A-S011-0262"
        # staffNo = "1009853A-S011-1016"
        result = self.main.goto_registration().goto_newstulist(). \
            simple_search(self.staffNo).goto_details(self.staffNo).last_event()
        assert "保险申请表" == result


    def test_detail_editadress(self):
        adress = "南山一階"
        result = self.main.goto_registration().\
            goto_newstulist(). simple_search(self.staffNo).\
            goto_details(self.staffNo).edit_dress(adress)
        assert  result == '更改成功'

    def test_eventrepeat(self):
        # staffNo = "1209853A-S012-0031"
        '''
        这个用例运行出错，后期需要看一下
        :return:
        '''
        value = "PC端重置"
        result = self.main.goto_registration(). \
            goto_newstulist().simple_search(self.staffNo). \
            goto_details(self.staffNo).\
            goto_event_detail().\
            repeat(value)
        assert result == 1

    def history_oper_number(self):
        '''
        此用例没运行过
        :return:
        '''
        # staffNo = "1209853A-S012-0031"
        expect = 2
        result = self.main.goto_registration(). \
            goto_newstulist().simple_search(self.staffNo). \
            goto_details(self.staffNo). \
            goto_event_detail().\
            operation_history()
        assert result == expect


        '''
        sockect在應用層去抓，但是不關心永什麽協議。不對傳輸的數據做校驗
        TSL是對ssl的標準化，websocket實際上用的還是http，走charles，應用層的協議，web socket官網有代碼，可以仿寫一下
        http衹是在socket上做封裝而已，socket更加底層，屬於傳輸層和網絡層？
        charles map
        作爲服務器研究wire mock
        map local截獲curl命令'''
