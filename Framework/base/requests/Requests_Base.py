# -*- coding: utf-8 -*-
__author__ = 'Kerwin zhang'

import ast
import time
import json
import socket
import requests


class Requests_Base(object):
    # host_url = 'http://10.17.2.94:8089/rpa/web/amazon/getHost.do'

    def __init__(self, logger, casename):
        '''config the class params'''
        self.host_url = 'http://10.17.2.29:8089/rpa/web/common/getHost.do'
        self.casename = casename
        self.logger = logger
        self.host = self.get_host_ip()
        self.request_context = self.get_task_process_host()

    def get_host_ip(self):
        '''
        get the Robot machine's IP
        :return: Robot machine's IP
        '''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def get_host_name(self):
        '''
        :return: Robot machine's host name
        '''
        return socket.gethostname()

    def request_post(self, url, params):
        '''
        :param url: the url you want to request
        :param params: the params of your request
        :return: the response from the server which you requested with http post
        '''
        self.logger.info("url:%s; params:%s;", url, params)
        try:
            r = requests.post(url, params)
            if r.status_code == 200:
                http_result_map = json.loads(r.text)
                if http_result_map['status'] != 'success':
                    error_msg = 'HTTP ERROR: %s' % http_result_map['errorMessage']
                    self.logger.error(error_msg)
                    raise Exception(error_msg)
                else:
                    return http_result_map
            else:
                error_msg = 'HTTP Code: %s, msg: %s' % (r.status_code, r.reason)
                raise Exception(error_msg)
        except Exception as e:
            self.logger.error(e)

    def request_get(self, url, params):
        '''
        :param url: the url you want to request
        :param params: the params of your request
        :return: the response from the server which you requested with http get
        '''
        self.logger.info("url:{}; params:{};".format(url, params))
        try:
            r = requests.get(url, params)
            if int(r.status_code) == 200:
                ret = json.loads(r.text)
                if ret['status'] != 'success':
                    error_msg = 'HTTP ERROR: %s' % ret['errorMessage']
                    self.logger.error(error_msg)
                    raise Exception(error_msg)
                else:
                    return ret
            else:
                error_msg = 'HTTP Code: %s, msg: %s' % (r.status_code, r.reason)
                raise Exception(error_msg)
        except Exception as e:
            self.logger.error(e)

    def get_task_process_host(self):
        '''
        :return: get the server host address
        '''
        self.logger.info('Get web quote process host')
        url = self.host_url
        params = {'ip': self.host, 'caseName': self.casename}
        print(params)
        http_result_map = self.request_post(url, params)
        print(http_result_map)
        return http_result_map['data']['host']

    def get_task_process_config(self, postfix):
        '''
        :param postfix: the postfix of the url
        :param taskname: which task you want to process
        :return: the task config list
        '''
        self.logger.info('Get web quote process config')
        url = self.request_context + postfix
        params = {'ip': self.host, 'caseName': self.casename}
        http_result_map = self.request_post(url, params)
        return http_result_map['data']['caseConfig']

    def save_task_log_to_server(self, postfix, trans_begin, vendor_no, cpo_no, errormsg, *extend_values):
        '''
        :param postfix: the postfix of the url
        :param case_name: task name
        :param trans_begin: start name
        :param vendor_no: vendor number
        :param cpo_no: cpo number
        :param extend_values: more
        :return: nothing return
        '''
        self.logger.info('Save task log to server')
        url = self.request_context + postfix
        trans_end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ip = self.get_host_ip()
        params = {'ip': ip, 'caseName': self.casename, 'transBegin': trans_begin, 'transEnd': trans_end, 'errorMsg': errormsg,
                  'extendItem2': cpo_no}
        if len(extend_values) > 0:
            index = 3
            for extend_value in extend_values:
                value_name = 'extendItem' + str(index)
                params.setdefault(value_name, extend_value)
                index += 1
        if len(vendor_no) > 0:
            params.pop('extendItem1', vendor_no)
        params_json = ast.literal_eval(json.dumps(params))
        self.request_post(url, params_json)


if __name__ == '__main__':
    pass
