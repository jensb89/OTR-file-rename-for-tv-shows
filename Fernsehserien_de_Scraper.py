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
import codecs
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


class Fernsehserien_de_Scraper(object):
    # Parse the EpisodeGuide Page from Fernsehserien.de - get back all episodes as a list

    CACHE_FOLDER = '.cache'

    def __init__(self, show):
        self.name = show #e.g. 'Die Simpsons'

    ######  DOWNLOADING WEBPAGE : Fernsehserien - EpisodeGuide ########
    def downloadWebpage(self):
        logging.info('Trying to get website information...please wait...')
        cache = Fernsehserien_de_Scraper.CACHE_FOLDER + '/' + self.name + '_' + 'eplist.dat'
        if os.path.isfile(cache) and (time.time() - os.path.getmtime(cache)) < 43200:
            logging.info('Use local file...')       
            webpage = urlopen(cache)
        else:
            if serieslinks.has_key(self.name):
                title = serieslinks[self.name]
            else:
                title = self.name.replace(' ','-')

            webpage = urlopen('http://www.fernsehserien.de/'+title+'/episodenguide').read()

            if not(os.path.isdir(Fernsehserien_de_Scraper.CACHE_FOLDER)):
                os.mkdir(Fernsehserien_de_Scraper.CACHE_FOLDER)

            logging.info('Website scraping => done')
                
            f = open(cache,'w')
            f.write(webpage)
            f.close()
            
        self.soupobj = BeautifulSoup(webpage, "html.parser")
        #print self.soupobj.prettify()
    

    def getTitlesGerman(self):
        episodetitlesger = self.soupobj.select("td.episodenliste-titel")
        for i in episodetitlesger:
            if type(i.find('span')) is not NoneType:
                i.find('span').decompose()
            
        return [x.text for x in episodetitlesger]
        

    def getTitles(self):
        episodeLine = self.soupobj.select("tr.ep-hover")
        episodetitles = [episodeLine[i].find_all("td")[8].text.replace('.','') for i in range(0,len(episodeLine))]
        return episodetitles
        
        
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
        episodeLine = self.soupobj.select("tr.ep-hover")
        seasonNumbers = [episodeLine[i].find_all("td")[3].text.replace('.','') for i in range(0,len(episodeLine))]
        return seasonNumbers

    def getEpisodeNumber(self):
        episodeLine = self.soupobj.select("tr.ep-hover")
        episodeNumbers = [episodeLine[i].find_all("td")[4].text.replace('.','') for i in range(0,len(episodeLine))]
        return episodeNumbers

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
            for i in range(0,self.getCountEpisode()):
                print 'S' + s[i] + '.' + 'E'+ e[i] + ' : ' + t[i].decode('utf-8') + '( ' + d[i] + ' )'   

        return (d,s,e,t)


    ######  DOWNLOADING WEBPAGE : Fernsehserien - TimeTable ########
    def getTimeTable(self, sender):
        logging.info('Trying to get timetable information...please wait...')
                      
        if senderlinks.has_key(sender):
            senderlink = senderlinks[sender]
        else:
            logging.warning('Link zu Sender ' + sender +' nicht gefunden')
            return 0
        
        cache = Fernsehserien_de_Scraper.CACHE_FOLDER + '/' + self.name + '_ttlist.dat'
        if os.path.isfile(cache) and (time.time() - os.path.getmtime(cache)) < 43200:
            logging.info("Using recent cache file...")        
            webpage = urlopen(cache)
        else:
            if serieslinks.has_key(self.name.replace(' ','-')):
                title = serieslinks[self.name.replace(' ','-')]
            else:
                title = self.name.replace(' ','-')
            logging.info('Loading: http://www.fernsehserien.de/'+title+'/sendetermine/'+senderlink+'/-1')
            webpage = urlopen('http://www.fernsehserien.de/'+title+'/sendetermine/'+senderlink+'/-1').read()
            

            if not(os.path.isdir(Fernsehserien_de_Scraper.CACHE_FOLDER)):
                os.mkdir(Fernsehserien_de_Scraper.CACHE_FOLDER)
                
            f = open(cache,'w')
            f.write(webpage)
            f.close()   

            logging.info('Website scraping => done')
            
        
        #soup = BeautifulSoup(fernsehserien_testdata.gethtmlo(), "html.parser")
        soup = BeautifulSoup(webpage, "html.parser")
        tddata = soup.select("tr")

        epdate, eptime, season, episode, title = [],[],[],[],[]
        
        for index, item in enumerate(tddata):
            m = re.search("(\d{2}\.\d{2}\.\d{4}).*?(\d{2}:\d{2}).*?>(\d{1,3})<.*?>(\d{1,2}).*?>(\d{1,2}).*?>([^<]+)", str(item))
            if type(m) is not NoneType:            
                epdate.append(m.group(1))
                eptime.append(m.group(2))
                season.append(m.group(4))
                episode.append(m.group(5))
                title.append(m.group(6))
        return (epdate, season, episode, title, eptime)    


if __name__ == '__main__':
    #Print episodeguide
    import sys
    if len(sys.argv)>2:
        seriesname = sys.argv[1]
        lang = sys.argv[2] #de / us
        Fernsehserien_de_Scraper(seriesname).getEpisodeGuide(lang = lang, printout = True)