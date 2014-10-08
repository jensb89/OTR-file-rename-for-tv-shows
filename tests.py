#!/usr/bin/env python
# -*- coding: utf-8 -*-
from otr_rename import OTR_Rename

otrfile = OTR_Rename('Die_Simpsons_14.09.15_20-15_pro7_25_TVOON_DE.avi')
filename_neu = otrfile.buildNewFilename()
print filename_neu

otrfile = OTR_Rename('Sleepy_Hollow__This_Is_War_14.09.22_21-00_uswnyw_60_TVOON_DE.avi')
filename_neu = otrfile.buildNewFilename()
print filename_neu

otrfile = OTR_Rename('The_Blacklist_14.02.04_21-15_rtl_60_TVOON_DE.avi.otrkey')
filename_neu = otrfile.buildNewFilename()
print filename_neu

#otrfile.copy_and_sort()

print OTR_Rename('Die_Simpsons_14.09.15_20-15_pro7_25_TVOON_DE.avi').buildNewFilename()
