import datetime
import os
import sys
from common.contants import test_exam_plan_dir
curPath = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_dir)
sys.path.append('..')
from page.main import Main
import pytest
import yaml


class Test_Exam_Plan:
    with open(test_exam_plan_dir, encoding="utf-8") as f:

        datas = yaml.safe_load(f)
        setup_datas = datas["setup_datas"]
        test_check_upload_exists_plan_datas = datas["test_check_upload_exists_plan"]
        test_check_add_plan_succeed_datas = datas["test_check_add_plan_succeed"]
        test_current_exam_total_datas = datas["test_current_exam_total"]
        test_add_exam_same_examCode_pre1_datas = datas["test_add_exam_same_examCode_pre1"]
        test_add_exam_same_examCode_pre2_datas = datas["test_add_exam_same_examCode_pre2"]
        test_add_exam_same_examCode_end1_datas = datas["test_add_exam_same_examCode_end1"]
        test_add_exam_same_examCode_end2_datas = datas["test_add_exam_same_examCode_end2"]

    # def setup_class(self):
    #     '''
    #     非調試端口用
    #     '''
    #     self.main = Main().goto_login(). \
    #         username(self.setup_datas["username"]).password(self.setup_datas["password"]).save(). \
    #         goto_application(). \
    #         goto_exam(self.setup_datas["application"])
    #
    # def teardown_class(self):
    #     '''
    #     非調試端口啓用
    #     '''
    #     self.main.close()

    def setup(self):
        '''
        開啓調試端口啓用
        '''
        self.main = Main()

    @pytest.mark.parametrize("data", test_check_upload_exists_plan_datas)
    def test_check_upload_exists_plan(self, data):
        '''
        验证上传已排计划
        '''

        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(data["plan_name"]).term().\
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
            plan_name(data["plan_name"]).term().\
            upload_exists_plan_import(data["excel_path"]).\
            download_result().\
            goto_plan_details().\
            get_plan_name()
        assert data["expect"] in result

    @pytest.mark.parametrize("data", test_current_exam_total_datas)
    def test_current_exam_total(self,data):
        '''
        验证当前页考试科目行数
        '''
        result = self.main.goto_exam_plan(). \
            add_exists_plan(). \
            plan_name(data["plan_name"]).term(). \
            upload_exists_plan_import(data["excel_path"]).\
            goto_plan_details().\
            get_current_exam_total()
        assert result == data["expect"]

    @pytest.mark.parametrize("data", test_add_exam_same_examCode_pre1_datas)
    def test_add_exam_same_examCode_pre1(self,data):
        '''
        验证同排考編號考試時間自動同步，考試未開始
        '''
        # 獲取當前的時間
        now_time = datetime.datetime.now()
        # 格式化輸出當前日期+1天的時間
        examdate = (now_time + datetime.timedelta(days=+1)).strftime('%Y-%m-%d')
        # 先驗證前提條件，創建科目A成功
        result1 = self.main.goto_exam_plan().\
            goto_plan_details(data["plan_name"]).\
            goto_add_exam().\
            add_examCode(data["examCode"]).add_course_1(data["course"]).\
            add_teacher_1(data["teacher_1"]).add_class(data["classdata"]).\
            add_examdate(examdate).add_examtime(data["examtime"]).\
            add_grade(data["grade"]).click_save().check_add_succeed()
        assert data["expect"] == result1


    @pytest.mark.parametrize("data", test_add_exam_same_examCode_pre2_datas)
    def test_add_exam_same_examCode_pre2(self, data):
        # 在驗證創建同排考編號的科目B其日期和時間同步設置
        result2 = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]).\
            goto_add_exam().\
            add_examCode(data["examCode"]).add_course_1(data["course"]).\
            add_teacher_1(data["teacher_1"]).add_class(data["classdata"]).\
            click_save_same_examCode().check_add_succeed()
        assert data["expect"] == result2

    @pytest.mark.parametrize("data", test_add_exam_same_examCode_end1_datas)
    def test_add_exam_same_examCode_end1(self, data):
        '''
        验证添加同排考編號科目，考試已結束提示：
        该排考编号的科目考试已结束，如需继续请更换排考编号
        前提：增加已結束考試科目
        '''
        # 獲取當前的時間
        now_time = datetime.datetime.now()
        # 格式化輸出當前日期-1天的時間
        examdate = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        # 先驗證前提條件，創建科目A成功
        result1 = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course"]). \
            add_teacher_1(data["teacher_1"]).add_class(data["classdata"]). \
            add_examdate(examdate).add_examtime(data["examtime"]). \
            add_grade(data["grade"]).click_save().check_add_succeed()
        assert data["expect"] == result1

    @pytest.mark.parametrize("data", test_add_exam_same_examCode_end2_datas)
    def test_add_exam_same_examCode_end2(self, data):
        '''
        验证提示：
        该排考编号的科目考试已结束，如需继续请更换排考编号
        '''
        result1 = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).get_same_examCode_end_toast()

        assert data["expect"] in result1

        # 在驗證創建同排考編號的科目B其日期和時間同步設置
        result2 = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]). \
            get_same_examCode_end_toast()
        assert data["expect"] in result2

