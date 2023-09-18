# %%
# %%
import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
import time

# %%
def get_soap(url, id):
    time.sleep(0.5)
    print(f'[soup]')
    print('    [url]', id, url)
    headers = CaseInsensitiveDict()
    headers["Cookie"] = "ci_session=80aamtsnpm26kuhsmsc3v1595lf5njp8; assoc_id=34"
    response = requests.post(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# %%
base_url = 'http://ccnplaza.com/tkd_compet/match/match_list'

# %%
class_a_list = []
class_a_name_list = []

soup = get_soap(base_url, 'start')
for item in soup.find_all('option'):
    value = int(item.get('value'))
    if value < 10000:
        class_a_list.append(str(value))
        class_a_name_list.append(item.text)

# %%
class_b_list = []
class_b_name_list = []

for name_index, class_a_item in enumerate(class_a_list):
    soup = get_soap(base_url + '/' + class_a_item, class_a_item)
    for item in soup.find_all('option'):
        value = int(item.get('value'))
        if value > 10000:
            class_b_list.append((class_a_item, str(value)))
            class_b_name_list.append((class_a_name_list[name_index], item.text))

# %%
soup_list = []

for class_b_item in class_b_list:
    print(class_b_item)
    soup = get_soap(base_url + '/' + class_b_item[0] + '/' + class_b_item[1], class_b_item[0] + '/' + class_b_item[1])
    soup_list.append(soup)


# %%
for name_index, soup_item in enumerate(soup_list):
    # div
    div_list = soup_item.find_all("div", {"class": "col-md-9"})
    if div_list is None:
        print('Div None!!!')
        continue
    if len(div_list) == 0:
        print('Div 0!!!')
        continue
    # th
    th_list = div_list[0].find_all('th')
    if th_list is None:
        print('Th None!!!')
        continue
    if len(th_list) == 0:
        print('Th 0!!!')
        continue
    # tbody
    tbody_list = div_list[0].find_all('tbody')
    if tbody_list is None:
        print('Tbody None!!!')
        continue
    if len(tbody_list) == 0:
        print('Tbody 0!!!')
        continue
    # tr
    tr_list = tbody_list[0].find_all('tr')
    if tr_list is None:
        print('Tr None!!!')
        continue
    if len(tr_list) == 0:
        #print('Tr 0!!!')
        continue
    # td
    for index, tr_item in enumerate(tr_list):
        td_list = tr_item.find_all('td')
        if td_list is None:
            print('Td None!!!')
            continue
        if len(td_list) == 0:
            print('Td 0!!!')
            continue
        person = [str(len(td_list)), class_b_name_list[name_index][0], class_b_name_list[name_index][1]]
        for td_item in td_list:
            person.append(td_item.text.strip())
        if len(td_list) == 7:
            person.insert(4, '')
        print(person)


