import argparse
import socket

parser = argparse.ArgumentParser(description='UDP通信のテストプログラム（受信側）')
parser.add_argument('-p', '--port', type=int, default=8080, help='受信するポート（デフォルトは8080）')
args = parser.parse_args()
port = args.port

# ipv4を使うので、AF_INET
# udp通信を使いたいので、SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.1)
# ブロードキャストするときは255.255.255.255と指定せずに空文字
sock.bind(('', port))
try:
    while True:
        # データを待ち受け
        try:
            rcv_data, addr = sock.recvfrom(1024)
        except socket.timeout:
            continue

        print('recv : {}  from {} to port ({})'.format(rcv_data.decode(), addr, port))

except KeyboardInterrupt:
    sock.close()
    print('KeyboardInterrupt')
