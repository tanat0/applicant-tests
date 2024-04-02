import time
import requests
import pandas as pd

posts = 'http://jsonplaceholder.typicode.com/posts'
comments = 'http://jsonplaceholder.typicode.com/comments'

def parsing(url):
    result = []
    resp = requests.get(url)
    time.sleep(1)

    if resp.status_code == 200:
        json_data = resp.json()
        result += json_data
        #page_count = json_data['page_count']

    df = pd.DataFrame(result)
    return df

df1 = parsing(posts)
df2 = parsing(comments)

avg_comms = {}

for user_id in df1['userId'].unique():
    user_posts = df1['userId'].value_counts()[user_id]
    user_comms = df2.loc[df2['postId'].isin(df1.loc[df1['userId'] == user_id, 'id']), 'postId'].value_counts().sum()

    avg_comm = user_comms / user_posts if user_posts > 0 else 0

    avg_comms[user_id] = avg_comm

print(avg_comms)
