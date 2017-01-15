#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Search for avi files and move them in the right folder
"""

import os
from otr_rename import OTR_Rename
import sys

folder = "."

if __name__ == '__main__':
	if len(sys.argv) == 2:
		folder = sys.argv[1]
	else:
		folder = "."

files = [f for f in os.listdir(folder) if f.endswith('.avi')]

for filename in files:
    print filename
    tv_show = OTR_Rename(os.path.join(folder,filename))
    tv_show.copy_and_sort()





