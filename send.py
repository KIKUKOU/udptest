import argparse
import datetime
import time
import socket

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')

parser = argparse.ArgumentParser(description='UDP通信のテストプログラム（送信側）')
parser.add_argument('-H', '--host', default='<broadcast>', help='送信元のホストIP（デフォルトはbroadcast）')
parser.add_argument('-P', '--port', type=int, default=-1, help='送信元のポート（デフォルトは設定なし）')
parser.add_argument('-p', '--dport', type=int, default=8080, help='送信先のポート（デフォルトは8080）')
parser.add_argument('-n', '--num', type=int, default=1, help='送信回数（デフォルトは1）')
parser.add_argument('-i', '--interval', type=float, default=1.0, help='送信間隔[s]（デフォルトは1.0）')
args = parser.parse_args()
host = args.host
send_port = args.port
distination_port = args.dport
num = args.num
interval = args.interval

# ipv4での通信⇒AF_INET
# udp通信⇒SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ブロードキャストの設定
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# 送信元のポート設定
if send_port != -1:
    print(send_port)
    sock.bind(('', send_port))

# データ送信
for n in range(num):
    t = now = datetime.datetime.now(JST).strftime('%x %X.%f %z(%Z)')
    print('send: {}'.format(t))
    sock.sendto(t.encode(), (host, distination_port))
    if n < num - 1:
        time.sleep(interval)

sock.close()
