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

        self.channel_info = {}

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
                response_data = {"response": response_str}
                self.send(response_data)
            elif option == 2:
                response_str = self._option_2_send_a_message(request)
                response_data = {"response": response_str}
                self.send(response_data)
            elif option == 3:
                response_str = self._option_3_get_my_messages()
                response_data = {"response": response_str}
                self.send(response_data)
            elif option == 4:
                self._option_4_send_a_direct_msg_via_udp(request)
                response_data = {"response": response_str}
                self.send(response_data)
            elif option == 5:
                response_str = self._option_5_send_a_broadcast_message(request)
                response_data = {"response": response_str}
                self.send(response_data)
            elif option == 6:
                response_str = self._option_6_create_a_secure_channel(request)
                response_data = {"response": response_str}
                self.send(response_data)

                self._loop_in_channel()
            else:
                response_str = self._option_todo()
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
        curr_time_format = curr_time.strftime("%Y-%m-%d %H:%M")
        self.server.add_to_message_list(timestamp, curr_time_format, message, recipient, self.client_name, private=True)
        response_str = "Message sent!\n"
        print("OPTION_2:\tSave the private message with timestamp " + str(timestamp) + " to server from Client " + self.client_name + "(client id = " + str(self.client_id) + ")")
        return response_str

    def _option_3_get_my_messages(self):
        message_list = self.server.get_message_list()
        reading_list = {}
        response_str = ""

        for key in message_list:
            message_data = message_list[key]
            if message_data["recipient"] == str(self.client_id):
                reading_list[key] = message_data

        sorted_reading_list = sorted(reading_list.items())

        for key, message_data in sorted_reading_list:
            if message_data["private"] is False:
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

        for key in reading_list:
            self.server.remove_from_message_list(key)

        return response_str

    def _option_4_send_a_direct_msg_via_udp(self, request):
        print("OPTION_4\tClient " + self.client_name + "(client id = " + str(self.client_id) + ") sent a direct message to " + request["recipient_address"] + " from " + request["sender_address"])
        return None

    def _option_5_send_a_broadcast_message(self, request):
        message = request["message"]
        curr_time = datetime.now()
        curr_time_format = curr_time.strftime("%Y-%m-%d %H:%M")
        for client in self.server.get_client_list():
            if client != self.client_id:
                recipient = str(client)
                timestamp = time.time()
                self.server.add_to_message_list(timestamp, curr_time_format, message, recipient, self.client_name, private=False)
                print("OPTION_5:\tSave the broadcast message with timestamp " + str(
                    timestamp) + " to server from Client " + self.client_name + "(client id = " + str(self.client_id) + ")")
        response_str = "Message broadcast!\n"
        return response_str

    def _option_6_create_a_secure_channel(self, request):
        channel_id = request["channel_id"]
        self.channel_info["channel_id"] = channel_id
        self.channel_info["admin_id"] = int(self.client_id)
        self.channel_info["admin_name"] = self.client_name

        self.server.creat_a_channel(channel_id, self.client_id, self.client_name)
        print("OPTION_6:\tChannel #" + channel_id + " created, admin is " + self.client_name)

        response_str = "Private key received from server and channel " + channel_id + " was successfully created!\n" + \
                       "\n" + \
                       "----------------------- Channel " + channel_id + " ------------------------\n" + \
                       "\n" + \
                       "All the data in this channel is encrypted\n" + \
                       "\n" + \
                       "General Admin Guidelines:\n" + \
                       "1. #" + self.client_name + " is the admin of this channel\n" + \
                       "2. Type '#exit' to terminate the channel (only for admins)\n" + \
                       "\n" + "\n" + \
                       "General Chat Guidelines:\n" + "1. Type #bye to exit from this channel. (only for non-admins users)\n" + \
                       "2. Use #<username> to send a private message to that user.\n" + "\n" + \
                       "Waiting for other users to join....\n"
        return response_str

    def _loop_in_channel(self):
        time.sleep(1)
        self.send({"channel_info": self.channel_info})
        print("OPTION_6:\tSend channel info to Client " + self.client_name + "(client id = " + str(self.client_id) + ")")

        has_read_list = []

        while True:
            channel_msg_list = self.server.get_channel_msg_list(self.channel_info["channel_id"])
            for key in channel_msg_list:
                if key not in has_read_list:
                    msg_data = channel_msg_list[key]
                    if msg_data["sender_name"] != self.client_name:
                        if msg_data["receiver_name"] == "channel_public" or msg_data["receiver_name"] == self.client_name:
                            self.send({"chat_msg_recv": msg_data["message"]})
                            has_read_list.append(key)

            new_msg = self.receive()["chat_msg_send"]
            sender_name = self.client_name
            receiver_name = "channel_public";
            if new_msg[0] == '#':
                if self.client_id == self.channel_info["admin_id"] and new_msg == "#exit":
                    return
                elif self.client_id != self.channel_info["admin_id"] and new_msg == "#bye":
                    return
                else:
                    receiver_name = new_msg.split()[0][1:]
                    new_msg = new_msg[len(receiver_name) + 2:]

            new_msg = sender_name + "> " + new_msg

            timestamp = time.time()
            msg_data = {"sender_name": sender_name, "receiver_name": receiver_name, "message": new_msg}
            self.server.add_msg_to_channel(self.channel_info["channel_id"], timestamp, msg_data)

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
