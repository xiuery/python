import time
import requests
from lxml import etree
from gevent.pool import Pool
from gevent.monkey import patch_socket
from func_timeout import func_set_timeout
from utils.Log import drop_ship_po_process_logger as logger
from Mapping import DBSession, Registration, FailProcess
patch_socket()
pool = Pool(100)


class Process(object):

    url = 'http://171.221.172.13:8888/lottery/accept/searchDetails?applyNo=%s'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }

    def __init__(self):
        pass

    def start(self):
        numbers = [x for x in range(20180604000001, 20180604020000)]
        numbers += [x for x in range(20180605000001, 20180605020000)]
        numbers += [x for x in range(20180606000001, 20180606020000)]
        pool.map(self.process, numbers)

    @func_set_timeout(60)
    def stop(self):
        while True:
            session = DBSession()
            result = session.query(FailProcess).filter_by(status=1).all()
            if len(result) > 0:
                for r in result:
                    if session.query(Registration).filter_by(number=r.number).first() is None:
                        self.process(r.number)

                    r.status = '0'
                    session.commit()
                    continue
            break

    def process(self, number):
        status = 'success'

        try:
            response = self.get_registration(number)
            data = self.response_process(response)

            if 'number' in data.keys() and data['number']:
                self.save(data)
        except:
            self.save_fail({
                'number': number,
                'status': '1'
            })
            status = 'failure'
        finally:
            logger.info('process %s: %s', status, number)

    def get_registration(self, number):
        response = requests.get(self.url % number, headers=self.headers)

        # with open('html/' + str(number) + '.html', 'wb') as fp:
        #     fp.write(response.content)

        return response.text

    @staticmethod
    def response_process(response):
        data = dict()

        root = etree.HTML(response)
        html = etree.ElementTree(root)

        if html.xpath('//th[text()="购房登记号："]/following-sibling::td'):
            data['pur_apply'] = html.xpath('//th[text()="购房登记申请结果："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="购房登记申请结果："]/following-sibling::td') else ''
            data['status'] = html.xpath('//th[not(text())]/following-sibling::td/b/text()')[0].strip() if html.xpath('//th[not(text())]/following-sibling::td/b') else ''
            data['type'] = html.xpath('//th[text()="购房登记类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="购房登记类型："]/following-sibling::td') else ''
            data['family_type'] = html.xpath('//th[text()="家庭类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="家庭类型："]/following-sibling::td/text()') else ''
            data['divorce_time'] = html.xpath('//th[text()="离婚登记时间"]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="离婚登记时间"]/following-sibling::td/text()') else ''
            data['number'] = html.xpath('//th[text()="购房登记号："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="购房登记号："]/following-sibling::td') else ''
            data['area'] = html.xpath('//th[text()="项目所在区域："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="项目所在区域："]/following-sibling::td') else ''
            data['license'] = html.xpath('//th[text()="预/现售证号："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="预/现售证号："]/following-sibling::td') else ''

            data['person_type'] = html.xpath('//th[text()="人员类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="人员类型："]/following-sibling::td/text()') else ''
            data['certificate_type'] = html.xpath('//th[text()="证件类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="证件类型："]/following-sibling::td/text()') else ''
            data['username'] = html.xpath('//th[text()="姓名："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="姓名："]/following-sibling::td') else ''
            data['id_card'] = html.xpath('//th[text()="证件号码："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="证件号码："]/following-sibling::td') else ''
            data['is_join'] = html.xpath('//th[text()="是否参与购房登记"]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="是否参与购房登记"]/following-sibling::td') else ''
            data['talent_type'] = html.xpath('//th[text()="人才类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="人才类型："]/following-sibling::td') else ''
            data['household_area'] = html.xpath('//th[text()="户籍所在区域："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="户籍所在区域："]/following-sibling::td/text()') else ''
            data['social_type'] = html.xpath('//th[text()="社保类型："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="社保类型："]/following-sibling::td') else ''
            data['social_number'] = html.xpath('//th[text()="社保编码："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="社保编码："]/following-sibling::td') else ''
            data['company_name'] = html.xpath('//th[text()="缴存单位名称："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="缴存单位名称："]/following-sibling::td') else ''
            data['certificate_company_name'] = html.xpath('//th[text()="出具证明的单位名称："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="出具证明的单位名称："]/following-sibling::td') else ''
            data['stationed'] = html.xpath('//th[text()="服役部队驻扎地："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="服役部队驻扎地："]/following-sibling::td') else ''
            data['full_name_troops'] = html.xpath('//th[text()="部队全称："]/following-sibling::td/text()')[0].strip() if html.xpath('//th[text()="部队全称："]/following-sibling::td') else ''

            data['create_time'] = time.time()

        return data

    @staticmethod
    def save(data):
        session = DBSession()
        registration = Registration(**data)
        session.add(registration)
        session.commit()

    @staticmethod
    def save_fail(data):
        session = DBSession()
        fail_process = FailProcess(**data)
        session.add(fail_process)
        session.commit()


if __name__ == '__main__':
    process = Process()
    # process.start()
    process.stop()
