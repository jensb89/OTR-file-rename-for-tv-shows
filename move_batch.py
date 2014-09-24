#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Search for avi files and move them in the right folder
"""

import os
import move_tv_show

files = [f for f in os.listdir(".") if f.endswith('.avi')]

for filename in files:
    print filename
    move_tv_show.copysort(filename)





