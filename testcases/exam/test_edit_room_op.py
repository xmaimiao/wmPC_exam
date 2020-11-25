import datetime
import os
import shelve
import sys
from common.contants import test_edit_room_dir, basepage_dir
from page.basepage import _get_working

curPath = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_dir)
sys.path.append('..')
from page.main import Main
import pytest
import yaml

def get_env():
    '''
    获取环境变量：uat、dev、mo正式站
    '''
    with open(basepage_dir, encoding="utf-8") as f:
        return yaml.safe_load(f)["default"]

class Test_Exam_Plan:
    with open(test_edit_room_dir, encoding="utf-8") as f:

        datas = yaml.safe_load(f)
        setup_datas = datas[get_env()]
        test_add_examroom_datas = datas["test_add_examroom"]
        test_delete_examroom_datas = datas["test_delete_examroom"]
        test_edit_examroom_datas = datas["test_edit_examroom"]



    _working = _get_working()
    if _working == "port":
        def setup(self):
            '''
            開啓調試端口啓用
            '''
            self.main = Main()
    else:
        def setup_class(self):
            '''
            非調試端口用
            '''
            self.main = Main().goto_login(). \
                username(self.setup_datas["username"]).password(self.setup_datas["password"]).save(). \
                goto_application(). \
                goto_exam(self.setup_datas["application"])

        def teardown_class(self):
            '''
            非調試端口啓用
            '''
            self.main.close()

    @pytest.mark.parametrize("data", test_add_examroom_datas)
    def test_add_examroom(self, data):
        '''
        验证添加考室
        '''

        result = self.main.goto_room_setting().\
            add_room().edit_roomCode(data["room"]).\
            edit_seatCount(data["seatCount"]).\
            edit_faculty(data["faculty"]).\
            click_save()
        assert result == data["expect"]

    @pytest.mark.parametrize("data", test_delete_examroom_datas)
    def test_delete_examroom(self, data):
        '''
        验证刪除考室
        '''

        result = self.main.goto_room_setting(). \
            search_roomCode(data["room_keys"]).\
            delect_the_first_room().get_current_datacount()
        db = shelve.open("room_total")
        before_room_total = db["room_total"]
        db.close()
        assert result == before_room_total - 1

    @pytest.mark.parametrize("data", test_edit_examroom_datas)
    def test_edit_examroom(self, data):
        '''
        验证編輯考室
        '''

        result = self.main.goto_room_setting(). \
            search_roomCode(data["room_keys"]).\
            edit_the_first_room(). \
            edit_seatCount(data["seatCount"]). \
            edit_startSn_and_endSn(data["startSn"]). \
            click_save()
        assert result == data["expect"]