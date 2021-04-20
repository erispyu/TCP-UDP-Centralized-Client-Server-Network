import pickle
import time
from datetime import datetime
from threading import Thread
import hashlib
import random

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

        print("CONNECT:\tClient " + self.client_name + "(client id = " + str(
            self.client_id) + ") has successfully connected to the server.")

    def send_menu(self):
        menu_data = {"menu_str": self.menu.get(self=self.menu), "request_headers": self.request_headers,
                     "response_headers": self.response_headers}
        self.send({"menu": menu_data})
        print("CACHE_MENU:\tSend menu to Client " + self.client_name + "(client id = " + str(self.client_id) + ")")

    def process_client_option(self):
        request = self.receive()["request"]
        option = request["option"]
        response_str = None
        if 1 <= option <= 13:
            print("REQUEST:\tClient " + self.client_name + "(client id = " + str(
                self.client_id) + ") requests for option No." + str(option))

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
                time.sleep(1)
                self.send({"channel_info": self.channel_info})
                print("OPTION_6:\tSend channel info to Client " + self.client_name + "(client id = " + str(
                    self.client_id) + ")")
                self._loop_in_channel()
            elif option == 7:
                response_str = self._option_7_join_an_existing_channel(request)
                response_data = {"response": response_str}
                self.send(response_data)
                time.sleep(1)
                self.send({"channel_info": self.channel_info})
                print("OPTION_7:\tSend channel info to Client " + self.client_name + "(client id = " + str(
                    self.client_id) + ")")
                self._loop_in_channel()
            elif option == 8:
                response_str = self._option_8_create_a_bot(request)
                response_data = {"response": response_str}
                self.send(response_data)
            elif option == 9:
                response_str = self._option_9_map_the_network()
                response_data = {"response": response_str}
                self.send(response_data)
            elif option == 10:
                response_str = self._option_10_link_state()
                response_data = {"response": response_str}
                self.send(response_data)
            elif option == 11:
                response_str = self._option_11_distance_vector()
                response_data = {"response": response_str}
                self.send(response_data)
            elif option == 13:
                self._option_13_disconnect_from_server()
            else:
                response_str = self._option_todo()
                response_data = {"response": response_str}
                self.send(response_data)
        else:
            print("REQUEST:\tClient " + self.client_name + "(client id = " + str(
                self.client_id) + ") requests for an invalid option")

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
        print("OPTION_2:\tSave the private message with timestamp " + str(
            timestamp) + " to server from Client " + self.client_name + "(client id = " + str(self.client_id) + ")")
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
        print("OPTION_3:\tShow unread messages to Client " + self.client_name + "(client id = " + str(
            self.client_id) + ")")

        for key in reading_list:
            self.server.remove_from_message_list(key)

        return response_str

    def _option_4_send_a_direct_msg_via_udp(self, request):
        print("OPTION_4\tClient " + self.client_name + "(client id = " + str(
            self.client_id) + ") sent a direct message to " + request["recipient_address"] + " from " + request[
                  "sender_address"])
        return None

    def _option_5_send_a_broadcast_message(self, request):
        message = request["message"]
        curr_time = datetime.now()
        curr_time_format = curr_time.strftime("%Y-%m-%d %H:%M")
        for client in self.server.get_client_list():
            if client != self.client_id:
                recipient = str(client)
                timestamp = time.time()
                self.server.add_to_message_list(timestamp, curr_time_format, message, recipient, self.client_name,
                                                private=False)
                print("OPTION_5:\tSave the broadcast message with timestamp " + str(
                    timestamp) + " to server from Client " + self.client_name + "(client id = " + str(
                    self.client_id) + ")")
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
                       "General Chat Guidelines:\n" + \
                       "1. Type #bye to exit from this channel. (only for non-admins users)\n" + \
                       "2. Use #<username> to send a private message to that user.\n" + "\n" + \
                       "Waiting for other users to join....\n"
        return response_str

    def _option_7_join_an_existing_channel(self, request):
        channel_id = request["channel_id"]
        self.channel_info = self.server.get_channel_info(channel_id)
        print("OPTION_7:\tGet channel info for Client " + self.client_name + "(client id = " + str(
            self.client_id) + ")")

        admin_name = self.channel_info["admin_name"]
        normal_users = self.channel_info["normal_users"]
        normal_users_str = ""
        for user in normal_users:
            normal_users_str = normal_users_str + user + " "

        member_info_str = None
        if len(normal_users) == 0:
            member_info_str = "#" + admin_name + " is already on the channel.\n"
        else:
            member_info_str = normal_users_str + "#" + admin_name + " are already on the channel.\n"

        self.server.add_user_to_channel(channel_id, self.client_name)
        print("OPTION_7:\tAdd Client " + self.client_name + "(client id = " + str(
            self.client_id) + ") to channel #" + channel_id)

        response_str = "\n----------------------- Channel " + channel_id + " ------------------------\n" + \
                       "\n" + \
                       "All the data in this channel is encrypted\n" + \
                       "\n" + \
                       self.client_name + " just joined\n" + \
                       member_info_str + \
                       admin_name + " is the admin of this channel\n" + \
                       "\n" + \
                       "Chat Guidelines:\n" + \
                       "1. Type #bye to exit from this channel. (only for non-admins users)\n" + \
                       "2. Use #<username> to send a private message to that user.\n" + "\n" + \
                       "\n"
        return response_str

    def _loop_in_channel(self):
        channel_id = self.channel_info["channel_id"]
        exit_data = {"close_channel": "\nChannel " + channel_id + " closed by admin\n"}
        if channel_id not in self.server.channels:
            self.send(exit_data)
            self.channel_info = {}
            return
        is_admin = False
        if self.channel_info["admin_name"] == self.client_name:
            is_admin = True
        has_read_list = []
        # send_to_client_thread = Thread(target=self._channel_send_to_client)
        # receive_from_client_thread = Thread(target=self._channel_receive_from_client, args=(terminate, left))
        # send_to_client_thread.start()
        # receive_from_client_thread.start()
        while True:
            channel_msg_list = self.server.get_channel_msg_list(self.channel_info["channel_id"])
            chat_msg_recv = ""
            for key in channel_msg_list:
                if key not in has_read_list:
                    msg_data = channel_msg_list[key]
                    if msg_data["sender_name"] != self.client_name:
                        if msg_data["receiver_name"] == "channel_public" or msg_data["receiver_name"] == self.client_name:
                            chat_msg_recv += (msg_data["message"] + "\n")
                            print("CHANNEL:\tSend message with timestamp=" + str(
                                key) + " to Client " + self.client_name + "(client id = " + str(self.client_id) + ")")
                            has_read_list.append(key)
            self.send({"chat_msg_recv": chat_msg_recv})

            new_msg = self.receive()["chat_msg_send"]
            sender_name = self.client_name
            receiver_name = "channel_public"
            if len(new_msg) > 0 and new_msg[0] == '#':
                if is_admin and new_msg == "#exit":
                    self.send(exit_data)
                    self.channel_info = {}
                    self.server.terminate_a_channel(channel_id)
                    print("CHANNEL:\tAdmin " + self.client_name + " terminate the channel #" + channel_id)
                    return
                elif not is_admin and new_msg == "#bye":
                    left_msg = self.client_name + " left the channel."
                    timestamp = time.time()
                    msg_data = {"sender_name": sender_name, "receiver_name": receiver_name, "message": left_msg}
                    self.server.add_msg_to_channel(channel_id, timestamp, msg_data)
                    self.send({"close_channel": left_msg})
                    self.channel_info = {}
                    self.server.remove_user_from_channel(channel_id, self.client_name)
                    print("CHANNEL:\tClient " + self.client_name + " left the channel #" + channel_id)
                    return
                else:
                    receiver_name = new_msg.split()[0][1:]
                    new_msg = new_msg[len(receiver_name) + 2:]

            new_msg = sender_name + "> " + new_msg

            timestamp = time.time()
            msg_data = {"sender_name": sender_name, "receiver_name": receiver_name, "message": new_msg}
            self.server.add_msg_to_channel(channel_id, timestamp, msg_data)
            print("CHANNEL:\tAdd message with timestamp=" + str(timestamp) + " to channel #" + channel_id)

    # def _channel_send_to_client(self):
    #     has_read_list = []
    #     while True:
    #         channel_msg_list = self.server.get_channel_msg_list(self.channel_info["channel_id"])
    #         chat_msg_recv = ""
    #         for key in channel_msg_list:
    #             if key not in has_read_list:
    #                 msg_data = channel_msg_list[key]
    #                 if msg_data["sender_name"] != self.client_name:
    #                     if msg_data["receiver_name"] == "channel_public" or msg_data["receiver_name"] == self.client_name:
    #                         chat_msg_recv += (msg_data["message"] + "\n")
    #                         print("CHANNEL:\tSend message with timestamp=" + str(key) + " to Client " + self.client_name + "(client id = " + str(self.client_id) + ")")
    #                         has_read_list.append(key)
    #         self.send({"chat_msg_recv": chat_msg_recv})
    #
    # def _channel_receive_from_client(self, terminate, left):
    #     while True:
    #         new_msg = self.receive()["chat_msg_send"]
    #         sender_name = self.client_name
    #         receiver_name = "channel_public"
    #         # if len(new_msg) > 0 and new_msg[0] == '#':
    #         #     if self.client_id == self.channel_info["admin_id"] and new_msg == "#exit":
    #         #         return
    #         #     elif self.client_id != self.channel_info["admin_id"] and new_msg == "#bye":
    #         #         return
    #         #     else:
    #         #         receiver_name = new_msg.split()[0][1:]
    #         #         new_msg = new_msg[len(receiver_name) + 2:]
    #
    #         # new_msg = sender_name + "> " + new_msg
    #
    #         timestamp = time.time()
    #         msg_data = {"sender_name": sender_name, "receiver_name": receiver_name, "message": new_msg}
    #         self.server.add_msg_to_channel(self.channel_info["channel_id"], timestamp, msg_data)
    #         print("CHANNEL:\tAdd message with timestamp=" + str(timestamp) + " to channel #" + self.channel_info[
    #             "channel_id"])

    def _option_8_create_a_bot(self, request):
        bot_name = request["bot_name"]
        permissions = request["permissions"]
        m = hashlib.md5()
        m.update(bot_name.encode())
        m.update(str(self.client_id).encode())
        token = m.hexdigest()
        self.server.create_a_bot(token, bot_name, self.client_name, permissions)
        print("OPTION_8:\tClient " + self.client_name + "(client id = " + str(self.client_id) + ") create the bot " + bot_name + " with permissions " + permissions)
        response_str = "\n" + bot_name + "'s Configuration:\nToken: " + token + "\nPermissions Enabled: " + permissions + "\nStatus: ready\n"
        return response_str

    def _option_9_map_the_network(self):
        response_str = "\nRouting table requested! Waiting for response....\n\nNetwork Map:\n\n"

        clients, map_info = self.generate_random_map_info()
        print("OPTION_9:\tGenerate random map info for Client " + self.client_name + "(client id = " + str(self.client_id) + "):")

        response_str += self.get_map_str(clients, map_info)

        return response_str

    def generate_random_map_info(self):
        client_list = self.server.get_client_list()
        num_clients = len(client_list)

        clients = [self.client_name]
        for key in client_list:
            if key != self.client_id:
                clients.append(client_list[key])

        map_info = [[-100 for col in range(num_clients)] for row in range(num_clients)]
        for col in range(num_clients):
            for row in range(num_clients):
                if col == row:
                    map_info[row][col] = 0
                elif map_info[col][row] != -100:
                    map_info[row][col] = map_info[col][row]
                else:
                    path_val = random.randint(1, 11)
                    if path_val == 11:
                        map_info[row][col] = '-'
                    else:
                        map_info[row][col] = path_val
        return clients, map_info

    def get_map_str(self, clients, map_info):
        map_str = ""
        row_format = "{:>10}" * (len(clients) + 1)
        map_str += (row_format.format("", *clients) + "\n")
        for client, row in zip(clients, map_info):
            map_str += (row_format.format(client, *row) + "\n")
        return map_str

    def _option_10_link_state(self):
        response_str = "\nRouting table requested! Waiting for response....\n\nNetwork Map:\n\n"

        clients, map_info = self.generate_random_map_info()
        print("OPTION_10:\tGenerate random map info for Client " + self.client_name + "(client id = " + str(
            self.client_id) + "):")

        response_str += self.get_map_str(clients, map_info)

        response_str += "\nRouting table for " + self.client_name + " (id: " + str(self.client_id) + ") computed with Link State Protocol:\n\n"

        response_str += self.link_state_alg(clients, map_info)

        return response_str

    def link_state_alg(self, clients, map_info):
        result_table = [["Destination", "Path", "Cost"]]

        min_cost_dist = self.dijkstra(map_info)
        print("OPTION_10:\tApply link-state alg for Client " + self.client_name + "(client id = " + str(self.client_id) + "):")
        min_cost_dist.pop(0)

        for key in min_cost_dist:
            path = min_cost_dist[key]["path"]
            path_str = "{"
            for i in range(len(path)):
                path_str += clients[path[i]]
                if i < len(path) - 1:
                    path_str += ", "
            path_str += "}"
            cost = min_cost_dist[key]["cost"]
            result_table.append([clients[key], path_str, cost])

        table_str = ""
        for line in result_table:
            table_str += ("{:<15} {:<25} {:<10}".format(line[0], line[1], line[2]) + "\n")
        return table_str

    def dijkstra(self, map_info):
        v_size = len(map_info)
        min_cost_dist = {}
        for i in range(v_size):
            min_cost_dist[i] = {"cost": 10000, "path": []}
        min_cost_dist[0]["cost"] = 0
        visited_set = [False] * v_size

        for i in range(v_size):
            u = self.min_distance(v_size, min_cost_dist, visited_set)
            visited_set[u] = True
            for v in range(v_size):
                if map_info[u][v] != '-' and map_info[u][v] > 0 and visited_set[v] is False and min_cost_dist[v][
                    "cost"] > min_cost_dist[u]["cost"] + map_info[u][v]:
                    min_cost_dist[v]["cost"] = min_cost_dist[u]["cost"] + map_info[u][v]
                    min_cost_dist[v]["path"].append(u)

        for v in range(v_size):
            min_cost_dist[v]["path"].append(v)

        return min_cost_dist

    def min_distance(self, v_size, min_cost_dist, visited_set):
        min = 10000

        for vertex in range(v_size):
            if min_cost_dist[vertex]["cost"] < min and visited_set[vertex] is False:
                min = min_cost_dist[vertex]["cost"]
                min_index = vertex
        return min_index

    def _option_11_distance_vector(self):
        response_str = self._option_9_map_the_network()
        response_str += "\nRouting table computed with Distance Vector Protocol:\n"
        return response_str

    def _option_13_disconnect_from_server(self):
        print("DISCONNECT:\tClient " + self.client_name + "(client id = " + str(self.client_id) + ") disconnected!")
        # remove the client from the client list
        self.server.remove_from_client_list(self.client_id)
        exit(1)

    def _option_todo(self):
        response_str = "OPTION_TODO:\tThe requested option has not been implemented yet"
        print(response_str)
        return response_str

    def send(self, data):
        data = pickle.dumps(data)
        time.sleep(0.2)
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
