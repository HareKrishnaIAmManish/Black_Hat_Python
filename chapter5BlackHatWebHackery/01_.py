import urllib2
url='https://www.google.com'
response=urllib2.urlopen(url)#GET
print(response.read())
response.close()
