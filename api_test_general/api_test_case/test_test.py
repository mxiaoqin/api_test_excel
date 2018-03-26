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

class Test_test_test1(unittest.TestCase):

    def setUp(self):
        self.headers = {'Content-Type': 'application/json'}
        self.cookies = ''
        self.url = request_url + 'approvaltpl' + '?' + token


    def test_test_test1(self):
        data = {}

        data['name'] = "测试流程-财务"
        data['type'] = '823'
        data['amount_range'] = 1
        data['company'] = 22
        data['project'] = 373
        data['is_fundchange'] = 1
        data['order'] = 0

        payload = ""

        payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
        r = post_request(self.url, payload, self.headers, self.cookies)
        print(r.json())

    def tearDown(self):
        add_log(patch, 'test_test_test1', 'post', 'www.baidu.com', 'Fail', "{'a':'b'}", "{'message':'失败'}", 500)

if __name__ =='__main__':
  unittest.main()
