# don't modify this imports.
import socket
import pickle
from threading import Thread
from client_handler import ClientHandler
import hashlib


class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10  # keeps 10 clients in queue

    def __init__(self, host="127.0.0.1", port=12000):
        """
        TODO: copy and paste your implementation from lab 3 for self.server socket property
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # your implementation for this socket here
        self.client_list = {}
        self.message_list = {}
        self.channels = {}

        self.bots = {}

    def _bind(self):
        """
        TODO: copy and paste your implementation from lab 3
        :return: VOID
        """
        self.server_socket.bind((self.host, self.port))

    def _listen(self):
        """
        TODO: copy and paste your implementation from lab 3
        :return: VOID
        """
        try:
            self._bind()
            self.server_socket.listen(self.MAX_NUM_CONN)
            print("Listening at " + str(self.host) + "/" + str(self.port))
        except:
            print("ERROR: server could not listen at " + str(self.host) + "/" + str(self.port))
            self.server_socket.close()

    def _accept_clients(self):
        """
        #TODO: Modify your implementation from lab 3, so now the
               server can support multiple clients pipelined.
               HINT: you must thread the handler(...) method
        :return: VOID
        """
        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = Thread(target=self._handler, args=(client_socket, addr), daemon=True)
            client_thread.start()

    def _handler(self, client_socket, addr):
        """
        TODO: create an object of the ClientHandler.
              see the client_handler.py file to see
              the parameters that must be passed into
              the ClientHandler's constructor to create
              the object.
              Once the ClientHandler object is created,
              add it to the dictionary of client handlers initialized
              on the Server constructor (self.handlers)
        :clienthandler: the clienthandler child process that the server creates when a client is accepted
        :addr: the addr list of server parameters created by the server when a client is accepted.
        """
        client_handler = ClientHandler(self, client_socket, addr)
        client_handler.run()

    def get_client_list(self):
        return self.client_list

    def add_to_client_list(self, client_id, client_name):
        self.client_list[client_id] = client_name
        return

    def remove_from_client_list(self, client_id):
        self.client_list.pop(client_id)
        return

    def get_message_list(self):
        return self.message_list

    def add_to_message_list(self, timestamp, curr_time_format, message, recipient, sender, private):
        self.message_list[timestamp] = {"curr_time_format": curr_time_format, "message": message, "recipient": recipient, "sender": sender, "private": private}
        return

    def remove_from_message_list(self, timestamp):
        self.message_list.pop(timestamp)
        return

    def creat_a_channel(self, channel_id, admin_id, admin_name):
        self.channels[channel_id] = {"channel_id": channel_id, "admin_id": admin_id, "admin_name": admin_name, "normal_users": [], "msg_list": {}}

    def terminate_a_channel(self, channel_id):
        self.channels.pop(channel_id)
        return

    def remove_user_from_channel(self, channel_id, user_name):
        channel = self.channels[channel_id]
        normal_users = channel["normal_users"]
        normal_users.remove(user_name)
        return

    def get_channel_info(self, channel_id):
        return self.channels[channel_id]

    def add_user_to_channel(self, channel_id, user_name):
        channel = self.channels[channel_id]
        normal_users = channel["normal_users"]
        normal_users.append(user_name)
        return

    def add_msg_to_channel(self, channel_id, timestamp, msg_data):
        channel = self.channels[channel_id]
        msg_list = channel["msg_list"]
        msg_list[timestamp] = msg_data
        return

    def get_channel_msg_list(self, channel_id):
        return self.channels[channel_id]["msg_list"]

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._listen()
        self._accept_clients()

    def create_a_bot(self, token, bot_name, client_id, permissions):
        self.bots[token] = {"bot_name": bot_name, "client_id": client_id, "permissions": permissions}

# main execution
if __name__ == '__main__':
    server = Server()
    server.run()
