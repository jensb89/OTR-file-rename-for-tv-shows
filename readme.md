**OTR file rename for tv-shows**

Extract all information from the (decoded) otrkey file name (onlinetvrecorder.com)
and use the website fernsehserien.de to rename the file with the episode and season info 

# Install #

## Prerequisites ##

You need Python and the extension Beautiful Soup 4 installed. 

For Beautiful Soup on Windows:

Download easy_setup (https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py)
````
$ python ez_setup.oy
$ easy_install BeautifulSoup4
````

# USAGE #
Just get information
_______________________
````
$ python otr_rename.py otrkey-filename
````
Example:
````
$ python otr_rename The_Big_Bang_Theory_13.09.02_21-10_pro7_30_TVOON_DE.mpg.otrkey
> The Big Bang Theory.S1E15.Spoileralarm!.otrkey
````


RENAME AND MOVE ALL AVI FILES in the current folder:
_______________________
````
$ python move_batch.py
````

This will create a new folder for each tv-show and rename the file respectively.
Also a log.txt file will be created

Example output:
````
Marvel_s_Agents_of_S_H_I_E_L_D___0-8-4_13.10.01_20-00_uswabc_61_TVOON_DE.avi was copied to Marvel s Agents of S H I E L D/Marvel s Agents of S H I E L D.S1E02.0–8-4.avi
Sleepy_Hollow__For_the_Triumph_of_Evil_13.09.30_21-00_uswnyw_60_TVOON_DE.avi was copied to Sleepy Hollow/Sleepy Hollow.S1E03.For The Triumph Of Evil.avi
Supernatural_13.10.05_01-15_pro7_55_TVOON_DE.avi was copied to Supernatural/Supernatural.S7E16.Von schwarzen Schwänen.avi
Supernatural_13.10.05_02-10_pro7_45_TVOON_DE.avi was copied to Supernatural/Supernatural.S7E17.Identitätsverlust.avi
````
