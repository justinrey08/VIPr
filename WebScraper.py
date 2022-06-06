#!/usr/bin/env python
# coding: utf-8

# In[3]:


from urllib.request import urlopen
from urllib.request import urlretrieve
import bs4 as bs
import os


# In[2]:


searchString = input("Enter Search String: ")
folderName = '_'.join(searchString.split(" "))
currPath = os.path.dirname(os.path.realpath(__file__))
reqPath = os.path.join(currPath,folderName)
if os.path.isdir(reqPath) == False:
	os.mkdir(folderName)


# In[5]:


searchQuery = '+'.join(searchString.split(" "))
myLink = "https://imgur.com/search/score?q="+searchQuery


# In[6]:


source = urlopen(myLink,timeout=10).read()
soup = bs.BeautifulSoup(source, "html.parser")


# In[7]:


def alterSrc(s):
	l = len(s)
	for i in range(0,l):
		if s[i] == 'b' and s[i+1] == '.':
			return s[0:i]+s[i+1:]


# In[8]:


atags = soup.findAll("a",{"class":"image-list-link"})
imgtags = [a.find("img") for a in atags]
srcs = ["https:"+alterSrc(img['src']) for img in imgtags]


# In[9]:


print("Downloading...")
for l in srcs:
	filename = os.path.join(reqPath,os.path.basename(l))
	urlretrieve(l,filename)
print("Successful!")


# In[ ]:




