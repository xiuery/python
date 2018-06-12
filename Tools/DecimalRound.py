# -*- coding: utf-8 -*-
__author__ = 'XIUERY'

'''
python3 四舍五入
'''

import decimal
from decimal import Decimal


def decimal_round(unit_price):
    context = decimal.getcontext()
    context.rounding = decimal.ROUND_HALF_UP
    return round(Decimal(unit_price), 2)
