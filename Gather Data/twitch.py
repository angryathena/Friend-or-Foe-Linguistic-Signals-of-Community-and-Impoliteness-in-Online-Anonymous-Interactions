import pandas as pd
import json

import os

# assign directory
directory = 'ICWSM19_data'

data = []

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    df = pd.read_pickle(f)
    print(filename)
    i = 0
    id = ''
    for index, row in df.iterrows():
        if not id == row['video_id']:
            if i>0:
                data.append({'thread': id, 'comments': comments})
            i = i+1
            id = row['video_id']
            comments = []
        if i > 2:
            break
        comments.append(row['body'])

with open("twitch.json", "w") as outfile:
    json.dump(data, outfile, indent=4)