from io import BytesIO
from lxml import etree
import requests
url="https://nostarch.com"
r=requests.get(url)#get
content=r.content #content is of type bytes
parser=etree.HTMLParser()
print('-'*30)
print(content)
print('-'*30)
print(BytesIO(content))
print('-'*30)
content=etree.parse(BytesIO(content),parser=parser)#parses into tree
print(content)
print('-'*30)
for link in content.findall('//a'): #find all "a" anchor elements
    print(f"{link.get('href')} -> {link.text}")
