# -*- coding: utf-8 -*-
import sys
import re
import urllib2
from bs4 import BeautifulSoup
from mechanize import Browser
from tabulate import tabulate
import fpdf
import string

'''
   Currently supports:  #star-movies
            #sony-max
            #movies-now
            #romedy-now
            #movies-ok
            #sony-pix
            #hbo
            #filmy
            #star-gold
'''

web_url = "http://tvinfo.in/"
web_url2= "http://tvscheduleindia.com/channel/"
base_url = 'http://www.imdb.com/find?q='

#Method to initialize pdf object
def pdf_save(data_movies,headers):
    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Tv Timings !",ln=1, align="C")
    #pdf.cell(200, 10, str(tabulate(data_movies,headers)),0,1, align="l")
    for data in data_movies:
        str1 = "Movie: " + str(data[0]) + "  Time: " + str(data[1])+ "  Rating: " + str(data[2])
        pdf.cell(200, 10, str1,0,1, align="l")
    pdf.output('La-Z-Boy.pdf')

def getBSoup(url):
    print'''
Processing...

    '''
    req = urllib2.urlopen(url)
    soup = BeautifulSoup(req.read(), "lxml")
    return soup

#def search_channel(channel,channel2):
def search_channel(channel2):
    #channel_url = web_url + channel + ".html"
    #soup = getBSoup(channel_url)
    time = []
    ratings = []
    title_search = re.compile('/title/tt\d+')

    #movie_name = soup.find_all('p', {"class": "title2"})

    channel2_url= web_url2 + channel2
    soup2 = getBSoup(channel2_url)

    for s in soup2.find_all("strong"):
        if s.string:
            s.string.replace_with(s.string.strip())
    movie_name=[]
    movie_name2 = soup2.find_all("strong")

    for i in range(0,len(movie_name2)):
        movie_name2[i]=movie_name2[i].text

    #for i in range(0, len(movie_name)):
    #    movie_name[i] = movie_name[i].text

    #print movie_name

    #time1 = soup.find_all('div', {"class": "col-lg-12"})

    for s in soup2.find_all('b',{"class":"from"}):
        if s.string:
            s.string.replace_with(s.string.strip())

    for s in soup2.find_all('b',{"class":"to"}):
        if s.string:
            s.string.replace_with(s.string.strip())

    time2_from = soup2.find_all('b',{"class":"from"})
    time2_to = soup2.find_all('b',{"class":"to"})
    
    for i in range(0,len(time2_from)):
        time2_from[i]=time2_from[i].text

    for i in range(0,len(time2_to)):
        time2_to[i]=time2_to[i].text

    checkList=[]                                                # soup2 has the code for page1. Not all the movies on page one are shown today!
    for table_row in soup2.find_all('tr'):
        # table_row=BeautifulSoup(table_row)
        day = table_row.find_all('span', {'class': 'date'})
        if (len(day) > 0):
            day = str(day[0].string).replace(" ", "")
            day = day.replace("\n", "")                         # If day = Today then only we should print the movie.
            if (day == "Today"):
                checkList.append(True)
            else:
                checkList.append(False)

    #print(movie_name2)
    #print(time2_from)
    #print (time2_to)
    #print(checkList)


    #for i in range(1, len(time1)-1, 2):
    #    time.append(time1[i].text[0:13].strip(''))

    #time = [x for x in time if x != '']

    for i in range(0,len(movie_name2)):
        if(checkList[i]):
            movie_name.append(movie_name2[i])
            movie_name[i]=movie_name[i].encode('utf-8')
            movie_name[i]=movie_name[i].encode('ascii','ignore').strip()
            time.append(time2_from[i]+"-"+time2_to[i])

    #print movie_name

    # time = filter(None, time)

    for i in range(0, len(movie_name)):
        try:
            print "Checking IMDb rating of "+ movie_name[i]
            movie_search = '+'.join(movie_name[i].split())
            movie_url = base_url + movie_search + '&s=all'
            #print movie_url
            br = Browser()
            #print "check1"
            br.open(movie_url)
            #print "check2"
            link = br.find_link(url_regex=re.compile(r'/title/tt.*'))
            res = br.follow_link(link)
            #print "check3"
            soup = BeautifulSoup(res.read(), "lxml")
            #print "check4"
            movie_title = soup.find('title').contents[0]
            #print "check5"
            rate = soup.find('span', itemprop='ratingValue')
            if rate is not None:
                ratings.append(str(rate.contents[0]))
            else:
                ratings.append("-")
        except:
            ratings.append("-")
    headers = ['Movies', 'Time', 'Rating']
    data_movies = []
    for i in range(0, len(movie_name)):
        data_movies.append([str(movie_name[i]), str(time[i]), ratings[i]])
    print tabulate(data_movies, headers=headers)

    #Saving to pdf
    print("\nWant to save as pdf? Y/N")
    choice = raw_input().lower()
    if choice == 'y':
        pdf_save(data_movies,headers)
        print('\nSaved!')
    else:
        print('\nBye!')

def main():

    print'''
                                                                        Welcome to La-Z-Boy
                                                                    For the love of good content
    '''
    #channel = raw_input("Enter name of the TV Channel: ")
    channel2 = raw_input("Enter name of the TV Channel: ")
    #channel = "-".join([item.strip() for item in channel.split(" ")])
    if(len(channel2.split())>1):
        channel2 = "-".join([item.strip() for item in channel2.split(" ")])
        channel2 = channel2.title()
    else:
        channel2 = channel2.strip()
        channel2 = channel2.upper()
    movie_rating = search_channel(channel2)

if __name__ == '__main__':
    main()
