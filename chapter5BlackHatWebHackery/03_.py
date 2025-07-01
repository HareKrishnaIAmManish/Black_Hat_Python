# import urllib.parse
# import urllib.request
# url="https://nostarch.com"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
# }
# req = urllib.request.Request(url, headers=headers)
# with urllib.request.urlopen(req) as response:#get 
#     content=response.read()
#     print(content)
import urllib.request
import urllib.parse
url="https://boodely.com/category/web/"
with urllib.request.urlopen(url) as response:#get 
     content=response.read()
     print(content)
