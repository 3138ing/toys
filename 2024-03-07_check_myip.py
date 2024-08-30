# %%
import requests
import time
import datetime

# %%
server = ['http://ip.seeip.org', 'http://checkip.amazonaws.com']
#'http://api.ipify.org'

server_index = 0
old_myip = ''

# %%
with open('../toys-data/var/log/check_myip.log', 'ab') as f:
    while True:
        myip = ''
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        server_index = 0 if server_index == 1 else 1
        try:
            myip = requests.get(server[server_index]).text.strip()
            text = f'{date}\t{myip}'
        except Exception as ex:
            text = f"{date}\t[EXCEPT] {server[server_index].split('.')[-2]}"
            text += f'\t{ex}'
        #
        if old_myip != myip:
            old_myip = myip
            print(text)
        #
        f.write(f'{text}\n'.encode())
        f.flush()
        #
        time.sleep(60)


