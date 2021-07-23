"""
provides a networking interface
to the gscheme language
"""

import socket


def socket_create():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def socket_connect(socket: socket.socket, host: str, port: int = 80):
    socket.connect((host, port))


def socket_send(socket: socket.socket, data: str):
    socket.sendall(bytes(data, "utf-8"))


def socket_recieve(socket: socket.socket, bytes: int):
    return socket.recv(bytes).decode("utf-8")


net_functions = {
    "socket-create": socket_create,
    "socket-connect": socket_connect,
    "socket-send": socket_send,
    "socket-recieve": socket_recieve
}