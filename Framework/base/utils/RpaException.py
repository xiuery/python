# -*- coding: utf-8 -*-
__author__ = 'Kerwin zhang'


class RpaException(Exception):
    def __str__(self):
        return 'An unspecified Robot error has occurred'
