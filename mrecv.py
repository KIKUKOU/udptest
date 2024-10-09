import argparse
import socket
import struct

parser = argparse.ArgumentParser(description='UDP通信のテストプログラム（受信側）')
parser.add_argument('-H', '--host', default='224.0.0.1', help='送信元のホストIP（デフォルトは224.0.0.1）')
parser.add_argument('-p', '--port', type=int, default=8080, help='受信するポート（デフォルトは8080）')
parser.add_argument('-m', '--message', action='store_true')
args = parser.parse_args()

multicast_group = args.host
port = args.port
is_only_massage = args.message
timeout = 0.1


# udp通信のソケット設定
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.settimeout(timeout)
# アドレスを指定せずとにかく流れてきたものを受信する
sock.bind(('', port))

# マルチキャストグループへの参加

group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

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