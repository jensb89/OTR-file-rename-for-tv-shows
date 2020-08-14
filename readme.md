# OTR file rename for tv-shows

Extract all information from the (decoded) otrkey file name (onlinetvrecorder.com)
and use the website fernsehserien.de to rename the file with the episode and season info 

## Install ##

### Prerequisites ###

You need Python and the extension Beautiful Soup 4 installed. 

For Beautiful Soup on Windows:

Download easy_setup (https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py)
````
$ python ez_setup.oy
$ easy_install BeautifulSoup4
````

## USAGE ##
Just get information
_______________________
````
$ python otr_rename.py otrkey-filename
````
Example:
````
$ python otr_rename.py The_Big_Bang_Theory_13.09.02_21-10_pro7_30_TVOON_DE.mpg.otrkey
> The Big Bang Theory.S1E15.Spoileralarm!.otrkey
````


RENAME AND MOVE ALL AVI FILES in the current folder:
_______________________
````
$ python move_batch.py
````

This will create a new folder for each tv-show and rename the file respectively.
Also a log.txt file will be created

For a folder somewhere else use:
````
$ python move_batch.py /volume1/folder_with_avi_files/
````

Example output:
````
2014-1-26 23:34 : input  The_Blacklist_14.01.21_20-15_rtl_55_TVOON_DE.avi
2014-1-26 23:34 : output The Blacklist/The Blacklist.S1E01.Raymond Reddingtons schwarze Liste.avi

2014-1-26 23:34 : input  The_Blacklist_14.01.21_21-10_rtl_55_TVOON_DE.avi
2014-1-26 23:34 : output The Blacklist/The Blacklist.S1E02.Der Freelancer (Nr. 145).avi

2014-1-30 19:51 : input  Die_Simpsons_14.01.27_20-15_pro7_30_TVOON_DE.avi
2014-1-30 19:51 : output Die Simpsons/Die Simpsons.S24E15.Blauauge sei wachsam.avi

2014-1-30 19:51 : input  Revolution__Happy_Endings_14.01.29_20-00_uswnbc_60_TVOON_DE.avi
2014-1-30 19:51 : output Revolution/Revolution.S2E13.Happy Endings.avi

2014-1-30 19:51 : input  The_Originals__Dance_Back_From_the_Grave_14.01.28_20-00_uswpix_60_TVOON_DE.avi
2014-1-30 19:51 : output The Originals/The Originals.S1E12.Dance Back From The Dead.avi
````

## Info / Disclaimer
This project started as a personal project. It is just for educational purposes and private usage without any warranty or liability. 
