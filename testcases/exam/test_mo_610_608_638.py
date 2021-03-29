import datetime
import os
import shelve
import sys
from common.contants import basepage_dir, test_mo_610_608_638_dir
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
        datas = yaml.safe_load(f)
        wm_env = datas["default"]
        setup_datas = datas[wm_env]
        return setup_datas


class Test_Mo_610_608_638:
    with open(test_mo_610_608_638_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)
        test_add_examroom_datas = datas["test_add_examroom"]
        test_delete_examroom_datas = datas["test_delete_examroom"]
        test_check_upload_exists_plan_datas = datas["test_check_upload_exists_plan"]
        test_check_add_plan_succeed_datas = datas["test_check_add_plan_succeed"]
        test_student_del_or_T_style_datas = datas["test_student_del_or_T_style"]

    # 獲取當前的時間
    _now_time = datetime.datetime.now()
    _setup_datas = get_env()
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
                username(self._setup_datas["username"]).password(self._setup_datas["password"]).save(). \
                goto_application(). \
                goto_exam(self._setup_datas["application"])

        def teardown_class(self):
            '''
            非調試端口啓用
            '''
            self.main.close()

    # 前置條件準備------》

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

    # 後置條件清楚數據------》

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

    # 測試用例部分------》
    @pytest.mark.parametrize("data", test_check_upload_exists_plan_datas)
    def test_check_upload_exists_plan(self, data):
        '''
        验证上传已排计划
        '''

        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(self._now_time.strftime('%m%d')+data["plan_name"]).term(data["term"]). \
            exam_type(data["type"]). \
            upload_exists_plan_import(data["excel_path"]).\
            download_result().\
            check_upload_result()
        assert result == data["expect"]

    @pytest.mark.parametrize("data", test_check_add_plan_succeed_datas)
    def test_check_add_plan_succeed(self, data):
        '''
        验证添加計劃成功
        '''

        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(self._now_time.strftime('%m%d')+data["plan_name"]).term(data["term"]). \
            exam_type(data["type"]). \
            upload_exists_plan_import(data["excel_path"]).\
            download_result().\
            goto_plan_details().\
            get_plan_name()
        assert data["expect"] in result

    @pytest.mark.parametrize("data", test_student_del_or_T_style_datas)
    def test_student_del_or_T_style(self, data):
        '''
        验证從”按學生查詢“移除學生
        '''
        result = self.main.goto_search_of_student().\
            simple_search_student(data["user_s"]).\
            del_the_fir_student().\
            get_the_fir_username_style().get_the_fir_del_button
        # 讀取數據庫
        db = shelve.open("username_style")
        username_style = db["username_style"]
        db.close()
        # 驗證無刪除按鈕
        pytest.assume( data["expect"] == result )
        # 驗證樣式變化
        pytest.assume( username_style == "text-decoration: line-through;" )


