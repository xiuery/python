# -*- coding: utf-8 -*-
__author__ = 'XIUERY'

'''
将有键值关系的字符串转为可直接复制使用的字典
'''

import json


def line_by_line(string):
    """
    一行键一行值的拆分
    """
    lines = string.split('\n')
    lines = [i.strip() for i in lines if i.strip()]
    # 奇偶拆分
    r = dict(zip(lines[::2], lines[1::2]))

    return json.dumps(r, indent=4)


def line_kv(string):
    """
    key:value 类型的拆分
    """
    lines = string.split('\n')
    lines = [i.strip() for i in lines if i.strip()]

    r = dict()
    for line in lines:
        r[line.split(':', 1)[0].strip()] = line.split(':', 1)[1].strip()

    return json.dumps(r, indent=4)


if __name__ == '__main__':
    string1 = '''
    Accept	
    text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Encoding	
    gzip, deflate
    Accept-Language	
    zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
    Cache-Control	
    max-age=0
    Connection	
    keep-alive
    Cookie	
    BAIDUID=BE0013EA57F731754102807D887E6A38:FG=1; BIDUPSID=BE0013EA57F731754102807D887E6A38; PSTM=1528263159; BD_UPN=13314352; BD_HOME=0; H_PS_PSSID=26599_1456_21080_26577_22074
    Host	
    www.baidu.com
    Upgrade-Insecure-Requests	
    1
    User-Agent	
    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
    '''
    string2 = '''
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9
    Cache-Control: no-cache
    Connection: keep-alive
    Cookie: BAIDUID=C75328B4A58406E0A8B42C7B55C9A564:FG=1; PSTM=1528680973; BIDUPSID=B29D39A47C12438F9908F6B0172E0157; BD_UPN=12314353; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_CK_SAM=1; BD_HOME=0; PSINO=7; H_PS_PSSID=26524_1459_21100_26350_26433_26578_20927; H_PS_645EC=fa2dApgFiRhZKdHugqwgC6LKpDIXyfEFvzkP4zoFfvOrP7Lu8Tm8GiTz0NA
    Host: www.baidu.com
    Pragma: no-cache
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36
    '''
    print(line_by_line(string1))
    print(line_kv(string2))



