#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get all information about a tv show from fernsehserien.de
(seasons, episodes and dates (german) )

@author: Jens
"""

from bs4 import BeautifulSoup
from urllib import urlopen
from math import fmod
import re
from types import * 
import codecs
import os
import fernsehserien_de_links as tlinks
import time

def getSeriesTimeTable(seriesname, sender):
    print 'Trying to get timetable information...please wait...'
                  
    if tlinks.senderlist.has_key(sender):
        senderlink = tlinks.senderlist[sender]
    else:
        print 'Link zu Sender ' + sender +' nicht gefunden'
        return 0
    
    cache = seriesname.replace('-',' ') + '/' + 'ttlist.dat'
    if os.path.isfile(cache) and (time.time() - os.path.getmtime(cache)) < 43200:
        print "Use local file..."        
        webpage = urlopen(cache)
    else:
        if tlinks.serieslinks.has_key(seriesname):
            title = tlinks.serieslinks[title]
        else:
            title = seriesname
            
        webpage = urlopen('http://www.fernsehserien.de/'+title+'/sendetermine/'+senderlink+'/-1#jahr-2013').read()
        
        if not(os.path.isdir(seriesname.replace('-',' '))):
            os.mkdir(seriesname.replace('-',' '))
            
        f = open(cache,'w')
        f.write(webpage)
        f.close()   
        
    
    print 'Website successfully scraped'
    #soup = BeautifulSoup(fernsehserien_testdata.gethtmlo(), "html.parser")
    soup = BeautifulSoup(webpage, "html.parser")
    tddata = soup.select("tr")

    epdate = []
    eptime = []
    season = []
    episode = []
    title =[]
    
    for index, item in enumerate(tddata):
        if fmod(index,2) != 0 and index>0:
            #print item.text
            m = re.search("([0-9]{2}\.[0-9]{2}\.[0-9]{4})([0-9]{2}\:[0-9]{2}).*([0-9]{1})\.([0-9]{2})(.*)", item.text)
            if type(m) is not NoneType:            
                epdate.append(m.group(1))
                eptime.append(m.group(2))
                season.append(m.group(3))
                episode.append(m.group(4))
                title.append(m.group(5))
                
    return (epdate, season, episode, title, eptime)    
    
def main(seriesname, sender):
    d,s,e,t,time = getSeriesTimeTable(seriesname, sender)
    
    for i in range(0,len(d)):
        print 'S' + s[i] + '.' + 'E'+ e[i] + ' : ' + t[i] + '( ' + d[i] + ' )'         


if __name__ == '__main__':
    import sys
    """ 
    Deal with Windows Output/ Codecs (see http://stackoverflow.com/questions/5419/python-unicode-and-the-windows-console for more info)
    """
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    #print sys.getdefaultencoding()
    
    if sys.platform == 'win32':
        try:
            import win32console 
        except:
            print "Python Win32 Extensions module is required.\n You can download it from https://sourceforge.net/projects/pywin32/ (x86 and x64 builds are available)\n"
            exit(-1)
        # win32console implementation  of SetConsoleCP does not return a value
        # CP_UTF8 = 65001
        win32console.SetConsoleCP(65001)
        if (win32console.GetConsoleCP() != 65001):
            raise Exception ("Cannot set console codepage to 65001 (UTF-8)")
        win32console.SetConsoleOutputCP(65001)
        if (win32console.GetConsoleOutputCP() != 65001):
            raise Exception ("Cannot set console output codepage to 65001 (UTF-8)")
    
    #import sys, codecs
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    sys.stderr = codecs.getwriter('utf8')(sys.stderr)
    print "This is an Е乂αmp١ȅ testing Unicode support using Arabic, Latin, Cyrillic, Greek, Hebrew and CJK code points.\n"
    """
    //END
    """
    if len(sys.argv)>2:
        seriesname = sys.argv[1]
        sender = sys.argv[2]
        main(seriesname, sender)
     