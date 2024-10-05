import argparse
import time
import socket

parser = argparse.ArgumentParser(description='UDP通信のテストプログラム（送信側）')
parser.add_argument('-H', '--host', default='<broadcast>', help='送信側のホストIP（デフォルトはbroadcast）')
parser.add_argument('-p', '--port', type=int, default=8080, help='送信側のポート（デフォルトは8080）')
parser.add_argument('-n', '--num', type=int, default=1, help='送信回数（デフォルトは1）')
parser.add_argument('-i', '--interval', type=float, default=1.0, help='送信間隔[s]（デフォルトは1.0）')
args = parser.parse_args()
host = args.host
port = args.port
num = args.num
interval = args.interval

# ipv4を使うので、AF_INET
# udp通信を使いたいので、SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ブロードキャストを行うので、設定
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# データ送信
for n in range(num):
    t = str(time.time())
    print('send: {}'.format(t))
    sock.sendto(t.encode(), (host, port))
    if n < num - 1:
        time.sleep(interval)

sock.close()
