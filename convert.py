import pandas as pd
import json
import time
import os

SESSION_COOKIE = 'eyJpZCI6IjIyNjI0MDdiLWExYWUtNTdmOC04YjdlLTVhMmU2ZDhiNjk2MyIsImNyZWF0ZWQiOjE2NjU1NzQ1NDExNzEsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.1.1267307625.1692372568; _ga_KTGLXV8B2H=GS1.1.1694078221.5.0.1694078221.0.0.0; csrftoken=UsaVHzNV8ozH5ynWT7kcp0JMhiPWoylLtHwVtEWCi968v4JXjFIXpEwr7DNvTlcP; sessionid=0hho7bjjxak6erp3pm309wce0v3bkxyf; _hjIncludedInSessionSample_2798930=0; _hjSession_2798930=eyJpZCI6IjgxM2RjYjAxLTZlNTQtNDgzMi1iNDU1LTZhMzJlNTQ5MTczYyIsImNyZWF0ZWQiOjE2OTUzMzEyMjYzOTIsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _ga_SP6YTCCCW3=GS1.1.1695331226.32.1.1695331227.0.0.0'
PAGE_TOTAL = 19

REQUEST = "curl 'https://backend.app.vestlane.com/api/subscription/?format=json&page=<PAGE_NUMBER>' "\
            "-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' " \
            "-H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' " \
            "-H 'Connection: keep-alive' " \
            "-H 'Cookie: <SESSION_COOKIE>' " \
            "-H 'Sec-Fetch-Dest: document' " \
            "-H 'Sec-Fetch-Mode: navigate'" \
            "-H 'Sec-Fetch-Site: none'" \
            "-H 'Sec-Fetch-User: ?1'" \
            "-H 'Upgrade-Insecure-Requests: 1'" \
            "-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'" \
            "-H 'sec-ch-ua: \"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"'" \
            "-H 'sec-ch-ua-mobile: ?0'" \
            "-H 'sec-ch-ua-platform: \"macOS\"'" \
            "--compressed"


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


all_flattened_subscriptions = []
for page_number in range(1, PAGE_TOTAL+1):
    response = os.popen(REQUEST.replace('<SESSION_COOKIE>', SESSION_COOKIE).replace('<PAGE_NUMBER>', str(page_number))).read()
    subscriptions = json.loads(response)['results']
    for subscription in subscriptions:
        all_flattened_subscriptions.append(flatten_json(subscription))
    time.sleep(5)

df = pd.DataFrame(all_flattened_subscriptions)
df.to_excel('./output.xlsx', index=False)
