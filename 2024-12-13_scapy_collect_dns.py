# %%
from scapy.all import sniff, DNS, DNSRR
import re
import ipaddress

cidr_text = """
sudo ip route add 61.247.192.0/19 via 192.168.1.1
sudo ip route add 110.93.144.0/20 via 192.168.1.1
sudo ip route add 125.209.192.0/18 via 192.168.1.1
sudo ip route add 202.179.176.0/21 via 192.168.1.1
sudo ip route add 210.89.160.0/19 via 192.168.1.1
sudo ip route add 223.130.192.0/20 via 192.168.1.1
"""
cidr_list = []
result=re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/\d{1,3}", cidr_text)
for item in result:
    ip = item.replace('(', '').replace(')', '')
    cidr_list.append(ip)
cidr_list
site_list = ["naver.com", "daum.net", "tistory.com", "danawa.com", "11st.com", "gmarket.com", "auction.com"]

def packet_callback(packet):
    if not packet.haslayer(DNS) or packet[DNS].ancount == 0:
        return
    for i in range(packet[DNS].ancount):
        answer = packet[DNS].an[i]
        if not isinstance(answer, DNSRR) or answer.type != 1:
            continue
        domain = answer.rrname.decode().rstrip('.')
        ip_address = answer.rdata if isinstance(answer.rdata, str) else answer.rdata.decode()
        for site in site_list:
            if not re.search(site, domain):
                continue
            found = False
            for cidr in cidr_list:
                if (ipaddress.ip_address(ip_address) in ipaddress.ip_network(cidr)):
                    #print(ip, '=>',cidr)
                    found = True
                    break
            if found == False:
                print(f"{ip_address},{domain}")

print("Starting packet capture...")
sniff(filter="udp port 53", prn=packet_callback, store=False, iface='enp4s0')


