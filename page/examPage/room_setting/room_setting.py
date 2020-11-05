from common.contants import room_setting_dir
from page.basepage import BasePage
from page.examPage.room_setting.add_or_edit_room import Add_Or_Edit_Room


class Room_Setting(BasePage):
    def add_room(self):
        '''
        添加考室
        '''
        self.step(room_setting_dir,"add_room")
        return Add_Or_Edit_Room(self._driver)

    def search_roomCode(self,room_keys):
        '''
        查詢考室編號，並點擊”查詢“按鈕
        '''
        self._params["room_keys"] = room_keys
        self.step(room_setting_dir,"search_roomCode")
        return self

    def edit_the_first_room(self):
        '''
        編輯第一條數據，點擊”編輯“按鈕
        '''
        self.step(room_setting_dir,"edit_the_first_room")
        return Add_Or_Edit_Room(self._driver)

    def delect_the_first_room(self):
        '''
        刪除第一條數據
        '''
        self.step(room_setting_dir, "delect_the_first_room")
        return self

    def get_current_datacount(self):
        '''
        獲取當前頁面數據量
        '''
        return self.step(room_setting_dir, "get_current_datacount")

