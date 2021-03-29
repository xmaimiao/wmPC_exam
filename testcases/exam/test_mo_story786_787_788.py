import datetime
import os
import random
import sys
from common.contants import basepage_dir,test_mo_story786_787_788_dir
from page.basepage import _get_working

curPath = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_dir)
sys.path.append('')
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
    with open(test_mo_story786_787_788_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas



class Test_Mo_Story786_787_788:

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


    # 验证刪除考室
    def delete_examroom(self, room_keys):
        result = self.main.goto_room_setting(). \
            search_roomCode(room_keys).\
            delect_the_first_room().get_current_datacount()
        return result

    # 验证添加考室
    def add_examroom(self, room,seatCount,faculty):
        result = self.main.goto_room_setting().\
            add_room().edit_roomCode(room).\
            edit_seatCount(seatCount).\
            edit_faculty(faculty).\
            click_save()
        assert result == "保存成功"

    # 發佈本科計劃-全部
    def release_undergraduate_plan_all(self):
        result = self.main.goto_exam_plan(). \
            goto_release_undergraduate_plan_of_the_fir().\
            wait_sleep(1).release_all().\
            click_release().get_ele_of_addplan()
        assert "添加已排計劃" == result

    # 测试前置-添加房间
    @pytest.mark.parametrize("data", get_data("test_add_examroom"))
    def test_add_examroom(self, data):
        '''
        验证添加考室
        '''
        self.add_examroom(data["room"],data["seatCount"],data["faculty"])



    # 测试用例
    # story788
    @pytest.mark.parametrize("data", get_data("test_check_upload_error_788"))
    def test_check_upload_error_788(self, data):
        '''
        验证上传已排计划，有错误提示
        '''

        self.check_upload_error(data["plan_name"],data["term"],data["type"],data["excel_path"])

    @pytest.mark.parametrize("data", get_data("test_check_upload_warn_788"))
    def test_check_upload_warn_788(self, data):
        '''
        验证上传已排计划，有警告提示
        '''
        self.check_upload_warn(data["plan_name"],data["term"],data["type"],data["excel_path"])

    @pytest.mark.parametrize("data", get_data("test_check_add_plan_succeed"))
    def test_check_add_plan_succeed(self, data):
        '''
        验证添加計劃成功
        '''
        self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])
        self.release_undergraduate_plan_all()
        # self.del_exam_plan()


    # 测试后置-删除房间
    @pytest.mark.parametrize("data", get_data("test_delete_examroom"))
    def test_delete_examroom(self, data):
        '''
        验证刪除考室
        '''
        result = self.delete_examroom(data["room_keys"])
        assert result == data["expect"]



