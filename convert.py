import pandas as pd
import json
import time
import os

#take it by peeking into a request after login to prod
SESSION_COOKIE = 'eyJpZCI6IjIyNj . . . nIjp0cnVlfQ==; _ga=GA1.1.72899393.1697115589; _ga_KTGLXV8B2H=GS1.1.1700164054.7.0.1700164336.0.0.0; csrftoken=dTdhGah43kXZ26FoAQX9V7tc53hKHfvdzUed3tsFWmlMO8SpYqBUlbhu78H3o7Me; sessionid=t70ejgyb97x0ridmmdnbxihv9i4n12gk; _hjIncludedInSessionSample_2798930=0; _hjSession_2798930=eyJpZCI6ImYzYTEwNDM0LWRkNTgtNGRjZi1hMDg4LTMwODc1MGM2YWJlZSIsImNyZWF0ZWQiOjE3MDEyODc1NDE3MzUsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6ZmFsc2V9; _hjAbsoluteSessionInProgress=1; _ga_SP6YTCCCW3=GS1.1.1701287541.38.1.1701287623.0.0.0'
PAGE_START = 1
PAGE_END = 19

REQUEST = (
    'curl \'https://backend.app.vestlane.com/api/subscription/?format=json&page=<PAGE_NUMBER>\' '
    '-H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" '
    '-H "Accept-Language: en-GB,en-US;q=0.9,en;q=0.8" '
    '-H "Connection: keep-alive" '
    '-H "Cookie: <SESSION_COOKIE>"'
    '--compressed'
)



def flatten_json(json_obj, separator='_', parent_key=''):
    items = {}
    for key, value in json_obj.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_json(value, separator, new_key))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, (dict, list)):
                    array_key = f"{new_key}{separator}{i}"
                    items.update(flatten_json({str(i): item}, separator, array_key))
                else:
                    array_key = f"{new_key}{separator}{i}"
                    items[array_key] = item
        else:
            items[new_key] = value
    return items

all_subscriptions=[]

all_flattened_subscriptions = []
for page_number in range(1, PAGE_END + 1):
    response = os.popen(REQUEST.replace('<SESSION_COOKIE>', SESSION_COOKIE).replace('<PAGE_NUMBER>', str(page_number))).read()
    subscriptions = json.loads(response).get('results')
    if not subscriptions:
        continue

    all_subscriptions.extend(subscriptions)

    for subscription in subscriptions:
        all_flattened_subscriptions.append(flatten_json(subscription))
    time.sleep(5)

with open('./output.json', 'w') as json_file:
    json.dump(all_subscriptions, json_file)

print(f"Number of JSON objects: {len(all_subscriptions)}")

df = pd.DataFrame(all_flattened_subscriptions)
df.to_excel('./output.xlsx', index=False)