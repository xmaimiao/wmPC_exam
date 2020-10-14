from selenium.common.exceptions import NoSuchElementException

from common.contants import exam_plan_dir
from page.basepage import BasePage
from page.examPage.exam_planPage.add_exists_plan import Add_Exists_Plan
from page.examPage.exam_planPage.plan_details import Plan_Details


class Exam_Plan(BasePage):
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
