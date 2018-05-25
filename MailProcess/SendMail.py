# -*- coding: utf-8 -*-
__author__ = 'XIUERY'

import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import parseaddr, formataddr


class Mail:
    smtp = None

    def __init__(self, host='localhost', port=25, auth=False, username='', password=''):
        self.host = host
        self.port = port
        self.auth = auth
        self.username = username
        self.password = password

        self.smtp = smtplib.SMTP(self.host)
        # self.smtp.set_debuglevel(1)

    def send(self, subject, from_address, to_address, cc_address, body, attaches=[], type='plain'):

        msg = self.get_msg(subject, body, from_address, to_address, cc_address, attaches, type)

        try:
            self.smtp.sendmail(list(from_address)[0], list(dict(to_address, **cc_address).keys()), msg)
        except:
            raise
        finally:
            self.quit()

    def get_msg(self, subject, body, from_address, to_address, cc_address, attaches, type='plain'):

        # 构建普通邮件正文
        # msg = MIMEText(body, type, 'utf-8')
        # 构建带附件的邮件正文
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, type, 'utf-8'))

        msg['Subject'] = Header(subject, 'utf-8')

        msg_from_address = '%s ' % tuple(from_address.values()) + '<%s>' % tuple(from_address)
        msg['From'] = self.format_address(msg_from_address)

        msg_to_address = []
        for address, name in zip(list(to_address), list(to_address.values())):
            msg_to_address.append('%s <%s>' % (name, address))
        to = []
        for address in msg_to_address:
            to.append(self.format_address(address))
        msg['To'] = ','.join(to)

        msg_cc_address = []
        for address, name in zip(list(cc_address), list(cc_address.values())):
            msg_cc_address.append('%s <%s>' % (name, address))
        cc = []
        for address in msg_cc_address:
            cc.append(self.format_address(address))
        msg['Cc'] = ','.join(cc)

        msg = self.add_attach(msg, attaches)

        return msg.as_string()

    @staticmethod
    def add_attach(msg, attaches):
        for attach in attaches:
            with open(attach, 'rb') as f:
                mime = MIMEApplication(f.read())
                mime.add_header('Content-Disposition', 'attachment', filename=os.path.split(f.name)[1])
                msg.attach(mime)
        return msg

    @staticmethod
    def format_address(address):
        name, addr = parseaddr(address)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def quit(self):
        self.smtp.quit()


