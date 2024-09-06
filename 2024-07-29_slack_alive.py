# %%
import sys
sys.path.insert(0, '../toys-data')
import conf

# %%
import requests

# %%
def slack(title, content, ip):
    requests.post(
        f'https://hooks.slack.com/services/{conf.SLACK_WEBHOOK_URL}',
        headers={
            'content-type': 'application/json'
        },
        json={
            'text': title,
            'blocks': [
            {
                'type': 'section',
                'text': {
                'type': 'mrkdwn',
                'text': f'{content}{ip}'
                }
            }
            ]
        }
    )

# %%
def getmyip():
    try:
        return requests.get(r'http://checkip.amazonaws.com').text.strip()
    except:
        try:
            return requests.get(r'http://api.ipify.org').text.strip()
        except:
            return ""

# %%
slack("굿모닝", ":sun_with_face::smile:", getmyip())


