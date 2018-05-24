#!/usr/bin/env python

## saves top x google image search results to current directory
#
# This app connects with the API from goole image search and automatically saves images according to search criteria.
# Inputs: - keywords, must be specified in quotation marks, ex: "barrack+obama+president+washington+politics+leader"
#	  - number of images, must be specified as a scalar, ex: 100	
# Output: images in requested format are saved under the directory where app is launched from.
#
# Syntax example to launch app from command line: 
# pyhton imgSearch.py  "goldfish+animal+fish+pet" 100 ".jpg" "xlarge" "photo"
#
# The more keywords are specified, the broader the search and the more images may be found.
# If search is too narrow, app may crash.
# 
# app developed by F. Roux, University of Birmingham, 2017
#
# For more details about search options consult
# https://developers.google.com/custom-search/json-api/v1/reference/cse/list
# https://developers.google.com/custom-search/json-api/v1/using_rest

import os
import sys
import re
import shutil
import json
import requests
import time

os.environ['SERVER_KEY']='AIzaSyCaPYqnvr_rfgtXEu4VtfHkAJ7F7kYUSf0' 
os.environ['CUSTOM_SEARCH_ID']='013941156354834928564:tezifyye-9m'

#print os.environ['SERVER_KEY']
#print os.environ['CUSTOM_SEARCH_ID']

#url='https://www.googleapis.com/customsearch/v1?key=SERVER_KEY&cx=CUSTOM_SEARCH_ID&q=flower&searchType=image&fileType=jpg&imgSize=xlarge&alt=json'
#url = 'https://www.googleapis.com/customsearch/v1?&num=10&start=11&key={}&cx={}&searchType=image&q={}&searchType=image&fileType=jpg&imgSize=xlarge&alt=json'
url = 'https://www.googleapis.com/customsearch/v1?&num=10&start={}&key={}&cx={}&searchType=image&q={}&searchType=image&fileType={}&imgSize={}&imgType=photo&alt=json'

apiKey = os.environ['SERVER_KEY']
cx = os.environ['CUSTOM_SEARCH_ID']

q = sys.argv[1] 	# key words
n = int(sys.argv[2])	#number of requested images, ex 10, 100, 1000 etc
ftp = sys.argv[3]	# file type, ex ".jpg", ".gif", ".png", .etc
isz = sys.argv[4]	# image size, ex "xlarge", "xxlarge", "small", "medium", "large", "icon", "huge"
imt = sys.argv[5] 	# image type, ex "clipart","face","lineart","news","photo"

#print q #keywords
#print n # number of images

k = 1
c = 1
nr = 0
for c in range(n):
  i = 1
  #print k
  time.sleep(0.01)
  for result in requests.get(url.format(k,apiKey, cx, q,ftp,isz)).json()['items']:
    link = result['link']
    image = requests.get(link, stream=True)
    if image.status_code == 200:
      m = re.search(r'[^\.]+$', link)
      nr=k+i
      filename = './{}-{}.{}'.format(q, nr, m.group())
      with open(filename, 'wb') as f:
        image.raw.decode_content = True
        shutil.copyfileobj(image.raw, f)
      i += 1
  c+=1
  k+=i
