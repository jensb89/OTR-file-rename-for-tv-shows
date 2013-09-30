# -*- coding: utf-8 -*-
"""
Get all information about a tv show from fernsehserien.de
(seasons, episodes and dates (german) )

@author: Jens
"""

from bs4 import BeautifulSoup
from urllib import urlopen
from types import * 

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
     