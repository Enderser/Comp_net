from ping3 import ping, verbose_ping
import socket
import csv

def my_ping(host):
    ip_address = socket.gethostbyname(host)
    rtt = ping(host)
    return ip_address, rtt

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
