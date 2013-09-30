**OTR file rename for tv-shows**

Extract all information from the (decoded) otrkey file name (onlinetvrecorder.com)
and use the website fernsehserien.de to rename the file with the episode and season info 

## Install 
You need Beautiful Soup 4 installed. 

# Windows:
Download easy_setup (https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py)
````
$ python ez_setup.oy
$ easy_install BeautifulSoup4

## USAGE 
````
$ python otr_rename.py otrkey-filename
````

Until now, it just creates a new String for a given file name string:
````
$ python otr_rename The_Big_Bang_Theory_13.09.02_21-10_pro7_30_TVOON_DE.mpg.otrkey
> The Big Bang Theory.S1E15.Spoileralarm!.otrkey
````

More in a future update...
