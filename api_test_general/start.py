import os
patch =os.path.dirname(os.path.realpath(__file__))
print(patch)
from core_control.core_control import *

case_list = [
    'test_test.py',
    'test_test_add.py',
    'test_xc_pc_index.py',
        ]

if __name__ =='__main__':
    print('start')
    print(patch)
    create_log(patch)
    run_case(patch,case_list)
   # notice_dingding(patch)
    print('end')
