# -*- coding: utf-8 -*-
"""
OTR file rename for tv-shows
Extract all information from the (decoded) otrkey file name (onlinetvrecorder.com)
and use the website fernsehserien.de to rename the file with the episode and season info  

@author: Jens
"""
import re
import tv_scraper_fernsehsendungen_de as scraper
import os
from datetime import datetime

def getFileInfo(filename):
    extension = os.path.splitext(filename)[1]

    m=re.search("(.*)_([0-9]{2}\.[0-9]{2}\.[0-9]{2})_([0-9]{2}\-[0-9]{2})_([A-Za-z0-9]+)", filename)
    title = m.group(1)
    title = title.split('__')[0] # for US series SeriesName__EpisodeTitle (problems with shows like CSI__NY)
    title = title.replace("_",'-')
    seriesdate = m.group(2)
    seriestime = m.group(3)
    sender = m.group(4)
    
    return title,seriesdate,sender,extension,seriestime

def queryEpisodeInfo(title):
    serieslinks = {'The Big Bang Theory' : 'the-big-bang-theory',
                   'The-Simpsons' : 'die-simpsons'} #to be continued...

    if serieslinks.has_key(title):
        title = serieslinks(title)
        
    page = scraper.getWebPage(title)
    d = scraper.getDateGerman(page)
    s = scraper.getSeasonNumber(page)
    e = scraper.getEpisodeNumber(page)
    t = scraper.getTitlesGerman(page)
    
    return d,s,e,t


def searchDate(date, date_list): 
    date=datetime.strptime(date,"%y.%m.%d")
    for index, item in enumerate(date_list):
        if item != u'\xa0':
            actualdate = datetime.strptime(item,"%d.%m.%Y")
            if actualdate.date() == date.date():
                return index

def buildNewFileName(filename):
    showtitle,date,sender,extension,seriestime = getFileInfo(filename) 
    date_list,season,episode,eptitle = queryEpisodeInfo(showtitle)
    idx = searchDate(date, date_list)
    
    print showtitle.replace('-',' ') + '.' + 'S' + season[idx] + 'E' + episode[idx] + '.' + eptitle[idx] + extension

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        buildNewFileName(filename)
    else:
        print 'Usage: ' + sys.argv[0] + ' filename'

               
