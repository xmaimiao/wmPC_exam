import datetime
import os
import random
import shelve
import sys
from common.contants import basepage_dir, test_story771_661_667_dir
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
    with open(test_story771_661_667_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas



class Test_Story771_661_667:

    _now_time = datetime.datetime.now()
    _num = str(random.randint(0,100))
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
    # 验证上传已排计划
    def check_upload_exists_plan(self, plan_name,term,type,excel_path):
        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(self._now_time.strftime('%m%d')+plan_name+self._num).term(term). \
            exam_type(type). \
            upload_exists_plan_import(excel_path).\
            download_result().\
            check_upload_result()
        assert result

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

    @pytest.mark.parametrize("data", get_data("test_check_upload_exists_plan"))
    def test_check_upload_exists_plan(self, data):
        '''
        验证上传已排计划
        '''

        result = self.check_upload_exists_plan(data["plan_name"],data["term"],data["type"],data["excel_path"])
        assert result == data["expect"]

    @pytest.mark.parametrize("data", get_data("test_story667"))
    def test_story667(self, data):
        self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])

    @pytest.mark.parametrize("data", get_data("test_check_add_plan_succeed"))
    def test_check_add_plan_succeed(self, data):
        '''
        验证添加計劃成功
        '''

        self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])


    # bug29292-1同科目，不同的班别允许排考编号不同
    @pytest.mark.parametrize("data", get_data("test_bug29292_1"))
    def test_bug29292_1(self, data):
        '''
        验证上传已排计划
        '''
        self.check_add_plan_succeed(data["plan_name"], data["term"], data["type"], data["excel_path"])
        self.del_exam_plan()


    # bug29292-2同科目，存在相同的班别排考编号不同（考试时间不同）导入报错
    @pytest.mark.parametrize("data", get_data("test_bug29292_2"))
    def test_bug29292_2(self, data):
        '''
        验证上传已排计划
        '''
        result = self.check_upload_exists_plan(data["plan_name"], data["term"], data["type"], data["excel_path"])
        assert result == data["expect"]

    # bug29292-3同科目，存在相同的班别排考编号相同（考试时间同）导入成功，且保存成功
    @pytest.mark.parametrize("data", get_data("test_bug29292_3"))
    def test_bug29292_3(self, data):
        '''
        验证上传已排计划
        '''
        self.check_add_plan_succeed(data["plan_name"], data["term"], data["type"], data["excel_path"])
        self.del_exam_plan()