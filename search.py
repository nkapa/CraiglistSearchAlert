import bs4 
import requests
import smtplib
import sys

if(len(sys.argv) <= 1):
	raise Exception("No search provided")

# generate url
baseUrl = 'https://sandiego.craigslist.org/search/cta?query='
args = sys.argv[1:]
for word in args:
	baseUrl += word
	if(args.index(word) < len(args) - 1):
		baseUrl += '+'
print(baseUrl)
