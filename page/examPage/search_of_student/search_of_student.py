import shelve

from common.contants import search_of_student_dir
from page.basepage import BasePage


class Search_Of_Student(BasePage):

    def wait_sleep(self,sleeps):
        self.sleep(sleeps)
        return self

    def simple_search_student(self,user_s):
        '''
        1.簡易查詢學生賬號/姓名
        2.點擊“查詢”icon
        '''
        self._params["user_s"] = user_s
        self.step(search_of_student_dir,"simple_search_student")
        return self

    def get_the_fir_username_style(self):
        '''
        驗證“刪除/設置為T”的學生樣式用，若已移除/T則屬性 style="text-decoration: line-through;"
        '''
        try:
            # 打開數據庫,保存獲取的賬號屬性
            # db = shelve.open("username_style")
            username_style =  (self.step(search_of_student_dir,"get_the_fir_username_style")).get_attribute("style")
            print(f"username_style:{username_style}")
            # db["username_style"] = username_style
            # db.close()
            if username_style =="username_style:text-decoration: unset;":
                return False
            elif username_style =="username_style:text-decoration: line-through;":
                return True
        except Exception as e:
            print("查詢結果：暫無數據")
            raise e

    def del_the_fir_student(self):
        '''
        移除第一行的學生
        '''
        try:
            self.step(search_of_student_dir,"del_the_fir_student")
            return self
        except Exception as e:
            print("沒有移除按鈕，無法操作！")
            raise e
    def get_the_fir_del_button(self):
        '''
        判斷第一行數據是否存在”移除“按鈕，存在返回true，否則false
        '''
        return self.step(search_of_student_dir,"get_the_fir_del_button")