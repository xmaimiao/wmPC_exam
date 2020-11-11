from selenium.common.exceptions import NoSuchElementException

from common.contants import exam_plan_dir
from page.basepage import BasePage
from page.examPage.exam_planPage.add_exists_plan import Add_Exists_Plan
from page.examPage.exam_planPage.plan_details import Plan_Details


class Exam_Plan(BasePage):

    def get_ele_of_addplan(self):
        '''
        获取“添加计划”元素，验证回到了计划列表页面
        '''
        try:
            return self.step(exam_plan_dir,"get_ele_of_addplan")
        except Exception as e:
            print("删除过程有误，请检查！")

    def add_exists_plan(self):
        '''
        添加已排计划
        '''
        self.step(exam_plan_dir,"add_exists_plan")
        return Add_Exists_Plan(self._driver)

    def goto_plan_details(self, plan_name):
        '''
        通过参数：计划名称，打开该计划详情
        '''
        self._params["plan_name"] = plan_name
        try:
            self.step(exam_plan_dir, "goto_plan_details")
            return Plan_Details(self._driver)
        except NoSuchElementException as e:
            print("排考計劃列表沒有該計劃")
            raise e

    def goto_the_first_plan_details(self):
        '''
        打開第一行的計劃，進入計劃詳情
        '''
        self.step(exam_plan_dir, "goto_the_first_plan_details")
        return Plan_Details(self._driver)

    def goto_release_undergraduate_plan(self):
        '''
        根據計劃名稱進行發佈操作
        發佈本科計劃，此處默認“全選”發佈
        '''
        self.step(exam_plan_dir,"goto_release_undergraduate_plan")
        return Release_Undergraduate_Plan(self._driver)