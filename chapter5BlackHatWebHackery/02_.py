import urllib2
url="https://www.nostarch.com"
headers={'User-Agent':"Googlebot"}
request=urllib2.Request(url,headers=headers)
response=urllib2.urlopen(request)
print(response.read())
response.close()


