########################################################################################################################
# Class: Computer Networks
# Date: 02/15/2021
# Lab3: TCP Client Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Zhuofu Liu
# Student ID: 920673504
# Student Github Username: zhuofu0513
# Instructions: Read each problem carefully, and implement them correctly.
########################################################################################################################

# don't modify this imports.
import socket
import pickle
from client_helper import ClientHelper

######################################## Client Socket ###############################################################3
"""
Client class that provides functionality to create a client socket is provided. Implement all the methods but bind(..)
"""


class Client(object):

    def __init__(self):
        """
        Class constructor
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = None
        self.server_port = 0
        self.client_id = 0
        self.client_name = None

    def connect(self):
        """
        TODO: Create a connection from client to server
              Note that this method must handle any exceptions
        :server_ip_address: the know ip address of the server
        :server_port: the port of the server
        """
        try:
            # get server info
            self.server_ip = input("Enter the server IP Address: ")
            self.server_port = int(input("Enter the server port: "))
            # get client name
            self.client_name = input("Enter a username: ")
            # connect
            self.client_socket.connect((self.server_ip, self.server_port))
            # set client id
            recv_data = self.receive()
            self.client_id = recv_data['client_id']
            # send client info
            send_data = {'client_name': self.client_name, 'client_id': self.client_id}
            self.send(send_data)

            # print success info
            print("Successfully connected to server: " + self.server_ip + "/" + str(self.server_port))

        except ConnectionError as connectionError:
            print('ConnectionError:', connectionError)
            exit(1)

    def bind(self, client_ip='', client_port=12000):
        """
        DO NOT IMPLEMENT, ALREADY IMPLEMENTED
        This method is optional and only needed when the order or range of the ports bind is important
        if not called, the system will automatically bind this client to a random port.
        :client_ip: the client ip to bind, if left to '' then the client will bind to the local ip address of the machine
        :client_port: the client port to bind.
        """
        self.client_socket.bind((client_ip, client_port))

    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data: the raw data to serialize (note that data can be in any format.... string, int, object....)
        :return: VOID
        """
        data = pickle.dumps(data)
        self.client_socket.send(data)

    def receive(self, max_alloc_buffer=4090):
        """
        TODO: Deserializes the data received by the server
        :param max_alloc_buffer: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        data = self.client_socket.recv(max_alloc_buffer)
        return pickle.loads(data)

    def client_helper(self):
        """
        TODO: create an object of the client helper and start it.
        """
        client_helper = ClientHelper(self)
        client_helper.run()

    def close(self):
        """
        TODO: close this client
        :return: VOID
        """
        self.client_socket.close()

    def get_client_name(self):
        return self.client_name

    def get_client_id(self):
        return self.client_id


# main code to run client
if __name__ == '__main__':
    client = Client()
    client.connect()  # creates a connection with the server
    client.client_helper()
