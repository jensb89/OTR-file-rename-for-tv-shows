#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OTR file rename for tv-shows
Extract all information from the (decoded) otrkey file name (onlinetvrecorder.com)
and use the website fernsehserien.de to rename the file with the episode and season info  

@author: Jens
"""

import re
#import tv_scraper_fernsehsendungen_de as scraper
#import tv_scraper_fernsehsendungen_de_sendetermine as scraper_timetable
import os
from datetime import datetime
import time
from shutil import move
from time import localtime

from bs4 import BeautifulSoup
from urllib import urlopen
from math import fmod
import re
from types import * 
import codecs
import os
import fernsehserien_de_links as tlinks

#Windows Hook for UTF-8 in console
codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

class OTR_Rename(object):
    def __init__(self, filename):
        self.file = filename
        self.parseFileInfo()

    def parseFileInfo(self):
        # Get Title, date and so on from filename
        self.extension = os.path.splitext(self.file)[1]
        m = re.search("(.*)_([0-9]{2}\.[0-9]{2}\.[0-9]{2})_([0-9]{2}\-[0-9]{2})_([A-Za-z0-9]+)", self.file)
        title = m.group(1)
        title = title.split('__')[0] # for US series SeriesName__EpisodeTitle (problems with shows like CSI__NY)
        self.show = title.replace("_",' ')
        self.epdate = m.group(2)
        self.eptime = m.group(3)
        self.sender = m.group(4)
        if self.sender[:2] != 'us':
            self.lang='de'
        else:
            self.lang='us'
        print self.lang

    def queryEpisodeInfo(self):
        self.scraper = Fernsehserien_de_Scraper(self.show)

        if self.lang == 'us':
            (d,s,e,t) = self.scraper.getEpisodeGuide(lang='us')

        if self.lang == 'de':
            (d,s,e,t,time_list) = self.scraper.getTimeTable(self.sender)

        # Find match in Date
        if not(d[:]):
            idx = False
        else:
            idx = self.searchDate(self.epdate, d)
        # Found match:     
        if str(idx).isdigit():
            if self.lang == 'de':
                idx = self.checkFollowingDateEntry(self.epdate, self.eptime, d, time_list, idx-1 if idx>0 else idx) #Search for closest eptime on the date
            date, season, episode, title = d[idx], s[idx], e[idx], t[idx]
        else: # No match
            date, season, episode, title = None, None, None, None
        
        return date, season, episode, title

    def buildNewFilename(self):
        # Get filename from the scraped webpage
        date, season, episode, title = self.queryEpisodeInfo()
        if None in (date, season, episode, title):
            newfilename = False
        else:
            newfilename = self.show + '.' + 'S' + season + 'E' + episode + '.' + title + self.extension

        return newfilename

    def copy_and_sort(self):
        if not(os.path.isdir(self.show)):
           os.mkdir(title)
       
        log = open('log.txt','a')
        lt = localtime()
        jahr, monat, tag, stunde, minute = lt[0:5]
        log.write(str(jahr)+'-'+ str(monat) +'-'+ str(tag) +' '+ str(stunde) +':'+ str(minute) +' : ')
        #log.write(strftime("%Y-%m-%d %H:%I"))
        log.write("input  " + self.file + "\n")

        newfilename = self.buildNewFilename()
        if newfilename != False:
            newfilename = "".join(i for i in newfilename if i not in r'\/:*?"<>|') 
            newpath = self.show + '/' + newfilename
        else:
            newpath = self.show + '/' + self.file
        
        if not(os.path.isfile(newpath)):
            move(self.file, newpath)
            log.write(str(jahr)+'-'+ str(monat) +'-'+ str(tag) +' '+ str(stunde) +':'+ str(minute) +' : ')
            log.write("output " + newpath + "\n\n")
            print self.file + ' moved to ' + newpath
            #log.write(filename + ' was copied to ' + newpath + '\n')       
        
        log.close()


    @staticmethod
    def searchDate(date, date_list): 
        date=datetime.strptime(date,"%y.%m.%d")
        for index, item in enumerate(date_list):
            if item != u'\xa0' and item != '':
                actualdate = datetime.strptime(item,"%d.%m.%Y")
                if actualdate.date() == date.date():
                    return index

    @staticmethod
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


class Fernsehserien_de_Scraper(object):
    # Parse the EpisodeGuide Page from Fernsehserien.de - get back all episodes as a list
    def __init__(self, show):
        self.name = show #e.g. 'Die Simpsons'

    ######  DOWNLOADING WEBPAGE : Fernsehserien - EpisodeGuide ########
    def downloadWebpage(self):
        print 'Trying to get website information...please wait...'
        cache = self.name + '/' + 'eplist.dat'
        if os.path.isfile(cache) and (time.time() - os.path.getmtime(cache)) < 43200:
            print "Use local file..."        
            webpage = urlopen(cache)
        else:
            if tlinks.serieslinks.has_key(self.name):
                title = tlinks.serieslinks[self.name.replace(' ','-')]
            else:
                title = self.name.replace(' ','-')
                
            webpage = urlopen('http://www.fernsehserien.de/'+title+'/episodenguide').read()
            
            if not(os.path.isdir(self.name.replace('-',' '))):
                os.mkdir(self.name.replace('-',' '))
                
            f = open(cache,'w')
            f.write(webpage)
            f.close()
            
        print 'Website successfully scraped'
        self.soupobj = BeautifulSoup(webpage, "html.parser")
        #print self.soupobj.prettify()
    

    def getTitlesGerman(self):
        episodetitlesger = self.soupobj.select("td.episodenliste-titel")
        for i in episodetitlesger:
            if type(i.find('span')) is not NoneType:
                i.find('span').decompose()
            
        return [x.text for x in episodetitlesger]
        

    def getTitles(self):
        episodetitles = self.soupobj.select("td.episodenliste-originaltitel")
        return [x.text for x in episodetitles]
        
        
    def getDate(self):
        episodedate = self.soupobj.select("td.episodenliste-oea")
        return [x.text.rstrip('\r\n') for x in episodedate]
        
        
    def getDateGerman(self):
        episodedate = self.soupobj.select("td.episodenliste-ea")
        for i in episodedate:
            if type(i.find('span')) is not NoneType:
                i.find('span').decompose()
        
        return [x.text for x in episodedate]
        
        
    def getSeasonNumber(self):
        episodenumber = self.soupobj.select("td.episodenliste-episodennummer span")
        return [episodenumber[2*i].text.replace('.','') for i in range(0,len(episodenumber)/2)]
        

    def getEpisodeNumber(self):
        episodenumber = self.soupobj.select("td.episodenliste-episodennummer span")
        return [episodenumber[2*i+1].text.replace('.','') for i in range(0,len(episodenumber)/2)]
        

    def getCountEpisode(self):
        return len(self.soupobj.select('td.episodenliste-originaltitel'))
        
        
    def getEpisodeGuide(self, lang = 'de', printout = False):
        self.downloadWebpage()
        s = self.getSeasonNumber()
        e = self.getEpisodeNumber()

        if lang == 'de':
            d, t = self.getDateGerman(), self.getTitlesGerman()
        else:
            d, t = self.getDate(), self.getTitles()

        #print len(getTitles(soup))
        
        if printout:
            for i in range(0,getCountEpisode(soup)):
                print 'S' + s[i] + '.' + 'E'+ e[i] + ' : ' + t[i] + '( ' + d[i] + ' )'    

        return (d,s,e,t)


    ######  DOWNLOADING WEBPAGE : Fernsehserien - TimeTable ########
    def getTimeTable(self, sender):
        print 'Trying to get timetable information...please wait...'
                      
        if tlinks.senderlist.has_key(sender):
            senderlink = tlinks.senderlist[sender]
        else:
            print 'Link zu Sender ' + sender +' nicht gefunden'
            return 0
        
        cache = self.name.replace('-',' ') + '/' + 'ttlist.dat'
        if os.path.isfile(cache) and (time.time() - os.path.getmtime(cache)) < 43200:
            print "Use local file..."        
            webpage = urlopen(cache)
        else:
            if tlinks.serieslinks.has_key(self.name.replace(' ','-')):
                title = tlinks.serieslinks[self.name.replace(' ','-')]
            else:
                title = self.name.replace(' ','-')
                
            webpage = urlopen('http://www.fernsehserien.de/'+title+'/sendetermine/'+senderlink+'/-1').read()
            
            if not(os.path.isdir(self.name)):
                os.mkdir(self.name)
                
            f = open(cache,'w')
            f.write(webpage)
            f.close()   
            
        
        print 'Website successfully scraped'
        #soup = BeautifulSoup(fernsehserien_testdata.gethtmlo(), "html.parser")
        soup = BeautifulSoup(webpage, "html.parser")
        tddata = soup.select("tr")

        epdate, eptime, season, episode, title = [],[],[],[],[]
        
        for index, item in enumerate(tddata):
            if fmod(index,2) != 0 and index>0:
                #print item.text
                m = re.search("(\d{2}\.\d{2}\.\d{4}).*?(\d{2}:\d{2}).*?>(\d{1,3})<.*?>(\d{1,2}).*?>(\d{1,2}).*?>([^<]+)", str(item))
                if type(m) is not NoneType:            
                    epdate.append(m.group(1))
                    eptime.append(m.group(2))
                    season.append(m.group(4))
                    episode.append(m.group(5))
                    title.append(m.group(6))
                    
        return (epdate, season, episode, title, eptime)    
