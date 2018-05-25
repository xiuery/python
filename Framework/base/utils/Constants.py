# -*- coding: utf-8 -*-
__author__ = 'Kerwin zhang'

import os
from os.path import dirname as dn, abspath


ROOT_DIR = dn(dn(dn(abspath(__file__))))
LOG_PATH = os.path.join(ROOT_DIR, "log")
