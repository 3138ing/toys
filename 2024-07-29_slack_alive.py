# %%
import sys
sys.path.insert(0, '../toys-data')
import conf

# %%
import requests
def slack_by_requests(title, content, ip):
    response = requests.post(
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
    for key, value in response.headers.items():
        print(f"{key}: {value}")

    print("\nBody:")
    print(response.text)
    print("HTTP Status Code:", response.status_code)

# %%
import subprocess
import json
import syslog
def slack_by_curl(msg):
    slack_webhook_url = f"https://hooks.slack.com/services/{conf.SLACK_WEBHOOK_URL}"
    curl_command = [
        "curl",
        "-k", "-i",
        "-X", "POST",
        "-H", "Content-type: application/json",
        "--data", json.dumps({"text": msg}),
        slack_webhook_url
    ]
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        response = result.stdout
        #
        syslog.openlog(ident="slack", logoption=syslog.LOG_PID)
        for line in response.split('\n'):
            syslog.syslog(syslog.LOG_INFO, f"{line}")
        syslog.closelog()
    except subprocess.CalledProcessError as e:
        syslog.openlog(ident="slack", logoption=syslog.LOG_PID)
        syslog.syslog(syslog.LOG_ERR, f"[EXCEPTION] [CalledProcessError] {e.stderr}")
        syslog.closelog()
    except Exception as e:
        syslog.openlog(ident="slack", logoption=syslog.LOG_PID)
        syslog.syslog(syslog.LOG_ERR, f"[EXCEPTION] {e}")  
        syslog.closelog()

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
#slack_by_requests("굿모닝", ":sun_with_face: :smile: :herb: ", getmyip())
slack_by_curl(f":sun_with_face: :smile: :herb: {getmyip()}")
