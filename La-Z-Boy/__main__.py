import sys
import re
import urllib2
from bs4 import BeautifulSoup
from mechanize import Browser
from tabulate import tabulate
import fpdf

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


def search_channel(channel):
    channel_url = web_url + channel + ".html"
    soup = getBSoup(channel_url)
    time = []
    ratings = []
    title_search = re.compile('/title/tt\d+')

    movie_name = soup.find_all('p', {"class": "title2"})
    for i in range(0, len(movie_name)):
        movie_name[i] = movie_name[i].text

    time1 = soup.find_all('div', {"class": "col-lg-12"})
    for i in range(1, len(time1)-1, 2):
        time.append(time1[i].text[0:13].strip(''))

    # time = filter(None, time)
    time = [x for x in time if x != '']

    for i in range(0, len(movie_name)):
        try :
            movie_search = '+'.join(movie_name[i].split())
            movie_url = base_url + movie_search + '&s=all'
            br = Browser()
            br.open(movie_url)
            link = br.find_link(url_regex=re.compile(r'/title/tt.*'))
            res = br.follow_link(link)

            soup = BeautifulSoup(res.read(), "lxml")
            movie_title = soup.find('title').contents[0]
            rate = soup.find('span', itemprop='ratingValue')
            if rate is not None:
                ratings.append(str(rate.contents[0]))
            else:
                ratings.append("-")
        except :
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
    channel = raw_input("Enter name of the TV Channel: ")
    channel = "-".join([item.strip() for item in channel.split(" ")])
    movie_rating = search_channel(channel)

if __name__ == '__main__':
    main()
