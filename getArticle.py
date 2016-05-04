import urllib
import json

def getText(pageTitle):
	wikiResponse = urllib.urlopen("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles="+pageTitle)
	wikiData = json.load(wikiResponse)
	wikiText = wikiData['query']['pages'].values()[0]['extract']
	wikiText = removeNonAscii(wikiText)
	return wikiText

def removeNonAscii(s):
	return "".join(i for i in s if ord(i)<128)

if __name__ == '__main__':
  pageTitle = "Barack Obama"
  print getText(pageTitle)