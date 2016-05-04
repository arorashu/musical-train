import urllib
import hashlib

def getImageLink(imageName):
	hashedString = hashlib.md5(imageName).hexdigest()
	folder =  hashedString[0:1] + "/" + hashedString[0:2] + "/"
	imageLink = "https://upload.wikimedia.org/wikipedia/commons/" + folder + imageName
	print imageLink
	return imageLink

imageName = "PM_Modi_Portrait(cropped).jpg"
imageLink = getImageLink(imageName)
urllib.urlretrieve(imageLink, "test.jpg")