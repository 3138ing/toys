import requests
import json
import time
import random
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib

class movie_request_item:
    def __init__(self, brchNo, brchNm, playDe):
        self.url = 'https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do'
        self.json = {"masterType":"brch","brchNo":brchNo,"brchNm":brchNm,"firstAt":"Y","brchNo1":brchNo, "playDe":playDe}
        self.brchNm = brchNm
        self.playDe = playDe
        self.mcount = -1

mitems = [
      movie_request_item('1351','코엑스','20230114')
    , movie_request_item('1351','코엑스','20230115')
    , movie_request_item('0019','남양주현대아울렛 스페이스원','20230114')
    , movie_request_item('0019','남양주현대아울렛 스페이스원','20230115')]

def mail(mitem, contents):
    # SMTP
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_SERVER = 'smtp.live.com'
    SMTP_SERVER = 'smtp.naver.com'
    SMTP_SERVER = ...
    SMTP_PORT = 465
    SMTP_PORT = 587
    SMTP_PORT = ...
    SMTP_USER = ...
    SMTP_PASSWORD = ...
    
    # mime
    msg = MIMEMultipart('alternative')
    msg['From'] = ...
    msg['To'] = ...
    msg['Subject'] = mitem.brchNm

    mimetext = MIMEText(contents, _charset='utf-8')
    msg.attach(mimetext)

    # smtp
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context = ssl.create_default_context()
    ssl_context.set_ciphers('DEFAULT:!DH')
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ssl_context)
    smtp.login(SMTP_USER, SMTP_PASSWORD)
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.close()

def slack(mitem, contents):
    requests.post(
    'https://hooks.slack.com/services/.../...',
    headers={
        'content-type': 'application/json'
    },
    json={
        'text': mitem.brchNm,
        'blocks': [
        {
            'type': 'section',
            'text': {
            'type': 'mrkdwn',
            'text': contents
            }
        }
        ]
    }
    )

def alarm(mitem):
    date = datetime.strptime(str(mitem.playDe), '%Y%m%d')
    date = date.strftime(f"%Y-%m-%d {'월화수목금토일'[date.weekday()]}")

    contents = mitem.brchNm + '\t' +  date + '\t' + str(mitem.mcount)
    print(contents)
    
    mail(mitem, contents)
    slack(mitem, contents)
    
def check(mitem):
    http_post_request = requests.post(mitem.url, json = mitem.json)
    js = json.loads(http_post_request.text)

    mcount = 0
    for mv in js['megaMap']['movieFormList']:
        if mv['movieNm'].find('아바타') != -1 and mv['movieNm'].find('4K') != -1:
            if mv['playSchdlNo'].startswith(mitem.playDe[2:]):
                mcount += 1
    if mitem.mcount != mcount:
        mitem.mcount = mcount
        alarm(mitem)
        
    time.sleep(random.randrange(50,70))

while True:
    for mitem in mitems:
        check(mitem)
