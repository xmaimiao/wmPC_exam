import datetime
import os
import random
import shelve
import sys
from common.contants import basepage_dir, test_bug29693_29682_dir
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
        # 获取basepage.yaml中设置的环境变量
        wm_env =  datas["default"]
        # 根据环境变量取对应的账号和密码
        user_env = datas["user"][wm_env]
        # 根据环境变量取对应的睡眠时间
        sleep_env = datas["sleeps"][wm_env]
        return user_env,sleep_env

def get_data(option):
    '''
    获取yaml测试数据
    '''
    with open(test_bug29693_29682_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas



class Test_Bug29693_29682:

    _now_time = datetime.datetime.now()
    _num = str(random.randint(0, 100))
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
                username(self._setup_datas[0]["username"]).password(self._setup_datas[0]["password"]).save(). \
                goto_application(). \
                goto_exam(self._setup_datas[0]["application"])

        def teardown_class(self):
            '''
            非調試端口啓用
            '''
            self.main.close()

    # 验证上传已排计划，有错误提示
    def check_upload_error(self, plan_name,term,type,excel_path):
        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(self._now_time.strftime('%m%d')+plan_name+self._num).term(term). \
            exam_type(type). \
            upload_exists_plan_import(excel_path).\
            download_result().\
            check_upload_result()
        assert result == True

    # 验证上传已排计划，有警告提示
    def check_upload_warn(self, plan_name,term,type,excel_path):
        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(self._now_time.strftime('%m%d')+plan_name+self._num).term(term). \
            exam_type(type). \
            upload_exists_plan_import(excel_path).\
            download_result().\
            check_upload_warn()
        assert result == True

    # 验证添加計劃成功
    def check_add_plan_succeed(self, plan_name,term,type,excel_path):
        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(self._now_time.strftime('%m%d')+ plan_name+ self._num).term(term). \
            exam_type(type). \
            upload_exists_plan_import(excel_path). \
            download_result().\
            goto_plan_details().\
            get_plan_name()
        assert "當前計劃" in result

    # 驗證刪除考試計劃
    def del_exam_plan(self):
        result = self.main.goto_exam_plan(). \
            goto_the_first_plan_details(). \
            del_plan().get_ele_of_addplan()
        assert result == "添加已排計劃"


    # 添加考試科目,无考室，验证保存成功
    def add_exam_succeed(self, plan_name, examCode, course_1, teacher_1, classdata_1, examdate, examtime):
        result = self.main.goto_exam_plan(). \
            goto_plan_details(plan_name). \
            goto_add_exam(). \
            add_examCode(examCode).add_course_1(course_1). \
            add_teacher_1(teacher_1).add_class_1(classdata_1). \
            add_examtime(examtime).add_examdate(examdate). \
            click_save().check_add_succeed()
        return result == "保存成功"

    # 添加考試科目,无考室，验证保存失败
    def add_exam_failed(self, plan_name, examCode, course_1, teacher_1, classdata_1, examdate, examtime):
        result = self.main.goto_exam_plan(). \
            goto_plan_details(plan_name). \
            goto_add_exam(). \
            add_examCode(examCode).add_course_1(course_1). \
            add_teacher_1(teacher_1).add_class_1(classdata_1). \
            add_examtime(examtime).add_examdate(examdate). \
            click_save().check_add_failed()
        return result == "保存失敗"


        # 测试用例
        # bug29693

    @pytest.mark.parametrize("data", get_data("test_check_add_plan_succeed_29693"))
    def test_check_add_plan_succeed_29693(self, data):
        '''
        验证添加計劃成功
        '''
        self.check_add_plan_succeed(data["plan_name"], data["term"], data["type"], data["excel_path"])
        # self.del_exam_plan()

    @pytest.mark.parametrize("data", get_data("test_add_exam_succeed"))
    def test_add_exam_succeed(self, data):
        '''
        验证添加科目成功，存在学生设置
        '''
        self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])
        plan = self._now_time.strftime('%m%d') + data["plan"]
        self.add_exam_succeed(plan,data["examCode"],data["course_1"],data["teacher_1"],data["classdata_1"],
                      data["examdate"],data["examtime"])
        self.del_exam_plan()

    @pytest.mark.parametrize("data", get_data("test_add_exam_failed"))
    def test_add_exam_failed(self, data):
        '''
        验证添加科目失败，存在学生设置
        '''
        self.check_add_plan_succeed(data["plan_name"], data["term"], data["type"], data["excel_path"])
        # plan = self._now_time.strftime('%m%d') + data["plan"]
        # self.add_exam_failed(plan, data["examCode"], data["course_1"], data["teacher_1"], data["classdata_1"],
        #                       data["examdate"], data["examtime"])
        # self.del_exam_plan()