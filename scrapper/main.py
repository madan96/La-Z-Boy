import sys
import re
import requests
from bs4 import BeautifulSoup

web_url = "http://tvinfo.in/"

def search_channel(channel):
	time = []
	channel_url = web_url + channel + ".html"
	r = requests.get(channel_url)
	soup = BeautifulSoup(r.text)
	movie_name = soup.find_all('p',{"class":"title2"})

	time1 = soup.find_all('div',{"class":"col-lg-12"})
	for i in range(1,len(time1)-1,2):
		time.append(time1[i].text[0:13].strip(''))

	#time = filter(None, time)
	time = [x for x in time if x != '']
	for i in range(0,len(movie_name)):
		str1 = "Movie: " + str(movie_name[i]) + "Time: " + str(time[i])
		print(str1)
	
	#print(time1[4].text)
	#for data in time1:
	#print(data)
	#	print("------------------")
	#print(soup.find_all('p',"data-date"))

def main():
	if(len(sys.argv)>2):
		channel = str(sys.argv[1] + "-" + sys.argv[2])
	else:
		channel = str(sys.argv[1])

	movie_rating = search_channel(channel)

if __name__ == '__main__':
	main()

#star-movies
#sony-max
#movies-now
#romedy-now
#movies-ok
#sony-pix
#hbo
#filmy
#star-gold
#
#
