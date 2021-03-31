import datetime
import os
import random
import shelve
import sys
from common.contants import basepage_dir, test_story786_787_788_dir
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
    with open(test_story786_787_788_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas



class Test_Story786_787_788:

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

    #添加考試科目,无考室，验证保存失败
    def add_exam(self, plan_name,examCode,course_1,teacher_1,classdata_1,examdate,examtime):
        result = self.main.goto_exam_plan(). \
            goto_plan_details(plan_name). \
            goto_add_exam(). \
            add_examCode(examCode).add_course_1(course_1). \
            add_teacher_1(teacher_1).add_class_1(classdata_1).\
            add_examtime(examtime). add_examdate(examdate).\
            click_save().check_add_failed()
        return result == "保存失敗"

    # 添加考試科目,有考室，验证保存成功
    def add_exam_room(self, plan_name,examCode,course_1,teacher_1,classdata_1,examdate,examtime,roomCode):
        result = self.main.goto_exam_plan(). \
            goto_plan_details(plan_name). \
            goto_add_exam(). \
            add_examCode(examCode).add_roomCode(roomCode).add_course_1(course_1). \
            add_teacher_1(teacher_1).add_class_1(classdata_1).\
            add_examtime(examtime). add_examdate(examdate).\
            click_save().check_add_succeed()
        return result == "保存成功"

    def edit_exam(self, plan_name,roomCode,num):
        '''
        驗證编辑單門科目,编辑课室 ,保存失败
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(plan_name). \
            edit_exam_of_num(num). \
            wait_sleep(2).edit_roomCode(roomCode). \
            click_save().check_add_failed()
        assert "保存失敗" == result

    def add_exam_same_examCode_roomCode(self,plan_name,examCode,course_1,teacher_1,classdata_1,roomCode):
        '''
        驗證同排考編號科目，考場不可相同
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(plan_name). \
            goto_add_exam(). \
            add_examCode(examCode).add_course_1(course_1). \
            add_teacher_1(teacher_1).add_class_1(classdata_1). \
            add_roomCode_same_examCode(roomCode).\
            click_save_same_examCode().check_add_failed()
        assert result == "保存失敗"

    #学生已刪除/設置為T
    def stu_of_del_or_T(self, user_s):
        result = self.main.goto_search_of_student(). \
            simple_search_student(user_s). \
            get_the_fir_username_style()
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

    # 测试用例
    # story786
    @pytest.mark.parametrize("data", get_data("test_check_upload_warn_786"))
    def test_check_upload_warn_786(self, data):
        '''
        验证上传已排计划，有警告提示
        '''

        self.check_upload_warn(data["plan_name"],data["term"],data["type"],data["excel_path"])

    @pytest.mark.parametrize("data", get_data("test_check_add_plan_succeed_786_1"))
    def test_check_add_plan_succeed_786_1(self, data):
        '''
        验证添加計劃成功
        '''
        self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])
        self.del_exam_plan()

    @pytest.mark.parametrize("data", get_data("test_check_add_plan_succeed_786_2"))
    def test_check_add_plan_succeed_786_2(self, data):
        '''
        验证添加計劃成功
        '''
        self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])
        self.del_exam_plan()

    # story787
    # @pytest.mark.skip
    @pytest.mark.parametrize("data", get_data("test_T_787_1"))
    def test_T_787_1(self, data):
        '''发布前撤销设置为T的学生'''
        # self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])
        # ----------------------------设置为T，撤销为T，后发布
        self.release_undergraduate_plan_all()
        assert self.stu_of_del_or_T(data["user_s"]) == False

    # @pytest.mark.skip
    @pytest.mark.parametrize("data", get_data("test_T_787_2"))
    def test_T_787_2(self, data):
        '''发布后撤销设置为T的学生'''
        self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])
        # ----------------------------设置为T，发布
        # self.release_undergraduate_plan_all()
        # ---------------检查学生为T
        # assert self.stu_of_del_or_T(data["user_s"]) == True
        # self.del_exam_plan()

    # story788

    @pytest.mark.parametrize("data", get_data("test_check_upload_error_788"))
    def test_data(self, data):
        '''
        验证上传已排计划，有错误提示
        '''
        self.check_upload_error(data["plan_name"],data["term"],data["type"],data["excel_path"])

    @pytest.mark.parametrize("data", get_data("test_check_upload_error_788"))
    def test_check_upload_error_788(self, data):
        '''
        验证上传已排计划，有错误提示
        '''

        self.check_upload_error(data["plan_name"],data["term"],data["type"],data["excel_path"])

    #123456
    @pytest.mark.parametrize("data", get_data("test_check_upload_warn_788"))
    def test_check_upload_warn_788(self, data):
        '''
        验证上传已排计划，有警告提示
        '''
        self.check_upload_warn(data["plan_name"],data["term"],data["type"],data["excel_path"])

    @pytest.mark.parametrize("data", get_data("test_add_exam_788"))
    def test_add_exam_788(self, data):
        '''
        验证添加科目成功
        '''
        self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])
        plan = self._now_time.strftime('%m%d') + data["plan"]
        self.add_exam(plan,data["examCode"],data["course_1"],data["teacher_1"],data["classdata_1"],
                      data["examdate"],data["examtime"])
        self.del_exam_plan()

    @pytest.mark.parametrize("data", get_data("test_check_difnum_the_same_room"))
    def test_check_difnum_the_same_room(self, data):
        '''
        bug29607编辑科目，同一时间不同排考编号的科目考试，占用同一间教室
        '''
        self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])
        plan = self._now_time.strftime('%m%d') + data["plan"]
        self.add_exam_room(plan,data["examCode"],data["course_1"],data["teacher_1"],data["classdata_1"],
                      data["examdate"],data["examtime"],data["roomCode"])
        self.del_exam_plan()

    @pytest.mark.parametrize("data", get_data("test_add_exam_same_examCode_roomCode"))
    def test_add_exam_same_examCode_roomCode(self, data):
        '''
        bug29607编辑科目，同一时间同排考编号的科目考试，占用同一间教室
        '''
        self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])
        plan = self._now_time.strftime('%m%d') + data["plan"]
        self.add_exam_same_examCode_roomCode(plan,data["examCode"],data["course_1"],data["teacher_1"],data["classdata_1"],
                      data["roomCode"])
        self.del_exam_plan()

    @pytest.mark.parametrize("data", get_data("test_upload_and_edit_exam"))
    def test_upload_and_edit_exam(self, data):
        '''
        bug29607编辑科目，同一时间同排考编号的科目考试，占用同一间教室
        '''
        # self.check_add_plan_succeed(data["plan_name"],data["term"],data["type"],data["excel_path"])
        # plan = self._now_time.strftime('%m%d') + data["plan"]
        plan = "0325" + data["plan"]
        self.edit_exam(plan,data["roomCode"],data["num"])
        # self.del_exam_plan()

