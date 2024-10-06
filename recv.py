import argparse
import socket

parser = argparse.ArgumentParser(description='UDP通信のテストプログラム（受信側）')
parser.add_argument('-p', '--port', type=int, default=8080, help='受信するポート（デフォルトは8080）')
parser.add_argument('-m', '--message', action='store_true')
args = parser.parse_args()

port = args.port
is_only_massage = args.message
timeout = 0.1


# ipv4での通信⇒AF_INET
# udp通信⇒SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(timeout)
# アドレスを指定せずとにかく流れてきたものを受信する
sock.bind(('', port))
try:
    while True:
        # データ受信
        try:
            recv_data, addr = sock.recvfrom(1024)
            recv_data = recv_data.decode()
        except socket.timeout:
            continue

        # タイムアウトせず受信できた回のみ受信データを出力
        if is_only_massage:
            print('recv : {}'.format(recv_data))
        else:
            print('recv : {} | from {}:{}'.format(recv_data, addr[0], addr[1]))

except KeyboardInterrupt:
    sock.close()
    print('KeyboardInterrupt')
