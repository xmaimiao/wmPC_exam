import datetime
import shelve
from common.contants import basepage_dir, test_story638_dir
from page.basepage import  _get_working
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

class Test_Approval:

    with open(test_story638_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)
        test_check_upload_exists_plan_datas = datas["test_check_upload_exists_plan"]
        test_check_add_plan_succeed_datas = datas["test_check_add_plan_succeed"]
        test_del_exam_plan_datas = datas["test_del_exam_plan"]
        test_add_exam_same_examCode_datas = datas["test_add_exam_same_examCode"]
        test_add_exam_datas = datas["test_add_exam"]

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
        def setup(self):
            '''
            非調試端口用
            '''
            self.main = Main()
            # 讀取數據庫
            self.db = shelve.open("overtimeSn")

        def teardown(self):
            '''
            非調試端口啓用
            '''
            self.main.close()
            self.db.close()

    @pytest.mark.parametrize("data", test_check_upload_exists_plan_datas)
    def test_check_upload_exists_plan(self, data):
        '''
        验证上传已排计划
        '''
        result = self.main.goto_exam_plan(). \
            add_exists_plan(). \
            plan_name(self._now_time.strftime('%m%d')+data["plan_name"]).term(data["term"]). \
            exam_type(data["type"]). \
            upload_exists_plan_import(data["excel_path"]). \
            download_result(). \
            check_upload_result()
        assert result == data["expect"]

    @pytest.mark.parametrize("data", test_check_add_plan_succeed_datas)
    def test_check_add_plan_succeed(self, data):
        '''
        验证添加計劃成功
        '''

        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(self._now_time.strftime('%m%d')+data["plan_name"]).term(data["term"]).\
            exam_type(data["type"]).\
            upload_exists_plan_import(data["excel_path"]).\
            download_result().\
            goto_plan_details().\
            get_plan_name()
        assert data["expect"] in result

    @pytest.mark.parametrize("data", test_del_exam_plan_datas)
    def test_del_exam_plan(self,data):
        '''
        驗證刪除考試計劃
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            del_plan().get_ele_of_addplan()
        assert result == data["expect"]

    @pytest.mark.parametrize("data", test_add_exam_same_examCode_datas)
    def test_add_exam_same_examCode(self, data):
        # 在驗證創建同排考編號的科目B其日期和時間同步設置

        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]).\
            goto_add_exam().\
            add_examCode(self._now_time+data["examCode"]).add_course_1(data["course_1"]).\
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]).\
            click_save_same_examCode().check_add_succeed()
        assert data["expect"] == result

    @pytest.mark.parametrize("data", test_add_exam_datas)
    def test_add_exam(self, data):
        '''
        验证添加考試科目
        '''
        # add_student_exam(data["num"]).
        # 格式化輸出當前日期+1天的時間
        # examdate = (self._now_time + datetime.timedelta(days=+1)).strftime('%Y-%m-%d')
        examdate = (self._now_time + datetime.timedelta(days=+6)).strftime('%Y-%m-%d')
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]).\
            add_examdate(examdate).add_examtime(data["examtime"]). \
            add_roomCode(data["roomCode"]).add_invigilate_one(data["invigilate_one"]).\
            click_save().check_add_succeed()
        assert data["expect"] == result