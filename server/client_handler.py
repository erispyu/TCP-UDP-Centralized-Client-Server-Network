import pickle
import time

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
        print("OPTION_1:\tSend user list to Client " + self.client_name + "(client id = " + str(self.client_id) + "):")
        print(response_str)
        return response_str

    def _option_2_send_a_message(self, request):
        message = request["message"]
        recipient = request["recipient"]
        # TO DO: Save message on server with timestamp
        response_str = "Message sent!"
        print("OPTION_2:\tSave the message to server")
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
