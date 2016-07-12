import sys
import re
import urllib2
from bs4 import BeautifulSoup
from mechanize import Browser

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

def getBSoup(url):
	req = urllib2.urlopen(url)
	soup = BeautifulSoup(req.read(),"lxml")
	return soup

def search_channel(channel):
	channel_url = web_url + channel + ".html"
	soup = getBSoup(channel_url);
	time = []
	ratings = []
	title_search = re.compile('/title/tt\d+')

	movie_name = soup.find_all('p',{"class":"title2"})
	for i in range(0,len(movie_name)):
		movie_name[i] = movie_name[i].text

	time1 = soup.find_all('div',{"class":"col-lg-12"})
	for i in range(1,len(time1)-1,2):
		time.append(time1[i].text[0:13].strip(''))

	#time = filter(None, time)
	time = [x for x in time if x != '']

	for i in range(0,len(movie_name)):
		movie_search = '+'.join(movie_name[i].split())
		movie_url = base_url + movie_search + '&s=all'
		br = Browser()
		br.open(movie_url)
		link = br.find_link(url_regex = re.compile(r'/title/tt.*'))
		res = br.follow_link(link)
		
		soup = BeautifulSoup(res.read(),"lxml")	 
		movie_title = soup.find('title').contents[0]
		rate = soup.find('span',itemprop='ratingValue')
		if rate!=None:
			ratings.append(str(rate.contents[0]))
		else:
			ratings.append("-")

 	for i in range(0,len(movie_name)):
 		str1 = "Movie: " + str(movie_name[i]) + "  Time: " + str(time[i])+ "  Rating: " + ratings[i]
		print(str1)

def main():
	if(len(sys.argv)>2):
		channel = str(sys.argv[1] + "-" + sys.argv[2])
	else:
		channel = str(sys.argv[1])
	movie_rating = search_channel(channel)

if __name__ == '__main__':
	main()


