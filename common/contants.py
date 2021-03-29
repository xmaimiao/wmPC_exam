import os
base_dir = os.path.dirname(os.path.dirname(__file__))

loginpage_dir = os.path.join(base_dir,'data/loginpage.yaml')

index_dir = os.path.join(base_dir,'data/index.yaml')

application_dir = os.path.join(base_dir,'data/application.yaml')

main1_dir = os.path.join(base_dir,'data/main1.yaml')

basepage_dir = os.path.join(base_dir,'data/basepage.yaml')

# 考试
exampage_dir = os.path.join(base_dir,'data/examPage/exampage.yaml')

exam_plan_dir = os.path.join(base_dir,'data/examPage/exam_planPage/exam_plan.yaml')

add_exists_plan_dir = os.path.join(base_dir,'data/examPage/exam_planPage/add_exists_plan.yaml')

exists_excel1_dir = os.path.join(base_dir,'excel/exists_excel1.yaml')

plan_details_dir = os.path.join(base_dir,'data/examPage/exam_planPage/plan_details.yaml')

add_exam_dir = os.path.join(base_dir,'data/examPage/exam_planPage/add_exam.yaml')

edit_exam_dir = os.path.join(base_dir,'data/examPage/exam_planPage/edit_exam.yaml')

release_undergraduate_plan_dir = os.path.join(base_dir,'data/examPage/exam_planPage/release_undergraduate_plan.yaml')

add_or_edit_room_dir = os.path.join(base_dir,'data/examPage/room_setting/add_or_edit_room.yaml')

room_setting_dir = os.path.join(base_dir,'data/examPage/room_setting/room_setting.yaml')

exam_studenttable_dir = os.path.join(base_dir,'data/examPage/room_setting/exam_studenttable.yaml')

search_of_student_dir = os.path.join(base_dir,'data/examPage/search_of_student/search_of_student.yaml')


# 考试case
test_exam_plan_dir = os.path.join(base_dir,'data/cases/exam/test_exam_plan.yaml')

test_authorization_dir = os.path.join(base_dir,'data/cases/exam/test_authorization/test_authorization.yaml')

test_edit_room_dir = os.path.join(base_dir,'data/cases/exam/test_edit_room.yaml')

test_bug27204_dir = os.path.join(base_dir,'data/cases/exam/test_bug27204.yaml')

test_bug27215_dir = os.path.join(base_dir,'data/cases/exam/test_bug27215.yaml')

test_student_of_T_dir = os.path.join(base_dir,'data/cases/exam/test_student_of_T.yaml')

test_mo_dir = os.path.join(base_dir,'data/cases/exam/test_mo.yaml')

test_student_of_makeup_exam_dir = os.path.join(base_dir,'data/cases/exam/test_student_of_makeup_exam.yaml')

test_bug_all_of_11_11_dir = os.path.join(base_dir,'data/cases/exam/test_bug_all_of_11_11.yaml')

test_story638_dir = os.path.join(base_dir,'data/cases/exam/test_story638.yaml')

test_mo_610_608_638_dir = os.path.join(base_dir,'data/cases/exam/test_mo_610_608_638.yaml')

test_story771_661_667_dir = os.path.join(base_dir,'data/cases/exam/test_story771_661_667.yaml')

test_mo_story771_661_667_dir = os.path.join(base_dir,'data/cases/exam/test_mo_story771_661_667.yaml')

test_story786_787_788_dir = os.path.join(base_dir,'data/cases/exam/test_story786_787_788.yaml')

test_mo_story786_787_788_dir = os.path.join(base_dir,'data/cases/exam/test_mo_story786_787_788.yaml')

test_bug29693_29682_dir = os.path.join(base_dir,'data/cases/exam/test_bug29693_29682.yaml')



class TestPath:
    def test_path(self):
        print(loginpage_dir)