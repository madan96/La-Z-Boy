# -*- coding: utf-8 -*-
import sys
import re
import urllib2
from bs4 import BeautifulSoup
from mechanize import Browser
from tabulate import tabulate
import fpdf
import string
from itertools import islice

web_url = "http://tvinfo.in/"
web_url2= "http://tvscheduleindia.com/channel/"
web_url3="http://tvscheduleindia.com"
base_url = 'http://www.imdb.com/find?q='
imdb_url = "https://www.imdb.com"

def getBSoup(url):
    print'''
Processing...

    '''
    req = urllib2.urlopen(url)
    soup = BeautifulSoup(req.read(), "lxml")
    return soup

def pdf_save(data_movies,headers):
    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Tv Timings !",ln=1, align="C")
    for data in data_movies:
        str1 = "Movie: " + str(data[0]) + "  Time: " + str(data[1])+ "  Rating: " + str(data[2])
        pdf.cell(200, 10, str1,0,1, align="l")
    pdf.output('La-Z-Boy.pdf')

class MovieEntry:
    '''
    Class for storing movie entries and utility functions
    '''
    def __init__(self):
        self.movie_names = []
        self.time = []
        self.ratings = []

    def search_channel(self, channel):
        title_search = re.compile('/title/tt\d+')

        channel_url = web_url2 + channel
        soup = getBSoup(channel_url)

        self.movie_names = [str(b.string) for b in soup.findAll('b')]

        time_from = []
        time_to = []
        table = soup.find('table', id="example")
        td_tags = soup.findAll('td')
        for td in td_tags:
            if td.get('id') is not None:
                if 'starttime' in td.get('id'):
                    time_from.append(str(td.text))
                if 'endtime' in td.get('id'):
                    time_to.append(str(td.text))

        for i in range(0, len(self.movie_names)):
            self.time.append(time_from[i] + "-" + time_to[i])

    def get_rating(self):
        for i in range(0, len(self.movie_names)):
            try:
                print "Checking IMDb rating of " + self.movie_names[i]
                movie_search = '+'.join(self.movie_names[i].split())
                movie_url = base_url + movie_search + '&s=all' 
                br = Browser()
                br.set_handle_robots(False)
                response = br.open(movie_url)
                links = br.links()
                link_list = []
                for link in links:
                    link_list.append(str(link.url))
                r = re.compile(r'/title/tt.*')
                links = list(filter(r.match, link_list))
                link = imdb_url + links[2]
                req = urllib2.urlopen(link)
                soup = BeautifulSoup(req.read(), "lxml")
                movie_title = soup.find('title').contents[0]
                rate = soup.find('span', itemprop='ratingValue')

                if rate is not None:
                    self.ratings.append(str(rate.contents[0]))
                else:
                    self.ratings.append("-")
            except:
                self.ratings.append("-")
    
    def display(self):
        headers = ['Movies', 'Time', 'Rating']
        data_movies = []
        for i in range(0, len(self.movie_names)):
            data_movies.append([str(self.movie_names[i]), str(self.time[i]), self.ratings[i]])
        print ('\n')
        print tabulate(data_movies, headers=headers)

        # Saving to pdf
        print("\nWant to save as pdf? Y/N")
        choice = raw_input().lower()
        if choice == 'y':
            pdf_save(data_movies, headers)
            print('\nSaved!')
        else:
            print('\nBye!')

def main():

    head = "\n\n   Welcome to La-Z-Boy\nFor the love of good content\n\n"
    print (head)

    movie_entries = MovieEntry()

    channel = raw_input("Enter name of the TV Channel: ")
    channel = channel.lower()
    if(len(channel.split())>1):
        channel = "-".join([item.strip() for item in channel.split(" ")])
    else:
        channel = channel.strip()
    movie_entries.search_channel(channel)
    movie_entries.get_rating()
    movie_entries.display()

if __name__ == '__main__':
    main()
