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
web_url3="http://tvscheduleindia.com"
base_url = 'http://www.imdb.com/find?q='


class Movie_entry:
    movie_name =''
    movie_start=''
    movie_end=''
    movie_rating=0

    def get_rating(self ):
        try:
            print "Checking IMDb rating of "+ self.movie_name
            movie_search = '+'.join(self.movie_name.split())
            movie_url = base_url + movie_search + '&s=all'
            print(movie_url)
            br = Browser()
            br.open(movie_url)
            link = br.find_link(url_regex=re.compile(r'/title/tt.*'))
            res = br.follow_link(link)
            soup = BeautifulSoup(res.read(), "lxml")
            movie_title = soup.find('title').contents[0]
            rate = soup.find('span', itemprop='ratingValue')
            if rate is not None:
                self.movie_rating=rate

        except:
            self.movie_rating='-'

movies_of_my_genre=[]



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

def getBSoup2(url):
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

def genre_recommend(genre):
    genre=genre.lower()
    soup3=getBSoup(web_url3)
    soup4=soup3.find('div',{'class' : 'massn' })
    for row in islice(soup4.findAll('a'),50):                          # This decides how many channels to see (here 50) .set 10 for quick response
        #print row.find('span').text
        #print ('Searching in  :'+web_url3 + row.get('href'))
        print 'Searching in  :' + row.find('span').text.replace('\n','')
        soup5=getBSoup2(web_url3 + row.get('href'))
        soup5=soup5.find('div',{'class': 'resultCont'})
        soup5 = soup5.findAll('tr')
        soup5=soup5[:-1]
        for link in soup5:                                           # link contains code of <tr>
            if(link.find('b',{'class':'genre'})):
                mov_gen=link.find('b',{'class':'genre'}).string.lower()
                mov_gen = re.sub('[' + string.punctuation + ']', ' ', mov_gen)
                mov_gen=mov_gen.split( )
                if genre in mov_gen:
                    date=link.find('span',{'class':'date'}).string.replace(" ", "").replace("\n", "")
                    if (date == "Today"):
                        new_movie=Movie_entry()
                        new_movie.movie_name=link.find('strong').string.replace("\n", "")
                        #print new_movie.movie_name
                        new_movie.movie_start=link.find('b',{'class':'from'}).string
                        new_movie.movie_end=link.find('b',{'class':'to'}).string
                        movies_of_my_genre.append(new_movie)

def get_ratings(movies_of_my_genre):
    for movie in movies_of_my_genre:
        try:
            print "Checking IMDb rating of :   " + movie.movie_name.replace('\t','')
            movie_search = '+'.join(movie.movie_name.split())
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
                movie.movie_rating=float(rate.contents[0])
            else:
                movie.movie_rating=0
        except:
            movie.movie_rating = 0

def main():

    print'''
                                                                        Welcome to La-Z-Boy
                                                                    For the love of good content
    '''
    print("If you want to check mmovies movies on a channel select 1")
    print("To get movies of a specific Genre select 2")
    choice=raw_input("Enter choice: ")

    if(str(choice)=='1'):
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
    else:
        genre = raw_input("Enter Genre: (like  comedy, action ....) ")
        genre_recommend(genre)
        print '\nNumber of movies of genre ' + genre.upper()+' found : ' + str(len(movies_of_my_genre))
        get_ratings(movies_of_my_genre)
        sorted_list = sorted(movies_of_my_genre, key=lambda movie: movie.movie_rating, reverse=True)

        headers = ['Movies', 'Time', 'Rating']
        data_movies2 = []

        for movie in islice(sorted_list, 5):
            data_movies2.append([movie.movie_name.replace('\t', ''), movie.movie_start+"-"+movie.movie_end, movie.movie_rating])
        print tabulate(data_movies2, headers=headers)

'''
        print("\nWant to save as pdf? Y/N")
        choice = raw_input().lower()
        if choice == 'y':
            pdf_save(data_movies2, headers)
            print('Saved!')
'''
if __name__ == '__main__':
    main()
