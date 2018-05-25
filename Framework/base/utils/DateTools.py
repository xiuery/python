import time
import xlrd


class DateTools(object):
    @staticmethod
    def date_dec(date_str, days, date_format='%m/%d/%Y'):
        date_value = time.strptime(date_str, date_format)
        date_value = int(time.mktime(date_value)) - 86400 * days

        date_value = time.localtime(date_value)
        date_value = time.strftime(date_format, date_value)
        return date_value

    @staticmethod
    def yesterday(date_format='%m/%d/%Y'):
        return DateTools.format_time_stamp(int(time.time()) - 86400, date_format)

    @staticmethod
    def format_time_stamp(time_stamp, date_format='%m/%d/%Y'):
        return time.strftime(date_format, time.localtime(time_stamp))

    @staticmethod
    def excel_date_format(time_stamp, date_format='%m/%d/%Y'):
        date_value = xlrd.xldate_as_datetime(time_stamp, 0)
        return date_value.strftime(date_format)


if __name__ == '__main__':
    pass
    # tz = pytz.timezone('Canada/Mountain')
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # print(datetime.now().timestamp())

