import unittest
import sys
import os

patch = os.path.dirname(os.path.realpath(__file__))
patch = patch[0:patch.rfind('\\')]
sys.path.append(patch)

from core_control.core_control import *
from core_control.config import *

class Test_xc_pc_indexlist(unittest.TestCase):

     def setUp(self):
         self.headers = {'Accept':'application/vnd.lumen.pc+json'}
         self.cookies = ''
         self.url = URL_XC + 'getindexlist'
         self.ispass = 'Fail'

     def test_xc_pc_indexlist(self):
         data = {}
         r = get_request(self.url,data,self.headers,self.cookies)
         print(r.status_code)
         if r.status_code != 200:
             self.ispass = 'Pass'
             print(r.json())


     def tearDown(self):

        add_log(patch,'获取PC首页新闻','get',self.url, self.ispass,"{'aaaaaaaa':'c'}","{'message':'成功'}",200)

if __name__ ==' main ':
    unittest.main

