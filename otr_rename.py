#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OTR file rename for tv-shows
Extract all information from the (decoded) otrkey file name (onlinetvrecorder.com)
and use the website fernsehserien.de to rename the file with the episode and season info  

@author: Jens
"""
import re
import tv_scraper_fernsehsendungen_de as scraper
import tv_scraper_fernsehsendungen_de_sendetermine as scraper_timetable
import os
from datetime import datetime
import time

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
    

def queryEpisodeInfo(title, lang):
    page = scraper.getWebPage(title)
    if lang == 'de':
        d = scraper.getDateGerman(page)
        t = scraper.getTitlesGerman(page)
    else:
        d = scraper.getDate(page)
        t = scraper.getTitles(page)
        
    s = scraper.getSeasonNumber(page)
    e = scraper.getEpisodeNumber(page)
    
    
    return d,s,e,t


def searchDate(date, date_list): 
    date=datetime.strptime(date,"%y.%m.%d")
    for index, item in enumerate(date_list):
        if item != u'\xa0' and item != '':
            actualdate = datetime.strptime(item,"%d.%m.%Y")
            if actualdate.date() == date.date():
                return index
                

def checkFollowingDateEntry(date,stime,date_list,time_list,idx):
    tc = time.strptime(date+' '+stime,"%y.%m.%d %H-%M")  #Time from filename 
    
    actual=time.strptime(date_list[idx]+' '+time_list[idx],"%d.%m.%Y %H:%M")
    
    if idx < len(date_list)-2:
        after=time.strptime(date_list[idx+1]+' '+time_list[idx+1],"%d.%m.%Y %H:%M")
    else:
        return idx
    
    trynext = True
    while trynext:

        diffactual= abs(time.mktime(actual)-time.mktime(tc))
        diffnext= abs(time.mktime(after)-time.mktime(tc))
        
        if diffactual > diffnext and idx < len(date_list)-2:
            idx=idx+1
            actual = time.strptime(date_list[idx]+' '+time_list[idx],"%d.%m.%Y %H:%M")
            after = time.strptime(date_list[idx+1]+' '+time_list[idx+1],"%d.%m.%Y %H:%M")  
        elif diffactual > diffnext and idx == len(date_list)-2:
            idx=idx+1
            trynext = False
        else:
            trynext = False
            
    return idx
           
    

def buildNewFileName(filename):
    showtitle,date,sender,extension,seriestime = getFileInfo(filename)
    if sender[:2] != 'us':
        lang='de'
    else:
        lang='us'
        
    date_list,season,episode,eptitle = queryEpisodeInfo(showtitle, lang)
    #print showtitle + ':' + date + '  ' + seriestime    
    #print date
    #print date_list
    
    idx = searchDate(date, date_list)
    if lang== 'us' and str(idx).isdigit():
        newfilename = showtitle.replace('-',' ') + '.' + 'S' + season[idx] + 'E' + episode[idx] + '.' + eptitle[idx] + extension
    else:
        if lang == 'de':
            date_list,season,episode,eptitle,time_list = scraper_timetable.getSeriesTimeTable(showtitle, sender)
            if not(date_list[:]):
                idx = False
            else:
                idx = searchDate(date, date_list)
            if str(idx).isdigit():
                idx = checkFollowingDateEntry(date,seriestime,date_list,time_list,idx-1 if idx>0 else idx)
                newfilename = showtitle.replace('-',' ') + '.' + 'S' + season[idx] + 'E' + episode[idx] + '.' + eptitle[idx] + extension
            else:
                newfilename = False
                print 'Keine Uebereinstimmung'
        else:
            newfilename = False
            print 'Keine Uebereinstimmung'
    
    return newfilename
        
        
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        newfilename = buildNewFileName(filename)
        if newfilename != False:
            print newfilename
    else:
        print 'Usage: ' + sys.argv[0] + ' filename'

               
