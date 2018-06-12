# -*- coding: utf-8 -*-
__author__ = 'XIUERY'

from dateutil.relativedelta import relativedelta


def relative_delta(dt, plus=True,
                   years=0, months=0, days=0,
                   hours=0, minutes=0, seconds=0,
                   weeks=0):

    if plus is True:
        return dt + relativedelta(years=years, months=months, days=days,
                                  hours=hours, minutes=minutes, seconds=seconds,
                                  weeks=weeks)
    else:
        return dt - relativedelta(years=years, months=months, days=days,
                                  hours=hours, minutes=minutes, seconds=seconds,
                                  weeks=weeks)


if __name__ == "__main__":
    from datetime import date, datetime
    dt0 = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    dt1 = relative_delta(datetime.today(), plus=False, years=1, months=7, weeks=1)
    dt2 = relative_delta(date.today(), plus=True, years=1, months=7, weeks=1)
    print(dt0)
    print(dt1)
    print(dt2)
