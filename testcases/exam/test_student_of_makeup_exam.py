import datetime
import os
import shelve
import sys
from common.contants import basepage_dir, test_student_of_makeup_exam_dir
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


class Test_Student_Of_Makeup_Exam:
    with open(test_student_of_makeup_exam_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)
        test_check_upload_exists_plan_datas = datas["test_check_upload_exists_plan"]
        test_check_upload_exists_plan_makeup_datas = datas["test_check_upload_exists_plan_makeup"]
        test_del_exam_plan_datas = datas["test_del_exam_plan"]
        test_check_add_plan_succeed_datas = datas["test_check_add_plan_succeed"]
        test_check_add_plan_fail_datas = datas["test_check_add_plan_fail"]
        test_add_exam1_datas = datas["test_add_exam1"]
        test_add_exam2_datas = datas["test_add_exam2"]
        test_add_exam3_datas = datas["test_add_exam3"]
        test_student_for_del_datas = datas["test_student_for_del"]
        test_student_del_or_T_style_datas = datas["test_student_del_or_T_style"]

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

    @pytest.mark.parametrize("data", test_check_upload_exists_plan_datas)
    def test_check_upload_exists_plan(self, data):
        '''
        验证上传補考计划
        '''

        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(data["plan_name"]).term(data["term"]).\
            exam_type(data["type"]).\
            upload_exists_plan_import(data["excel_path"]).\
            download_result().\
            check_upload_result()
        assert result == data["expect"]

    @pytest.mark.parametrize("data", test_del_exam_plan_datas)
    def test_del_exam_plan(self,data):
        '''
        驗證刪除考試計劃
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            del_plan().get_ele_of_addplan()
        assert result == data["expect"]

    @pytest.mark.parametrize("data", test_check_add_plan_succeed_datas)
    def test_check_add_plan_succeed(self, data):
        '''
        验证添加計劃成功
        '''
        result = self.main.goto_exam_plan(). \
            add_exists_plan(). \
            plan_name(self._now_time.strftime('%m%d')+data["plan_name"]).term(data["term"]). \
            exam_type(data["type"]). \
            upload_exists_plan_import(data["excel_path"]). \
            download_result(). \
            goto_plan_details(). \
            get_plan_name()
        assert data["expect"] in result

    #補考與其他計劃的衝突，已存在補考計劃11
    @pytest.mark.parametrize("data", test_check_upload_exists_plan_makeup_datas)
    def test_check_upload_exists_plan_makeup(self, data):
        '''
        验证上传考試计划
        '''

        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(data["plan_name"]).term(data["term"]).\
            exam_type(data["type"]).\
            upload_exists_plan_import(data["excel_path"]).\
            download_result().\
            check_upload_result()
        assert result == data["expect"]


    #其他计划添加/编辑考试科目冲突，已存在考試計劃61
    @pytest.mark.parametrize("data", test_add_exam1_datas)
    def test_add_exam1(self, data):
        '''
        验证添加考試科目
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]).add_student_exam(data["num"]). \
            add_examdate(data["examdate"]).add_examtime(data["examtime"]). \
            add_roomCode(data["roomCode"]). \
            click_save().check_add_failed()
        assert data["expect"] in result

    #其他计划添加/编辑考试科目冲突，已存在考試計劃61
    @pytest.mark.parametrize("data", test_add_exam2_datas)
    def test_add_exam2(self, data):
        '''
        验证添加考試科目
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]).add_student_exam(data["num"]).\
            add_examdate(data["examdate"]).add_examtime(data["examtime"]). \
            add_invigilate_one(data["invigilate_one"]).\
            click_save().check_add_failed()
        assert data["expect"] == result

    #其他计划添加/编辑考试科目冲突，已存在考試計劃61
    @pytest.mark.parametrize("data", test_add_exam3_datas)
    def test_add_exam3(self, data):
        '''
        验证添加考試科目
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]).\
            add_examdate(data["examdate"]).add_examtime(data["examtime"]). \
            click_save().check_add_failed()
        assert data["expect"] in result

    @pytest.mark.parametrize("data", test_check_add_plan_fail_datas)
    def test_check_add_plan_fail(self, data):
        '''
        验证模板有問題，導入失敗
        '''

        result = self.main.goto_exam_plan(). \
            add_exists_plan(). \
            plan_name(data["plan_name"]).term(data["term"]). \
            exam_type(data["type"]). \
            upload_exists_plan_import(data["excel_path"]). \
            get_upload_fail_toast()
        assert data["expect"] in result

    @pytest.mark.parametrize("data", test_student_for_del_datas)
    def test_student_for_del(self, data):
        '''
        验证學生移除/T 后無刪除按鈕，樣式變化
        '''
        result = self.main.goto_search_of_student().\
            simple_search_student(data["user_s"]).del_the_fir_student().\
            wait_sleep(1).get_the_fir_username_style().get_the_fir_del_button()
        # 讀取數據庫
        db = shelve.open("username_style")
        username_style = db["username_style"]
        db.close()
        # 驗證無刪除按鈕
        pytest.assume( data["expect"] == result )
        # 驗證樣式變化
        pytest.assume( username_style == "text-decoration: line-through;" )

    @pytest.mark.parametrize("data", test_student_del_or_T_style_datas)
    def test_student_del_or_T_style(self, data):
        '''
        验证從”按學生查詢“移除學生
        '''
        result = self.main.goto_search_of_student().\
            simple_search_student(data["user_s"]).\
            del_the_fir_student().\
            wait_sleep(1).get_the_fir_username_style().\
            get_the_fir_del_button()
        # 讀取數據庫
        db = shelve.open("username_style")
        username_style = db["username_style"]
        db.close()
        # 驗證無刪除按鈕
        pytest.assume( data["expect"] == result )
        # 驗證樣式變化
        pytest.assume( username_style == "text-decoration: line-through;" )


