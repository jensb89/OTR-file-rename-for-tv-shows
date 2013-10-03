# -*- coding: utf-8 -*-
"""
Get all information about a tv show from fernsehserien.de
(seasons, episodes and dates (german) )

@author: Jens
"""

from bs4 import BeautifulSoup
from urllib import urlopen
from types import * 
import codecs, sys

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

def getWebPage(seriesname):
    print 'Trying to get website information...please wait...'
    webpage = urlopen('http://www.fernsehserien.de/'+seriesname+'/episodenguide').read()
    print 'Website successfully scraped'
    soup = BeautifulSoup(webpage, "html.parser")
    #print soup.prettify()
    return soup
    

def getTitlesGerman(soupobj):
    episodetitlesger = soupobj.select("td.episodenliste-titel")
    for i in episodetitlesger:
        if type(i.find('span')) is not NoneType:
            i.find('span').decompose()
        
    return [x.text for x in episodetitlesger]
    

def getTitles(soupobj):
    episodetitles = soupobj.select("td.episodenliste-originaltitel")
    return [x.text for x in episodetitles]
    
    
def getDate(soupobj):
    episodedate = soupobj.select("td.episodenliste-oea")
    return [x.text for x in episodedate]
    
    
def getDateGerman(soupobj):
    episodedate = soupobj.select("td.episodenliste-ea")
    for i in episodedate:
        if type(i.find('span')) is not NoneType:
            i.find('span').decompose()
    
    return [x.text for x in episodedate]
    
    
def getSeasonNumber(soupobj):
    episodenumber = soupobj.select("td.episodenliste-episodennummer span")
    return [episodenumber[2*i].text.replace('.','') for i in range(0,len(episodenumber)/2)]
    

def getEpisodeNumber(soupobj):
    episodenumber = soupobj.select("td.episodenliste-episodennummer span")
    return [episodenumber[2*i+1].text.replace('.','') for i in range(0,len(episodenumber)/2)]
    

def getCountEpisode(soupobj):
    return len(soupobj.select('td.episodenliste-originaltitel'))
    
    
def main(seriesname):
    soup = getWebPage(seriesname)
    s = getSeasonNumber(soup)
    e = getEpisodeNumber(soup)
    d = getDateGerman(soup)
    t = getTitlesGerman(soup)
    print len(getTitles(soup))
    
    for i in range(0,getCountEpisode(soup)):
        print 'S' + s[i] + '.' + 'E'+ e[i] + ' : ' + t[i] + '( ' + d[i] + ' )'         

#main('the-big-bang-theory')

if __name__ == '__main__':
    import sys
    if len(sys.argv)>1:
        seriesname = sys.argv[1]
        main(seriesname)
     