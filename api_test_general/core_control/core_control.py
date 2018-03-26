import os
import time
import requests
import xlwt
import sys
import xlrd
import json
from xlutils.copy import copy

patch_control =os.path.dirname(os.path.realpath(__file__))
patch_control = patch_control[0:patch_control.rfind('/')]
sys.path.append(patch_control)

from core_control.config import *

# get
def get_request(url, payload, headers, cookies, type=0):
    r = requests.get(url, params=payload, headers=headers, cookies=cookies)
    if type == 0:
        return r
    elif type == 1:
        return r.text
    elif type == 2:
        return r.json()

# post
def post_request(url, payload, headers, cookies, type=0):
    r = requests.post(url, data=payload, headers=headers, cookies=cookies)

    if type == 0:
        return r
    elif type == 1:
        return r.text
    elif type == 2:
        return r.json()

def run_case(patch, case_list):

    for i in range(0,len(case_list)):
        os.system('python ' + patch + '/api_test_case/' + case_list[i])
        time.sleep(1)

def buid_excel_style(colour=1,bold=False):
    style = xlwt.XFStyle()

    #colour
    pattern = xlwt.Pattern()
    pattern.pattern=1
    pattern.pattern_fore_colour = 1
    style.pattern = pattern

    fnt = xlwt.Font()
    fnt.colour_index = 0
    if colour != 1:
        fnt.colour_index = 1

    fnt.bold = bold

    borders = xlwt.Borders()
    borders.left = 2
    borders.right = 2
    borders.top = 2
    borders.bottom = 2
    borders.bottom_colour=0x3A
    style.borders = borders

    return style


def create_log_name(patch):
    now = int(time.time())
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d_%H%M%S", timeArray)
    file = open(patch + 'tmp.txt', 'w')
    file.write(otherStyleTime)
    file.close()
    return otherStyleTime


def create_excel_head(patch):
    style = xlwt.XFStyle()
    style = buid_excel_style(0, True)
    wb = xlwt.Workbook()
    ws = wb.add_sheet('testReport')
    ws.write(0, 0, "case_name", style);
    ws.write(0, 1, 'request_mode', style);
    ws.write(0, 2, 'url', style);
    ws.write(0, 3, 'result', style);
    ws.write(0, 4, 'request_data', style);
    ws.write(0, 5, 'response_data', style);
    ws.write(0, 6, 'status_code', style);

    first_col = ws.col(0)  # xlwt中是行和列都是从0开始计算的
    first_col1 = ws.col(1)
    first_col2 = ws.col(2)
    first_col3 = ws.col(3)
    first_col4 = ws.col(4)
    first_col5 = ws.col(5)
    first_col6 = ws.col(6)

    first_col.width = 500 * 10
    first_col1.width = 250 * 20
    first_col2.width = 500 * 20
    first_col3.width = 150 * 20
    first_col4.width = 300 * 20
    first_col5.width = 300 * 20
    first_col6.width = 150 * 20

    wb.save(patch)

def create_log(patch_s):
    log_patch = patch_s + '/logs/'
    log_file_name = create_log_name(log_patch)
    create_excel_head(log_patch + log_file_name +'.xls')
    #print('create log')

def get_log_name(log_patch):
    #print(log_patch)
   # time.sleep(100)
    log_file = open(log_patch + 'tmp.txt','r')
    #print('log_file= ',log_file)
   # time.sleep(100)
    lines = log_file.readlines()
    log_file.close()
    return lines[0]

def add_log(log_patch, case_name, request_mode, url, result, request_data, response_data, status_code):
    log_patch = log_patch + '/logs/'
    log_name = get_log_name(log_patch)
    log_patch = log_patch + log_name + '.xls'
    styleBoldRed = xlwt.easyxf('pattern: pattern solid, fore_colour white;');
    if result == 'Fail':
        styleBoldRed = xlwt.easyxf('pattern: pattern solid, fore_colour red;font: color-index white');

    headerStyle = styleBoldRed;

    oldWb = xlrd.open_workbook(log_patch, formatting_info=True);
    table = oldWb.sheet_by_index(0)
    nrows = table.nrows

    newWb = copy(oldWb);
    newWs = newWb.get_sheet(0)
    newWs.write(nrows, 0, case_name, headerStyle);
    newWs.write(nrows, 1, request_mode, headerStyle);
    newWs.write(nrows, 2, url, headerStyle);
    newWs.write(nrows, 3, result, headerStyle);
    newWs.write(nrows, 4, request_data, headerStyle);
    newWs.write(nrows, 5, response_data, headerStyle);
    newWs.write(nrows, 6, status_code, headerStyle);
    newWb.save(log_patch);

def get_excel_dictionary(patch):
    log_patch = patch + '/logs/'
    log_name = get_log_name(log_patch)
    log_patch = log_patch + log_name + '.xls'

    workbook = xlrd.open_workbook(log_patch)
    table = workbook.sheet_by_index(0)
    columnName = table.row_values(0)
    nrows = table.nrows
    ncols = table.ncols
    excelDictionary = []
    for i in range(1, nrows):
        tableTmp = table.row_values(i)
        listTmp = {}
        for j in range(0, len(tableTmp)):
            listTmp[columnName[j]] = tableTmp[j]

        excelDictionary.append(listTmp)
    return excelDictionary

def notice_dingding(patch):
    excel_dictionary = get_excel_dictionary(patch)
    data = {}
    data['msgtype'] = "markdown"
    markdown = {}
    markdown['title'] = '接口自动化测试报警'
    markdown['text'] = "#### 某某自动化脚本\n\n"
    for i in range(0,len(excel_dictionary)):
        if(excel_dictionary[i]['result'] == 'Fail'):

            tmp = excel_dictionary[i]['url'] + "  error_code: " + str(excel_dictionary[i]['status_code']) + "\n\n"
            markdown['text'] = markdown['text'] + tmp

    data['markdown'] = markdown
    at = {}
    at['atMobiles'] = []
    at['isAtAll'] = False
    data['at'] = at
    payload1 = json.dumps(data, ensure_ascii=False).encode('utf-8')
    headerIe = {
        "Content-Type": "application/json"
    }
    r = post_request('https://oapi.dingtalk.com/robot/send?access_token=a81fcd62c0f3572983bf5b4c78560999ce2cc37554ff2df8e9feda0b4f474a9a',payload1,headerIe,'')
    return r






