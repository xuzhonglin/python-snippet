#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/7/23 8:08
@Author   : colinxu
@File     : port2port.py
@Desc     : 端口转发
"""
import socket
from argparse import ArgumentParser
from threading import Thread
import os
from time import sleep


class Port2Port:

    def __init__(self, listen_port, remote_port, listen_ip, remote_ip, service):
        self.listen_port = int(listen_port)
        self.remote_port = int(remote_port)
        self.listen_ip = listen_ip
        self.remote_ip = remote_ip
        self.service = service
        if self.service:
            self.service = self.service.lower()
        self.is_socket_closed = True
        self.pid = os.getpid()  # use pid for kill the process

    def start(self):

        print(f'listen ip : {self.listen_ip} listen port : {self.listen_port}')
        print(f'remote ip : {self.remote_ip} remote port : {self.remote_port}')

        while True:
            if self.is_socket_closed:
                self.start_listening()
                Thread(target=self.start_accepting).start()
                # handling Ctrl-C
                try:
                    while True:
                        sleep(10)
                except KeyboardInterrupt:
                    os.kill(self.pid, 9)

    def start_listening(self):
        """
        this function starts listening on a port ,for forwarding
        """

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.bind((self.listen_ip, self.listen_port))
            self.client_socket.listen(1)
        except Exception as e:
            print(f'Error --> {e}')
            self.is_socket_closed = True
            return
        else:
            self.is_socket_closed = False

    def start_accepting(self):
        """
        this functions starts a
        :return:
        """

        try:
            print('Listening for accepting connections ...')
            self.client_conn, addr = self.client_socket.accept()
            print(f'client connected : {addr[0]}')

        except Exception as e:
            print(f'Error --> {e}')
            self.close_both_connection()

        else:
            self.connect_to_remote_socket()

    def connect_to_remote_socket(self):
        """
        this function creates remote socket ,for forwarding
        """

        self.remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.remote_socket.connect((self.remote_ip, self.remote_port))

        except Exception as e:
            print(f'Error --> {e}')
            self.close_both_connection()

        else:
            Thread(target=self.forward_to_remote_port).start()
            Thread(target=self.forward_from_remote_port).start()

    def forward_to_remote_port(self):
        """
        this function forwards client socket data to remote socket
        """

        try:
            while True:
                client_data = self.client_conn.recv(4096)
                if not client_data:
                    self.close_both_connection()
                    break
                try:
                    final_data = (
                        self.commit_client_service_filters(data=client_data.decode(), _from='client')).encode()
                except:
                    final_data = client_data

                self.remote_socket.sendall(final_data)

        except Exception as e:
            print(f'Error --> {e}')
            self.close_both_connection()

    def forward_from_remote_port(self):
        """
        this function forwards remote socket data to client socket
        """

        try:
            while True:
                remote_data = self.remote_socket.recv(4096)
                if not remote_data:
                    self.close_both_connection()
                    break
                try:
                    final_data = (
                        self.commit_client_service_filters(data=remote_data.decode(), _from='remote')).encode()
                except:
                    final_data = remote_data

                self.client_conn.sendall(final_data)


        except Exception as e:
            print(f'Error --> {e}')
            self.close_both_connection()

    def close_both_connection(self):
        """
        this function closes both remote and client connections
        :return:
        """
        try:
            self.client_conn.close()
            self.remote_socket.close()
            self.client_socket.close()
            self.is_socket_closed = True

        except Exception as e:
            print(f'Error --> {e}')

    def commit_client_service_filters(self, data, _from):
        """
        this function process data and change them if it is necessary and if service is not None
        :param self:
        :param :data
        data is data from/to remote port before processing
        :param _from:
        _from can be "remote" ---> from remote socket  or "client" ---> from client socket
        :return:
        """
        sc_name = self.service  # sc_name is service name like http
        processed_data = None  # return var

        if sc_name is None:
            processed_data = data
            return processed_data

        if sc_name == 'http':
            if _from == 'client':
                data = data.replace(self.client_conn.getsockname()[0], self.remote_ip)
                data = data.replace(f':{self.listen_port}', f':{self.remote_port}')
                processed_data = data
                return processed_data

            elif _from == 'remote':
                data = data.replace(self.remote_ip, self.client_conn.getsockname()[0])
                data = data.replace(f':{self.remote_port}', f':{self.listen_port}')
                processed_data = data
                return processed_data


def print_help():
    help_msg = '''
usage: port2port.py [-h] [-lp LISTEN_PORT] [-rp REMOTE_PORT] [--listen-ip LISTEN_IP [default : 0.0.0.0]]
arguments:
  --listen-port or -lp LISTEN_PORT (listen port number)
  --remote-port or -rp REMOTE_PORT (remote port to forward)

optional arguments :
   --listen-ip or -lip LISTEN_IP (ip address to listen [default : 0.0.0.0])
   --remote-ip or -rip LISTEN_IP (ip address to forward [default : 127.0.0.1])
   --service or -sc SERVICE (Determine Service : [http])

   -h or --help                  (show this help message and exit)
    '''
    print(help_msg)


if __name__ == '__main__':
    parser = ArgumentParser(allow_abbrev=False, add_help=False)
    parser.add_argument('-lp', '--listen-port', help='listen port number')
    parser.add_argument('-rp', '--remote-port', help='remote port to forward')
    parser.add_argument('-lip', '--listen-ip', help='ip address to listen [default : 0.0.0.0]', default='0.0.0.0')
    parser.add_argument('-rip', '--remote-ip', help='ip address to forward [default : 127.0.0.1]', default='127.0.0.1')
    parser.add_argument('-sc', '--service', help='Determine Service [http]', default=None)
    args, unknown = parser.parse_known_args()

    if args.listen_port and args.remote_port:
        port2port = Port2Port(args.listen_port, args.remote_port, args.listen_ip, args.remote_ip, args.service)
        port2port.start()
    else:
        print_help()
