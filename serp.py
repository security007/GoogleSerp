import requests
from bs4 import BeautifulSoup as bs 
from requests.utils import requote_uri
from urllib.parse import urlparse
import argparse

class Rank:
	def __init__(self,domain,keyword):
		self.domain = domain 
		self.keyword = requote_uri(keyword) 
		self.google_url = "https://www.google.com/search?q="
		self.UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
		
	def scrap(self):
		get_source = requests.get(self.google_url+self.keyword,headers={'user-agent':self.UA})
		soup = bs(get_source.text,"lxml")
		find_link = soup.findAll("div",{"class":"yuRUbf"})
		return find_link
		
	def get_url(self,list_source):
		list_url = []
		for url in list_source:
			find_tag_a = url.findAll("a",href=True)
			for ls_url in find_tag_a:
				list_url.append(ls_url['href'])
		
		return list_url

def main():		
	print("""
++++++++++++++++++++++++++++++++++++
+     GOOGLE TOP 10 SERP CHECK     +
+     Alfian Buyung S              +
++++++++++++++++++++++++++++++++++++
	""")
	parser = argparse.ArgumentParser(description='GOOGLE TOP 10 SERP CHECK are parse domain that on top 10 google')
	parser.add_argument("--domain","-D",help="your domain name", required=True)
	parser.add_argument("--keyword","-K",help="your keyword", required=True)
	args = parser.parse_args()

	go = Rank(args.domain,args.keyword)

	rank = 1
	black_list = ["webcache.googleusercontent.com","translate.google.com"]
	my_rank = []
	for top10 in go.get_url(go.scrap()):
		get_domain = urlparse(top10).netloc
		if get_domain not in black_list and top10 != "#":
			print("["+str(rank)+"] "+top10)
			if args.domain in get_domain:
				my_rank.append("Rank ["+str(rank)+"] "+top10)
			rank += 1
	print("\n")
	print("RESULT :")
	if len(my_rank) == 0:
		print("Your page not in Top 10")
	else:
		for x in my_rank:
			print(x)
		print("Keyword : "+args.keyword)
		
if __name__ == "__main__":
	main()