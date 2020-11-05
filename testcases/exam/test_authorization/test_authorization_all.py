import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_dir)
from common.contants import test_authorization_dir
from page.main import Main
import pytest
import yaml


class Test0924:
    with open(test_authorization_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)
        setup_datas = datas["setup_datas"]
        test_get_memu_num_datas = datas["test_get_memu_num"]

    def setup_class(self):
        '''
        非調試端口用
        '''
        # self.main = Main().goto_login(). \
        #     username(self.setup_datas["username"]).password(self.setup_datas["password"]).save(). \
        #     goto_application(). \
        #     goto_exam(self.setup_datas["application"])
        self.main = Main()

    def setup(self):
        '''
        非調試端口用
        '''
        self.begin=self.main.goto_login(). \
            username(self.setup_datas["username"]).password(self.setup_datas["password"]).save(). \
            goto_application(). \
            goto_exam(self.setup_datas["application"])

    def teardown(self):
        '''
        非調試端口用
        '''
        self.main.back_to_index().quit()

    def teardown_class(self):
        '''
        非調試端口啓用
        '''
        self.main.close()

    # def setup(self):
    #     '''
    #     開啓調試端口啓用
    #     '''
    #     self.main = Main()

    @pytest.mark.parametrize("data", test_get_memu_num_datas)
    def test_get_memu_num(self, data):
        '''
        權限測試，驗證取消排考計劃權限，菜單只有5個
        '''
        result = self.begin.get_memu_num()
        assert result == data["expect"]