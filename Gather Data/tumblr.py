import pytumblr
import json

client = pytumblr.TumblrRestClient(
  'LvExrjPbytfSFurnuBOkZOUKtnXy3hQLa2f6BJxbPZmUXKW0AP',
  'zDAVR2q2J6QFuuhWSmgpVvlT3vrdkUsOqBEaPcIqYxCUyUItu7',
  'F3socjVeLCwEBS5NeCw6zKd0yHNkyTtzt2eoWwKkrs482rV5cd',
  '7CwEefhr7VRdUEH58eN4Aqjnkl1oFuJ8FJbMYEhIXEc9W9z5dm'
)

def getPosts(limit = 370):
  games = client.posts('decorum-video-games')
  posts = games.get('posts')
  while posts.__len__()<limit:
    timestamp = posts[-1].get('timestamp')
    print(posts.__len__())
    games = client.posts('decorum-video-games', before=timestamp,limit=20)
    posts.extend(games.get('posts'))
  with open("threads.json", "w") as outfile:
    json.dump(posts, outfile, indent=4)

def getNotes():
  with open('threads.json') as json_file:
    posts = json.load(json_file)
  notes = []
  for p, post in enumerate(posts):
    print(p)
    try:
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
    json.dump(notes, outfile, indent=4)

#getPosts()
#getNotes()

with open('threads.json') as json_file:
  threads = json.load(json_file)

with open('comments.json') as json_file:
  notes = json.load(json_file)

data = []
fails = 0
success = 0
for i in range(370):
  try:
    thread = threads[i].get('trail')[0].get('content_raw')
  except:
    thread = 'Image'
  comments = []
  for note in notes[i].get('notes'):
    if note.get("added_text") is not None:
      comments.append(note.get("added_text"))
    elif note.get("reply_text") is not None:
      comments.append(note.get("reply_text"))
  post = {'thread': thread, 'comments': comments}
  if len(comments)  < 4 or post in data:
    fails = fails+1
  else:
    success = success +1
    data.append({'thread': thread, 'comments': comments})

with open("tumblr.json", "w") as outfile:
  json.dump(data, outfile, indent=4)
print(success)


