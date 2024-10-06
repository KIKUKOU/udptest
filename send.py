import argparse
import datetime
import ipaddress
import time
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
self_addr = sock.getsockname()[0]
sock.close()
self_addr = ipaddress.ip_address(self_addr)

t_delta = datetime.timedelta(hours=9)

JST = datetime.timezone(t_delta, 'JST')
IPv4 = 4
IPv6 = 6

parser = argparse.ArgumentParser(description='UDP通信のテストプログラム（送信側）')
parser.add_argument('-H', '--host', default='255.255.255.255', help='送信元のホストIP（デフォルトは255.255.255.255）')
parser.add_argument('-P', '--port', type=int, default=-1, help='送信元のポート（デフォルトは設定なし）')
parser.add_argument('-p', '--dport', type=int, default=8080, help='送信先のポート（デフォルトは8080）')
parser.add_argument('-n', '--num', type=int, default=1, help='送信回数（デフォルトは1）')
parser.add_argument('-i', '--interval', type=float, default=1.0, help='送信間隔[s]（デフォルトは1.0）')
args = parser.parse_args()

host_addr = ipaddress.ip_address(args.host)
self_port = args.port
host_port = args.dport
num = args.num
interval = args.interval

# udp通信のソケット設定
if host_addr.version == IPv4:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=17)
    print('UDP IPv4 from {}'.format(str(self_addr)))
elif host_addr.version == IPv6:
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, proto=17)
    print('UDP IPv4 from {}'.format(str(self_addr)))
else:
    print('Input is not IP address.')
    raise

# Broadcast or Multicast or Unicastの設定
# Broadcastの判定は簡易的に末尾255で判断
if str(host_addr)[-3:] == '255':
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print('Broadcast Mode')
elif host_addr.is_multicast:
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(str(self_addr)))
    print('Multicast Mode')
else:
    print('Unicast Mode')

# 送信先のポート設定
if self_port != -1:
    sock.bind(('', self_port))

# データ送信
for n in range(num):
    t = datetime.datetime.now(JST).strftime('%x %X.%f %z(%Z)')
    send_data = '{} host {}:{}'.format(t, str(host_addr), host_port)
    print(send_data)
    send_data = send_data.encode()
    sock.sendto(send_data, (str(host_addr), host_port))
    if n < num - 1:
        time.sleep(interval)

sock.close()
