"""
provides a networking interface
to the gscheme language
"""

import ssl
import socket
import requests


def socket_create():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1)


def socket_connect(socket: socket.socket, host: str, port: int = 80):
    socket.connect((host, port))


def socket_send(socket: socket.socket, data: str):
    print(data)
    socket.sendall(bytes(data, "utf-8"))


def socket_recieve(socket: socket.socket, bytes: int):
    return socket.recv(bytes).decode("utf-8")


net_functions = {
    "socket-create": socket_create,
    "socket-connect": socket_connect,
    "socket-send": socket_send,
    "socket-recieve": socket_recieve,
    "http-get": lambda x: requests.get(x).text,
    "http-post": lambda x: requests.post(x).text,
}