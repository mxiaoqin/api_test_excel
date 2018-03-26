import unittest
import sys
import os
import time
import json

patch =os.path.dirname(os.path.realpath(__file__))
patch = patch[0:patch.rfind('\\')]
sys.path.append(patch)

from core_control.core_control import *
from core_control.config import *

class Test_xc_pc_index(unittest.TestCase):

    def setUp(self):
        self.headers = {'Accept': 'application/vnd.lumen.pc+json'}
        self.cookies = ''
        self.url = URL_XC + 'getcarousel'


    def test_xc_pc_index(self):
        data = {}
        r = get_request(self.url, data, self.headers, self.cookies)
        print(r.json())

    def tearDown(self):
        add_log(patch, '获取PC首页轮播27', 'get', URL_XC + 'getcarousel', 'Pass', "{'aaaaaaaa':'c'}", "{'message':'成功'}", 200)

if __name__ =='__main__':
  unittest.main()
