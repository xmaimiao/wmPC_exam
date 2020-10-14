import os
base_dir = os.path.dirname(os.path.dirname(__file__))

loginpage_dir = os.path.join(base_dir,'data/loginpage.yaml')

index_dir = os.path.join(base_dir,'data/index.yaml')

application_dir = os.path.join(base_dir,'data/application.yaml')

main1_dir = os.path.join(base_dir,'data/main1.yaml')

# 课表
# classtimetable_dir = os.path.join(base_dir,'data/classtimetablepage/classtimetable.yaml')
#
# degree_course_classmate_t_dir = os.path.join(base_dir,'data/classtimetablepage/teacher_managementPage/degree_course_classmate_t.yaml')
#
# degree_course_classmate_s_dir = os.path.join(base_dir,'data/classtimetablepage/student_managementPage/degree_course_classmate_s.yaml')
#
# degree_course_classmate_r_dir = os.path.join(base_dir,'data/classtimetablepage/room_managementPage/degree_course_classmate_r.yaml')
#
# teacher_management_degree_dir = os.path.join(base_dir,'data/classtimetablepage/teacher_managementPage/teacher_management_degree.yaml')
#
# student_management_degree_dir = os.path.join(base_dir,'data/classtimetablepage/student_managementPage/student_management_degree.yaml')
#
# room_management_degree_dir = os.path.join(base_dir,'data/classtimetablepage/room_managementPage/room_management_degree.yaml')
#
# postgraduate_sign_in_record_dir = os.path.join(base_dir,'data/classtimetablepage/postgraduate_sign_in_recordPage/postgraduate_sign_in_record.yaml')

# 考试
exampage_dir = os.path.join(base_dir,'data/examPage/exampage.yaml')

exam_plan_dir = os.path.join(base_dir,'data/examPage/exam_planPage/exam_plan.yaml')

add_exists_plan_dir = os.path.join(base_dir,'data/examPage/exam_planPage/add_exists_plan.yaml')

exists_excel1_dir = os.path.join(base_dir,'excel/exists_excel1.yaml')

plan_details_dir = os.path.join(base_dir,'data/examPage/exam_planPage/plan_details.yaml')

add_exam_dir = os.path.join(base_dir,'data/examPage/exam_planPage/add_exam.yaml')

# 考试case
test_exam_plan_dir = os.path.join(base_dir,'data/cases/exam/test_exam_plan.yaml')

# 课表case
# test_teacher_m_degree_dir = os.path.join(base_dir,'data/cases/signin/test_teacher_m_degree.yaml')
#
# test_student_m_degree_dir = os.path.join(base_dir,'data/cases/signin/test_student_m_degree.yaml')
#
# test_room_m_degree_dir = os.path.join(base_dir,'data/cases/signin/test_room_m_degree.yaml')
#
# test_0924_dir = os.path.join(base_dir,'data/cases/signin/test_0924.yaml')


class TestPath:
    def test_path(self):
        print(loginpage_dir)