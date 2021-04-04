import pickle
import time
from datetime import datetime

from menu import Menu

class ClientHandler:

    def __init__(self, server_instance, client_socket, addr):
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.client_socket = client_socket

        self.client_name = None
        self.menu = Menu()
        self.request_headers = self.menu.request_headers(self=self.menu)
        self.response_headers = self.menu.response_headers(self=self.menu)

        self.broadcast_has_read = []

    # TODO: implement the ClientHandler for this project.

    def process_client_info(self):
        self.send({'client_id': self.client_id})
        client_info = self.receive()
        self.client_name = client_info["client_name"]
        self.client_id = client_info["client_id"]

        # add the client to the client list
        self.server.add_to_client_list(self.client_id, self.client_name)

        print("CONNECT:\tClient " + self.client_name + "(client id = " + str(self.client_id) + ") has successfully connected to the server.")

    def send_menu(self):
        time.sleep(1)
        menu_data = {"menu_str": self.menu.get(self=self.menu), "request_headers": self.request_headers, "response_headers": self.response_headers}
        self.send({"menu": menu_data})
        print("CACHE_MENU:\tSend menu to Client " + self.client_name + "(client id = " + str(self.client_id) + ")")

    def process_client_option(self):
        request = self.receive()["request"]
        option = request["option"]
        response_str = None
        if 1 <= option <= 12:
            print("REQUEST:\tClient " + self.client_name + "(client id = " + str(self.client_id) + ") requests for option No." + str(option))

            if option == 1:
                response_str = self._option_1_send_user_list()
            elif option == 2:
                response_str = self._option_2_send_a_message(request)
            elif option == 3:
                response_str = self._option_3_get_my_messages()
            else:
                response_str = self._option_todo()
            time.sleep(1)
            response_data = {"response": response_str}
            self.send(response_data)
        else:
            print("REQUEST:\tClient " + self.client_name + "(client id = " + str(self.client_id) + ") requests for an invalid option")

    def _option_1_send_user_list(self):
        client_list = self.server.get_client_list()
        num_clients = len(client_list)
        cnt = 0
        response_str = "User connected: " + str(num_clients) + "\n"
        for i in client_list:
            response_str += (client_list[i] + ":" + str(i))
            cnt += 1
            if cnt < num_clients:
                response_str += ", "
        response_str += "\n"
        print("OPTION_1:\tSend user list to Client " + self.client_name + "(client id = " + str(self.client_id) + "):")
        print(response_str)
        return response_str

    def _option_2_send_a_message(self, request):
        message = request["message"]
        recipient = request["recipient"]
        timestamp = time.time()
        curr_time = datetime.now()
        curr_time_format = curr_time.strftime("%Y-%m-%d %H:%M:%S")
        if recipient == "broadcast":
            self.server.add_to_broadcast_message_list(timestamp, curr_time_format, message, recipient, self.client_name)
            self.broadcast_has_read.append(timestamp)
        else:
            self.server.add_to_private_message_list(timestamp, curr_time_format, message, recipient, self.client_name)
        response_str = "Message sent!\n"
        print("OPTION_2:\tSave the message with timestamp " + str(timestamp) + " to server from Client " + self.client_name + "(client id = " + str(self.client_id) + ")")
        return response_str

    def _option_3_get_my_messages(self):
        private_message_list = self.server.get_private_message_list()
        broadcast_message_list = self.server.get_broadcast_message_list()
        reading_list = {}
        response_str = ""
        private_has_read = []

        for key in private_message_list:
            message_data = private_message_list[key]
            if message_data["recipient"] == str(self.client_id):
                reading_list[key] = message_data
                private_has_read.append(key)

        for key in broadcast_message_list:
            if key in self.broadcast_has_read:
                continue
            reading_list[key] = broadcast_message_list[key]
            self.broadcast_has_read.append(key)

        sorted_reading_list = sorted(reading_list.items())

        for key, message_data in sorted_reading_list:
            if message_data["recipient"] == "broadcast":
                response_str += (message_data["curr_time_format"] + ": " + message_data[
                    "message"] + " (broadcast message from " + message_data["sender"] + ")\n")
                print("OPTION_3:\tClient " + self.client_name + "(client id = " + str(
                    self.client_id) + ")" + " has read public message with timestamp " + str(key))
            else:
                response_str += (message_data["curr_time_format"] + ": " + message_data[
                    "message"] + " (private message from " + message_data["sender"] + ")\n")
                print("OPTION_3:\tClient " + self.client_name + "(client id = " + str(
                    self.client_id) + ")" + " has read private message with timestamp " + str(key))

        response_str = "Number of unread messages: " + str(len(reading_list)) + "\n" + response_str
        print("OPTION_3:\tShow unread messages to Client " + self.client_name + "(client id = " + str(self.client_id) + ")")

        for key in private_has_read:
            self.server.remove_from_private_message_list(key)

        return response_str

    def _option_todo(self):
        response_str = "OPTION_TODO:\tThe requested option has not been implemented yet"
        print(response_str)
        return response_str

    def send(self, data):
        data = pickle.dumps(data)
        self.client_socket.send(data)

    def receive(self):
        data = self.client_socket.recv(4090)
        if not data:
            print("DISCONNECT:\tClient " + self.client_name + "(client id = " + str(self.client_id) + ") disconnected!")
            # remove the client from the client list
            self.server.remove_from_client_list(self.client_id)
            exit(1)
        return pickle.loads(data)

    def run(self):
        self.process_client_info()
        self.send_menu()
        while True:
            self.process_client_option()
        return
