import time
import requests
from lxml import etree
from gevent.pool import Pool
from gevent.monkey import patch_socket
# from utils.Log import drop_ship_po_process_logger as logger
from Mapping import DBSession, RegistrationNew
patch_socket()
pool = Pool(20)


class Process(object):

    url = 'http://171.221.172.13:8888/lottery/accept/searchDetails?applyNo=%s'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }

    def __init__(self):
        pass

    def start(self):
        pool.map(self.process, [x for x in range(20180604000001, 20180606999999)])

        # number = 20180604000001
        # while number <= 20180606999999:
        #     response = self.get_registration(number)
        #     #
        #     # data = self.response_process(response)
        #     # print(data)
        #     # self.save(data)

    def stop(self):
        pass

    def process(self, number):
        response = self.get_registration(number)
        data = self.response_process(response)
        self.save(data)

    def get_registration(self, number):
        response = requests.get(self.url % number, headers=self.headers)

        # with open('html/' + str(number) + '.html', 'wb') as fp:
        #     fp.write(response.content)

        return response.text

    @staticmethod
    def response_process(response):
        data = dict()

        try:
            root = etree.HTML(response)
        except Exception:
            return None

        html = etree.ElementTree(root)

        data['pur_apply'] = html.xpath('//th[text()="购房登记申请结果："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="购房登记申请结果："]/following-sibling::td') else ''
        data['status'] = html.xpath('//th[not(text())]/following-sibling::td/b/text()')[0].strip() if html.xpath('//th[not(text())]/following-sibling::td/b') else ''
        data['type'] = html.xpath('//th[text()="购房登记类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="购房登记类型："]/following-sibling::td') else ''
        data['family_type'] = html.xpath('//th[text()="家庭类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="家庭类型："]/following-sibling::td') else ''
        data['divorce_time'] = html.xpath('//th[text()="离婚登记时间"]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="离婚登记时间"]/following-sibling::td') else ''
        data['number'] = html.xpath('//th[text()="购房登记号："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="购房登记号："]/following-sibling::td') else ''
        data['area'] = html.xpath('//th[text()="项目所在区域："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="项目所在区域："]/following-sibling::td') else ''
        data['license'] = html.xpath('//th[text()="预/现售证号："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="预/现售证号："]/following-sibling::td') else ''

        data['person_type'] = html.xpath('//th[text()="人员类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="人员类型："]/following-sibling::td') else ''
        data['certificate_type'] = html.xpath('//th[text()="证件类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="证件类型："]/following-sibling::td') else ''
        data['username'] = html.xpath('//th[text()="姓名："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="姓名："]/following-sibling::td') else ''
        data['id_card'] = html.xpath('//th[text()="证件号码："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="证件号码："]/following-sibling::td') else ''
        data['is_join'] = html.xpath('//th[text()="是否参与购房登记"]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="是否参与购房登记"]/following-sibling::td') else ''
        data['talent_type'] = html.xpath('//th[text()="人才类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="人才类型："]/following-sibling::td') else ''
        data['household_area'] = html.xpath('//th[text()="户籍所在区域："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="户籍所在区域："]/following-sibling::td') else ''
        data['social_type'] = html.xpath('//th[text()="社保类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="社保类型："]/following-sibling::td') else ''
        data['social_number'] = html.xpath('//th[text()="社保编码："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="社保编码："]/following-sibling::td') else ''
        data['company_name'] = html.xpath('//th[text()="缴存单位名称："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="缴存单位名称："]/following-sibling::td') else ''
        data['certificate_company_name'] = html.xpath('//th[text()="出具证明的单位名称："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="出具证明的单位名称："]/following-sibling::td') else ''
        data['create_time'] = time.time()

        return data

    @staticmethod
    def save(data):
        session = DBSession()
        registration = RegistrationNew(**data)
        session.add(registration)
        session.commit()


if __name__ == '__main__':
    process = Process()
    process.start()
