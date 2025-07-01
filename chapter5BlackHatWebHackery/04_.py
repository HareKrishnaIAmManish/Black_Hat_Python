import urllib.request
import urllib.parse
url="https://boodely.com/category/web/"
#url="https://httpbin.org/post"
with urllib.request.urlopen(url) as response:#get 
     content=response.read()
     print(content)
