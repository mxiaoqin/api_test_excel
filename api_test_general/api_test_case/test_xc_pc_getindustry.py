import unittest
import sys
import os

patch = os.path.dirname(os.path.realpath(__file__))
patch = patch[0:patch.rfind('\\')]
sys.path.append(patch)

from core_control.core_control import *
from core_control.config import *

class Test_xc_pc_getindustry(unittest.TestCase):

    def setUp(self):
        self.headers = {'accept':'application/vnd.lumen.pc+json'}
        self.cookies = ''
        self.url = URL_XC + 'getindustry'
    def test_xc_pc_getindustry(self):
        data={}

        r = get_request(self.url,data,self.headers,self.cookies)
        print(r.json())
    def tearDown(self):

         add_log(patch,'获取PC左边导航所有','get',self.url,'pass',"{'sasa':'dd'}","{'message':'成功'}",200)

if __name__ ==' main ':
    unittest.main()