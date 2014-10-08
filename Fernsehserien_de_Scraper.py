#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OTR file rename for tv-shows
Extract all date, time, season and episode information for a specific TV-Show from fernsehserien.de

@author: Jens
"""

from bs4 import BeautifulSoup
from urllib import urlopen
from math import fmod
import re
from types import * 
import os
from tv_shows_db import serieslinks
from tv_stations_db import senderlinks
import time


class Fernsehserien_de_Scraper(object):
    # Parse the EpisodeGuide Page from Fernsehserien.de - get back all episodes as a list

    CACHE_FOLDER = '.cache'

    def __init__(self, show):
        self.name = show #e.g. 'Die Simpsons'

    ######  DOWNLOADING WEBPAGE : Fernsehserien - EpisodeGuide ########
    def downloadWebpage(self):
        print 'Trying to get website information...please wait...'
        cache = Fernsehserien_de_Scraper.CACHE_FOLDER + '/' + self.name + '_' + 'eplist.dat'
        if os.path.isfile(cache) and (time.time() - os.path.getmtime(cache)) < 43200:
            print "Use local file..."        
            webpage = urlopen(cache)
        else:
            if serieslinks.has_key(self.name):
                title = serieslinks[self.name.replace(' ','-')]
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
                      
        if senderlinks.has_key(sender):
            senderlink = tlinks.senderlist[sender]
        else:
            print 'Link zu Sender ' + sender +' nicht gefunden'
            return 0
        
        cache = Fernsehserien_de_Scraper.CACHE_FOLDER + '/' + self.name + '_ttlist.dat'
        if os.path.isfile(cache) and (time.time() - os.path.getmtime(cache)) < 43200:
            print "Use local file..."        
            webpage = urlopen(cache)
        else:
            if serieslinks.has_key(self.name.replace(' ','-')):
                title = serieslinks[self.name.replace(' ','-')]
            else:
                title = self.name.replace(' ','-')
                
            webpage = urlopen('http://www.fernsehserien.de/'+title+'/sendetermine/'+senderlink+'/-1').read()
            
            if not(os.path.isdir(self.name)):
                os.mkdir(self.name)

            if not(os.path.isdir(Fernsehserien_de_Scraper.CACHE_FOLDER)):
                os.mkdir(Fernsehserien_de_Scraper.CACHE_FOLDER)
                
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