#!/usr/bin/env python3
import socket
import sys


def find_free_port(start=8000, end=8099):
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    raise RuntimeError(f'No free port in range {start}-{end}')


if __name__ == '__main__':
    print(find_free_port())
