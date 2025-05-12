from ping3 import ping, verbose_ping
import socket
import csv

def my_ping(host):
    return socket.gethostbyname(host), ping(host)

hosts = ['google.com', 'yandex.ru', 'youtube.com', 'facebook.com', 'wikipedia.org', 
        'amazon.com', 'reddit.com', 'vk.com', 'pinterest.com', 'ebay.com']
with open('task1.csv', 'w') as table:
    csvwriter = csv.writer(table)
    csvwriter.writerow(['Host', 'IP', 'RTT'])
    for host in hosts:
        IP, RTT = my_ping(host)
        csvwriter.writerow([host, IP, RTT])
        print(host)
        verbose_ping(host)
