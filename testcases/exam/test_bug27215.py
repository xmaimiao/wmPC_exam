import os
import sys
from common.contants import basepage_dir, test_bug27215_dir
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


class Test_bug27215:
    with open(test_bug27215_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)
        setup_datas = datas[get_env()]
        test_check_upload_exists_plan_datas = datas["test_check_upload_exists_plan"]
        test_check_add_plan_succeed_datas = datas["test_check_add_plan_succeed"]
        test_add_exam_datas = datas["test_add_exam"]
        test_add_exam_false_datas = datas["test_add_exam_false"]

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

    @pytest.mark.parametrize("data", test_check_upload_exists_plan_datas)
    def test_check_upload_exists_plan(self, data):
        '''
        验证上传已排计划
        '''

        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(data["plan_name"]).term(data["term"]).\
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
            plan_name(data["plan_name"]).term(data["term"]).\
            upload_exists_plan_import(data["excel_path"]).\
            download_result().\
            goto_plan_details().\
            get_plan_name()
        assert data["expect"] in result

    @pytest.mark.parametrize("data", test_add_exam_datas)
    def test_add_exam(self, data):
        '''
        验证添加考試科目
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]).\
            add_examdate(data["examdate"]).add_examtime(data["examtime"]). \
            add_roomCode(data["roomCode"]).\
            click_save().close_and_goto_plan_details(). \
            get_current_exam_total()
        assert data["expect"] == result

    @pytest.mark.parametrize("data", test_add_exam_false_datas)
    def test_add_exam_false(self, data):
        '''
        验证添加考試科目失敗，獲取失敗提示語
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]).\
            add_examdate(data["examdate"]).add_examtime(data["examtime"]). \
            add_roomCode(data["roomCode"]).\
            click_save().check_add_failed()
        assert data["expect"] == result

