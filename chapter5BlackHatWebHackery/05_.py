import urllib.request
import urllib.parse
url="https://httpbin.org/post"
info={'user':'tim','passwd':'31337'}
data=urllib.parse.urlencode(info).encode() #data is now of type bytes
req=urllib.request.Request(url,data)
with urllib.request.urlopen(req) as response:#get 
     content=response.read()
     print(content)