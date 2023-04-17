import urllib, json, os, datetime
from unidecode import unidecode
import unicodecsv as csv
import urllib.request
from csv import writer
import json

boardLetter = 'v'

# Get the 4chan board catalog JSON file and open it
url = "https://a.4cdn.org/" + boardLetter + "/catalog.json"

with urllib.request.urlopen(url) as response:
    threadCatalog = json.loads(response.read())

data = []
with open("4chan.json", "w") as outfile:
    for p in range(5):
        page = threadCatalog[p]['threads']
        for i in range(20):
            if 'sub' in page[i]:
                subjectText = page[i]['sub']
            else:
                subjectText = ""
            if 'com' in page[i]:
                commentText = page[i]['com']
            else:
                commentText = ""
            thread = commentText

            url = "https://a.4cdn.org/" + boardLetter + "/thread/" + str(page[i]['no']) + ".json"
            with urllib.request.urlopen(url) as response:
                individualThread = json.loads(response.read())

            comments = []
            for j, post in enumerate(individualThread['posts']):
                if 'sub' in individualThread['posts'][j]:
                    subjectText = individualThread['posts'][j]['sub']
                else:
                    subjectText = "No Subject Text Provided"
                if 'com' in individualThread['posts'][j]:
                    commentText = individualThread['posts'][j]['com']
                else:
                    commentText = "No Comment Text Provided"
                comments.append(commentText)

            data.append({'thread': thread, 'comments': comments})
    print(json.dump(data, outfile, indent=4))
