import json
import time

from perspective import PerspectiveAPI
from googleapiclient import discovery
import json
import numpy as np
from random import sample
import treetaggerwrapper as tt
import requests

tagger = tt.TreeTagger(TAGLANG='en', TAGDIR='TreeTagger')
import pandas as pd

ADJECTIVE = ['AJ0', 'AJC', 'AJS']
ADVERB = ['AV0', 'AVP', 'AVQ']
ARTICLE = ['AT0']
CONJUNCTION = ['CJC', 'CJS', 'CJT']
INTERJECTION = ['ITJ']
NOUN = ['NN0', 'NN1', 'NN2', 'NP0']
NUMERAL = ['CRD', 'ORD']
PRONOUN = ['PNI', 'PNP', 'PNQ', 'PNX', 'POS',]
PREPOSITION = ['PRF', 'PRP']
PUNCTUATION = ['PUL', 'PUN', 'PUQ', 'PUR']
UNCLASSIFIED = ['UNC']
VERB = ['VBD', 'VHD', 'VVD', 'VDD', 'VM0', 'VBI', 'VHI', 'VDI', 'VVG', 'VVI', 'VBG', 'VDG', 'VHG', 'VBN', 'VDN', 'VHN', 'VVN']
PRESENT = ['VBB', 'VBZ', 'VHB', 'VHZ', 'VVB', 'VDB', 'VVZ', 'VDZ']
PAST = ['VBD', 'VHD', 'VVD', 'VDD']
FUTURE = ['VM0']

p = PerspectiveAPI("AIzaSyDXURFrLd6Zh94csGMhWWzuupl_EHqYkso")

def get_tags(text):
    tags = tagger.tag_text(text)
    tags = [tag.split('\t') for tag in tags]
    copy = tags.copy()
    for tag in copy:
        if not len(tag) == 3:
            tags.remove(tag)
    return tags

def get_comments(comments):
    comment = ''
    try:
        comments_sample = sample(comments, 100)
    except:
        comments_sample = comments
    for comm in comments_sample:
        comment = comment + str(comm)
    return comment


def we_count(text):
    tags = get_tags(text)
    if tags == []:
        return 0
    we_count = sum(1 for tag in tags if tag[1] in ['PNP', 'DPS', 'PNX'] and tag[2] in ['we', 'ours', 'ourselves', 'ourself'])
    total = len(tags)
    return we_count/total

def f_score(text):
    tags = get_tags(text)
    if tags == []:
        return 0
    noun_count = sum(1 for tag in tags if tag[1] in NOUN)
    adjective_count = sum(1 for tag in tags if tag[1] in ADJECTIVE)
    preposition_count = sum(1 for tag in tags if tag[1] in PREPOSITION)
    article_count= sum(1 for tag in tags if tag[1] in ARTICLE)
    pronoun_count = sum(1 for tag in tags if tag[1] in PRONOUN)
    verb_count = sum(1 for tag in tags if tag[1] in VERB)
    adverb_count = sum(1 for tag in tags if tag[1] in ADVERB)
    interjection_count = sum(1 for tag in tags if tag[1] in INTERJECTION)
    total = len(tags)
    F = (noun_count+adjective_count+preposition_count+article_count-pronoun_count-verb_count-adverb_count-interjection_count)/total
    return F

def verb_tens(text):
    tags = get_tags(text)
    past_count = sum(1 for tag in tags if tag[1] in PAST)
    present_count = sum(1 for tag in tags if tag[1] in PRESENT)
    future_count = sum(1 for tag in tags if tag[1] in FUTURE and tag[2] in ['will', 'shall'])
    total = max(past_count+present_count+future_count, 1)
    print(tags)
    return (past_count+future_count)/total

def toxicity(text):
    result = p.score(text, ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT', 'INFLAMMATORY'])
    return list(result.values())

text = '''I had been dancing'''
print(verb_tens(text))
data = []

'''for f, file in enumerate(['4chan_cleaned.json']):#,'twitch.json', '4chan.json','tumblr.json', 'reddit.json', '4chan_cleaned.json'
    print(file)
    with open(file) as json_file:
        posts = json.load(json_file)
        for k, post in enumerate(posts):
            print(k)
            comments = post.get('comments')
            thread = post.get('thread')
            comments.append(thread)
            comment = get_comments(comments)
            print('computing ' + str(len(comment)))
            while True:
                try:
                    values=toxicity(comment)
                    break
                except Exception as e:
                    print(e)
                    print('waiting...')
                    comment = get_comments(comments)
                    time.sleep(1)
            #values= np.insert(values,0,f)
            data.append(values)

data = pd.DataFrame(data, columns=['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT', 'INFLAMMATORY'])
data.to_csv('out2.csv',index=False)'''







'''try:
  blog = post.get('trail')[0].get('blog').get('name')
except:
  blog = 'decorum-video-games'
print(blog)
try:
  id = post.get('trail')[0].get('post').get('id')
except:
  id = post.get('id_string')
notes.append(client.notes(blog, id=id,mode='conversation'))
with open("comments.json", "w") as outfile:
json.dump(notes, outfile, indent=4)'''