import argparse
import time
import socket

parser = argparse.ArgumentParser(description='UDP通信のテストプログラム（受信側）')
parser.add_argument('-p', '--port', type=int, default=8080, help='送信側のポート（デフォルトは8080）')
parser.add_argument('-t', '--time', action='store_true', help='受信時刻の表示')
args = parser.parse_args()
port = args.port
recv_time_flag = args.time

# ipv4を使うので、AF_INET
# udp通信を使いたいので、SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.2)
# ブロードキャストするときは255.255.255.255と指定せずに空文字
sock.bind(('', port))
try:
    while True:
        # データを待ち受け
        try:
            rcv_data, addr = sock.recvfrom(1024)
        except socket.timeout:
            continue

        print('send : {}  from {}'.format(rcv_data.decode(), addr))
        if recv_time_flag:
            print('recv : {}'.format(time.time()))

except KeyboardInterrupt:
    sock.close()
    print('KeyboardInterrupt')
