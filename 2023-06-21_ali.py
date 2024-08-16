# %%
import sys
sys.path.insert(0, '../toys-data')
import conf

# %%
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup
import json
import time

project_id = '2023062100'

#page_base = f"{conf.get_base_url(project_id)}/w/wholesale-%EC%97%AC%EC%84%B1-%ED%99%94%EC%9E%A5%ED%92%88-%EB%A7%A4%EC%89%AC-%ED%8C%8C%EC%9A%B0%EC%B9%98.html?SearchText=%EC%97%AC%EC%84%B1+%ED%99%94%EC%9E%A5%ED%92%88+%EB%A7%A4%EC%89%AC+%ED%8C%8C%EC%9A%B0%EC%B9%98&catId=0&g=y&initiative_id=SB_20230620200505&spm=a2g0o.productlist.1000002.0&trafficChannel=main"

keyword = '여성 화장품 매쉬 파우치'
page_base = f"{conf.get_base_url(project_id)}/w/wholesale-{parse.quote(keyword.replace(' ', '-'))}.html?SearchText={parse.quote(keyword.replace(' ', '+'))}"

def get_url(page_number):
   if page_number == 1:
      return page_base
   return page_base + "&page=" + str(page_number)

def get_soap(page_number, url):
   #print(f'[soup]')
   #print('    [url]', page_number, url)
   with urlopen(url) as response:
      soup = BeautifulSoup(response, 'html.parser')
   return soup

def get_jscript(soup):
   #print('    [jscript...]')
   jscript = ''
   jcount = 0
   for item in soup.find_all('script'):
      if item.text.find('hierarchy') == -1:
         continue
      jcount += 1
      #print('        jscript', jcount)
      jscript = item.text
      break
   return jscript

def get_json(jscript):
   #print('    [json...]')
   begin_text = '"root":["'
   end_text = '"'
   begin = jscript.find(begin_text)
   if begin == -1:
      return None
   end = jscript.find(end_text, begin + len(begin_text))
   if end == -1:
      return None

   begin_text = '"data"'
   end_text = '"storeDirect_3641"'
   begin = jscript.find(begin_text, end)
   if begin == -1:
      return None
   end = jscript.find(end_text, begin + len(begin_text))
   if end == -1:
      return None

   text = '{' + jscript[begin:end].strip().strip(',') + '}}'
   return json.loads(text)

dic_productId = {}

def do_parsing():
   #print('    [parsing...]')
   num = 0
   if 'itemList' not in data_json['data']['root']['fields']['mods']:
      #print(data_json['data']['root']['fields']['mods'])
      return False
   for content in data_json['data']['root']['fields']['mods']['itemList']['content']:
      num += 1
      #print(content['trace']['utLogMap']['formatted_price'])
      
      displayTitle = content['title']['displayTitle']
      productId = content['productId']
      
      if productId not in dic_productId:
         dic_productId[productId] = 1
      else:
         continue
      if 'originalPrice' in content['prices']:
         price = int(content['prices']['originalPrice']['formattedPrice'].replace('₩ ', '').replace(',', ''))
      else:
         price = int(content['prices']['salePrice']['formattedPrice'].replace('₩ ', '').replace(',', ''))
      if price < 1000:
         print(num, price, displayTitle[:10], f'{conf.get_base_url(project_id)}/item/{productId}.html')
   return True

for page_number in range(1, 11):
   time.sleep(1)
   stop_retry = False
   for retry in range(1, 10):
      if stop_retry == True:
         break
      url = get_url(page_number)
      soup = get_soap(page_number, url)
      jscript = get_jscript(soup)
      if len(jscript) == 0:
         stop_retry = True
         continue
      data_json = get_json(jscript)
      if data_json is None:
         stop_retry = True
         continue
      succeeded = do_parsing()
      if succeeded == True:
         stop_retry = True
         continue
      else:
         stop_retry = False
         continue
      


