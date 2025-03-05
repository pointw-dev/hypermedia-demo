#!/usr/bin/env python3

import socket


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 12345))  # 12345 is random port. 0 fails on Mac.
    return s.getsockname()[0]


def main():
    with open('.env', 'w') as f:
        f.write(f'IP_ADDRESS={get_ip_address()}')


if __name__ == '__main__':
    main()
