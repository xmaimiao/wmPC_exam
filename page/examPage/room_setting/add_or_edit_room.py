from common.contants import add_or_edit_room_dir
from page.basepage import BasePage


class Add_Or_Edit_Room(BasePage):
    def edit_roomCode(self,room):
        self._params["room"] = room
        self.step(add_or_edit_room_dir,"edit_roomCode")
        return self

    def edit_seatCount(self,seatCount):
        '''
        編輯座位數
        '''
        self._params["seatCount"] = seatCount
        self.step(add_or_edit_room_dir,"edit_seatCount")
        return self

    def edit_startSn_and_endSn(self,startSn):
        '''
        編輯開始編號-結束編號
        '''
        self._params["startSn"] = startSn
        self.step(add_or_edit_room_dir,"edit_startSn_and_endSn")
        return self

    def edit_faculty(self,faculty):
        '''
        編輯可使用學院
        '''
        if self.step(add_or_edit_room_dir,"faculty_is_exist")>0:
            pass
        else:
            self._params["faculty"] = faculty
            self.step(add_or_edit_room_dir,"edit_faculty")
        return self

    def click_save(self):
        result =  self.step(add_or_edit_room_dir,"click_save")
        # 關閉抽屜
        self.step(add_or_edit_room_dir, "close_page")
        return result