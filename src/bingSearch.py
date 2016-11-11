# coding=utf-8
'''
Created on Nov 7, 2016

@author: yiting
'''
from bs4 import BeautifulSoup
import csv
import urllib
import requests, httplib, base64, json
from requests.auth import HTTPBasicAuth
import pprint

# Bing API key
API_KEY = "dWQ7MD1EDESHauQ8bMHT43KBrh/4lR+Uz84EpjmLezU"
API_COG_KEY = "be059325b7ec447598b5750223f2df0a"


"""
	new API
	count: max is 50; could use offset to retrieve more
"""
class Bing_search_cog_API:
	def __init__(self, query, source_type = "Web", count = 50):
		self.result = ""
		self.success = False
		user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36"

		headers = {
			# Request headers
			'User-Agent': user_agent,
			'Ocp-Apim-Subscription-Key': API_COG_KEY
		}
		params = urllib.urlencode({
			# Request parameters
			'q': query,
			'count': count,
			'mkt': 'en-us',
			'responseFilter': "Webpages"
		})

		try:
			conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
			conn.request("GET", "/bing/v5.0/search?%s" % params, "{body}", headers)
			response = conn.getresponse()
			data = response.read()
			data = json.loads(data)
			# pp = pprint.PrettyPrinter(indent=4)
			# pp.pprint(data)
			conn.close()
			self.result = data
			self.success = True
		except Exception as e:
			print("[Errno {0}] {1}".format(e.errno, e.strerror))


	def getWebpagesURLs(self):
		if self.success == True:
			urlList = []
			webpages = self.result["webPages"]["value"]
			for webpage in webpages:
				urlList.append(webpage["url"])
			return urlList
		else:
			return None


"""
	old API, still working
"""
def bing_search_api(query, source_type = "Web", top = 10, format = 'json'):
	"""Returns the decoded json response content
 
	:param query: query for search
	:param source_type: type for seacrh result
	:param top: number of search result
	:param format: format of search result
	"""
	# set search url
	query = '%27' + urllib.quote(query) + '%27'
	# web result only base url
	base_url = 'https://api.datamarket.azure.com/Bing/SearchWeb/' + source_type
	url = base_url + '?Query=' + query + '&$top=' + str(top) + '&$format=' + format
 
	# create credential for authentication
	user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"
	# create auth object
	auth = HTTPBasicAuth(API_KEY, API_KEY)
	# set headers
	headers = {'User-Agent': user_agent}
 
	# get response from search url
	response_data = requests.get(url, headers=headers, auth = auth)
	# decode json response content
	json_result = response_data.json()
 
	return json_result 





if __name__ == '__main__':
	# bingQuery = Bing_search_cog_API("Benzene")
	# urlList = bingQuery.getWebpagesURLs()
	# print urlList
	pass
