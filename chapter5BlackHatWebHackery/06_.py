import requests
url='https://httpbin.org/get'
response=requests.get(url)#get
print(response.text)
print(response.content)
data={'user':'tim','passwd':'31337'}
url="https://httpbin.org/post"
response=requests.post(url,data=data)#POST
print(response.text) #response.text is string;
print(response.content) #byte string


