import urllib
import hashlib
import json

def getImageLink(pageTitle):
	wikiResponse = urllib.urlopen("https://en.wikipedia.org/w/api.php?action=query&titles=" + pageTitle + "&prop=pageimages&format=json&pithumbsize=300")
	wikiData = json.load(wikiResponse)
	imageLink = wikiData['query']['pages'].values()[0]['thumbnail']['source']
	return imageLink


def downloadImage(imageLink):
	urllib.urlretrieve(imageLink, "test.jpg")

# if only image name is known, calculate image host folder
# imageName = "PM_Modi_Portrait(cropped).jpg"
# imageLink = getImageLink(imageName)
# urllib2.urlretrieve(imageLink, "test.jpg")

# def getImageLink(imageName):
# 	hashedString = hashlib.md5(imageName).hexdigest()
# 	folder =  hashedString[0:1] + "/" + hashedString[0:2] + "/"
# 	imageLink = "https://upload.wikimedia.org/wikipedia/commons/" + folder + imageName
# 	print imageLink
# 	return imageLink

if __name__ == '__main__':
	pageTitle = "David Beckham"
	downloadImage(getImageLink(pageTitle))