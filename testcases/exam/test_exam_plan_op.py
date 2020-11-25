import datetime
import os
import shelve
import sys
from common.contants import test_exam_plan_dir, basepage_dir
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


class Test_Exam_Plan:
    with open(test_exam_plan_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)
        test_check_upload_exists_plan_datas = datas["test_check_upload_exists_plan"]
        test_check_add_plan_succeed_datas = datas["test_check_add_plan_succeed"]
        test_current_exam_total_datas = datas["test_current_exam_total"]
        test_add_exam_same_examCode_pre1_datas = datas["test_add_exam_same_examCode_pre1"]
        test_add_exam_same_examCode_pre2_datas = datas["test_add_exam_same_examCode_pre2"]
        test_add_exam_same_examCode_end1_datas = datas["test_add_exam_same_examCode_end1"]
        test_add_exam_same_examCode_end2_datas = datas["test_add_exam_same_examCode_end2"]
        test_add_exam_same_examCode_roomCode_datas = datas["test_add_exam_same_examCode_roomCode"]
        test_add_exam_same_examCode_invigilate_datas = datas["test_add_exam_same_examCode_invigilate"]
        test_add_exam_same_examCode_update_examdate1_datas = datas["test_add_exam_same_examCode_update_examdate1"]
        test_add_exam_same_examCode_update_examdate2_datas = datas["test_add_exam_same_examCode_update_examdate2"]
        test_add_exam_datas = datas["test_add_exam"]
        test_add_double_exam_datas = datas["test_add_double_exam"]
        test_del_exam_plan_datas = datas["test_del_exam_plan"]
        test_del_exam_datas = datas["test_del_exam"]
        test_add_exam_type_datas = datas["test_add_exam_type"]
        test_add_double_exam_type_datas = datas["test_add_double_exam_type"]
        test_release_undergraduate_plan_for_date_datas = datas["test_release_undergraduate_plan_for_date"]
        test_release_undergraduate_plan_all_datas = datas["test_release_undergraduate_plan_all"]
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
        验证上传已排计划
        '''

        result = self.main.goto_exam_plan().\
            add_exists_plan().\
            plan_name(self._now_time.strftime('%m%d')+data["plan_name"]).term(data["term"]).\
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
            plan_name(self._now_time.strftime('%m%d')+data["plan_name"]).term(data["term"]).\
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
            plan_name(data["plan_name"]).term(data["term"]). \
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
        result = self.main.goto_exam_plan().\
            goto_plan_details(data["plan_name"]).\
            goto_add_exam().\
            add_examCode(data["examCode"]).add_course_1(data["course_1"]).\
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]).\
            add_examdate(examdate).add_examtime(data["examtime"]).\
            add_roomCode(data["roomCode"]).add_invigilate_one(data["invigilate_one"]).\
            add_grade(data["grade"]).click_save().check_add_succeed()
        assert data["expect"] == result


    @pytest.mark.parametrize("data", test_add_exam_same_examCode_pre2_datas)
    def test_add_exam_same_examCode_pre2(self, data):
        # 在驗證創建同排考編號的科目B其日期和時間同步設置
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]).\
            goto_add_exam().\
            add_examCode(data["examCode"]).add_course_1(data["course_1"]).\
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]).\
            click_save_same_examCode().check_add_succeed()
        assert data["expect"] == result

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
        # examdate = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        # 先驗證前提條件，創建科目A成功
        result1 = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]). \
            add_examdate(now_time).add_examtime(data["examtime"]). \
            add_grade(data["grade"]).click_save().check_add_succeed()
        assert data["expect"] == result1

    @pytest.mark.parametrize("data", test_add_exam_same_examCode_end2_datas)
    def test_add_exam_same_examCode_end2(self, data):
        '''
        验证提示：
        该排考编号的科目考试已结束，如需继续请更换排考编号
        '''
        # 在驗證創建同排考編號的科目B其日期和時間同步設置
        result2 = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]). \
            get_same_examCode_end_toast()
        assert data["expect"] in result2

    @pytest.mark.parametrize("data", test_add_exam_same_examCode_roomCode_datas)
    def test_add_exam_same_examCode_roomCode(self,data):
        '''
        驗證同排考編號科目，考場不可相同
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]). \
            add_roomCode_same_examCode(data["roomCode"]).\
            click_save_same_examCode().check_add_failed()
        assert data["expect"] in result

    @pytest.mark.parametrize("data", test_add_exam_same_examCode_invigilate_datas)
    def test_add_exam_same_examCode_invigilate(self,data):
        '''
        驗證同排考編號科目，考場不同，監考員不可相同
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]). \
            add_roomCode_same_examCode(data["roomCode"]).add_invigilate_one_same_examCode(data["invigilate_one"]).\
            click_save_same_examCode().check_add_failed()
        assert data["expect"] in result

    @pytest.mark.parametrize("data", test_add_exam_same_examCode_update_examdate1_datas)
    def test_add_exam_same_examCode_update_examdate1(self,data):
        '''
        验证同排考編號考試時間更改后自動同步
        前提：創建科目A
        '''
        result= self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]). \
            add_examdate(data["examdate"]).add_examtime(data["examtime"]). \
            add_roomCode(data["roomCode"]).add_invigilate_one(data["invigilate_one"]). \
            add_grade(data["grade"]).click_save().check_add_succeed()
        assert data["expect"] == result

    @pytest.mark.parametrize("data", test_add_exam_same_examCode_update_examdate2_datas)
    def test_add_exam_same_examCode_update_examdate2(self, data):
        '''
        验证同排考編號科目B，考試時間更改后自動同步科目A
        '''
        # 獲取當前的時間
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]). \
            add_examdate_same_examCode(data["examdate"]). \
            click_save_same_examCode().\
            close_and_goto_plan_details().\
            get_same_examdate_courses(data["examdate"])
        assert data["expect"] == result

    @pytest.mark.parametrize("data", test_add_exam_datas)
    def test_add_exam(self, data):
        '''
        验证添加考試科目
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]).add_student_exam(data["num"]).\
            add_examdate(data["examdate"]).add_examtime(data["examtime"]). \
            add_roomCode(data["roomCode"]).add_invigilate_one(data["invigilate_one"]).\
            click_save().check_add_succeed()
        assert data["expect"] == result

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
            click_save().check_add_succeed()
        assert data["expect"] == result

    @pytest.mark.parametrize("data", test_add_double_exam_datas)
    def test_studenttable_courseCode(self,data):
        '''
        改寫未完，不可用
        1.驗證學生清單裏科課程已改爲：科目
        2.驗證學生清單裏科目字段顯示為科目編號
        '''
        exam_title = self.main.goto_exam_plan(). \
            goto_the_first_plan_details().\
            goto_the_first_exam_studenttable().\
            get_exam_title()
        assert data["expect"] == exam_title

    @pytest.mark.parametrize("data", test_del_exam_plan_datas)
    def test_del_exam_plan(self,data):
        '''
        驗證刪除考試計劃
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            del_plan().get_ele_of_addplan()
        assert result == data["expect"]

    @pytest.mark.parametrize("data", test_del_exam_datas)
    def test_del_exam(self,data):
        '''
        驗證刪除考試
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            del_exam(data["num"]).get_current_exam_total()
        db = shelve.open("exam_total")
        before_exam_total = db["exam_total"]
        db.close()
        assert result == int(before_exam_total) - 1

    @pytest.mark.parametrize("data", test_add_exam_type_datas)
    def test_add_exam_type(self, data):
        '''
        驗證添加單門科目，考試形式為：閉卷，工具全部
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]).\
            add_exam_ruletype_close_book_1().add_exam_ruletype_book_1().\
            add_exam_ruletype_calcu_1().add_exam_ruletype_dict_1().add_exam_ruletype_computer_1().\
            add_examdate(data["examdate"]).add_examtime(data["examtime"]). \
            click_save().check_add_succeed()
        assert data["expect"] == result

    @pytest.mark.parametrize("data", test_add_double_exam_type_datas)
    def test_add_double_exam_type(self, data):
        '''
        驗證添加雙門科目，科目一、二考試形式為：閉卷，工具全部
        '''
        result = self.main.goto_exam_plan(). \
            goto_plan_details(data["plan_name"]). \
            goto_add_exam(). \
            add_examCode(data["examCode"]).add_course_1(data["course_1"]). \
            add_teacher_1(data["teacher_1"]).add_class_1(data["classdata_1"]). \
            add_exam_ruletype_close_book_1().add_exam_ruletype_book_1(). \
            add_exam_ruletype_calcu_1().add_exam_ruletype_dict_1().add_exam_ruletype_computer_1(). \
            add_course_2(data["course_2"]).add_teacher_2(data["teacher_2"]).add_class_2(data["classdata_2"]). \
            add_exam_ruletype_close_book_2().add_exam_ruletype_book_2(). \
            add_exam_ruletype_calcu_2().add_exam_ruletype_dict_2().add_exam_ruletype_computer_2(). \
            add_examdate(data["examdate"]).add_examtime(data["examtime"]). \
            add_roomCode(data["roomCode"]).add_invigilate_one(data["invigilate_one"]). \
            click_save().check_add_succeed()
        assert data["expect"] == result

    @pytest.mark.parametrize("data", test_release_undergraduate_plan_for_date_datas)
    def test_release_undergraduate_plan_for_date(self, data):
        '''
        驗證根據考試日期發佈本科計劃
        '''
        result = self.main.goto_exam_plan(). \
            simple_search_plan(data["plan_name"]).\
            goto_release_undergraduate_plan_of_the_fir(data["plan_name"]).\
            wait_sleep(1).release_for_date(data["date_list"]).\
            teacher_view_date(data["date_t"]).student_view_date(data["date_t"]).\
            click_release().get_ele_of_addplan()
        assert data["expect"] == result

    @pytest.mark.parametrize("data", test_release_undergraduate_plan_all_datas)
    def test_release_undergraduate_plan_all(self, data):
        '''
        驗證發佈本科計劃-全部
        '''
        result = self.main.goto_exam_plan(). \
            simple_search_plan(data["plan_name"]).\
            goto_release_undergraduate_plan_of_the_fir(data["plan_name"]).\
            wait_sleep(1).release_all().\
            teacher_view_date(data["date_t"]).student_view_date(data["date_t"]).\
            click_release().get_ele_of_addplan()
        assert data["expect"] == result

