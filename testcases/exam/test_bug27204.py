import os
import sys
from common.contants import basepage_dir, test_bug27204_dir
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


class Test_bug27204:
    with open(test_bug27204_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)
        setup_datas = datas[get_env()]
        test_check_add_plan_succeed_datas = datas["test_check_add_plan_succeed"]
        test_add_double_exam_datas = datas["test_add_double_exam"]

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


    @pytest.mark.parametrize("data", test_check_add_plan_succeed_datas)
    def test_check_add_plan_succeed(self, data):
        '''
        验证添加計劃成功
        '''

        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(data["plan_name"]).term().\
            upload_exists_plan_import(data["excel_path"]).\
            download_result().\
            goto_plan_details().\
            get_plan_name()
        assert data["expect"] in result

    @pytest.mark.parametrize("data", test_add_double_exam_datas)
    def test_add_double_exam(self,data):
        '''
        一次添加兩門科目
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]). \
            add_course_2(data["course_2"]).add_teacher_2(data["teacher_2"]).add_class_2(data["classdata_2"]). \
            add_student_exam(data["num"]).add_examdate(data["examdate"]).add_examtime(data["examtime"]). \
            add_roomCode(data["roomCode"]).add_invigilate_one(data["invigilate_one"]).\
            click_save(). \
            close_and_goto_plan_details(). \
            get_current_exam_total()
        assert data["expect"] == result