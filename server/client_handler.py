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
        menu_data = {"menu": self.menu.get(self=self.menu)}
        self.send(menu_data)
        print("CONNECT:\tSend menu to Client " + self.client_name + "(client id = " + str(self.client_id) + ")")

    def receive_option(self):
        option = self.receive()["option"]
        return option

    def process_client_option(self):
        option = self.receive_option()
        if 1 <= option <= 12:
            print("REQUEST:\tClient " + self.client_name + "(client id = " + str(self.client_id) + ") requests for option No." + str(option))
            if option == 1:
                self._option_1_send_user_list()
            else:
                self._option_todo()
        else:
            print("REQUEST:\tClient " + self.client_name + "(client id = " + str(self.client_id) + ") requests for an invalid option")

    def _option_1_send_user_list(self):
        client_list = self.server.get_client_list()
        num_clients = len(client_list)
        cnt = 0
        response = "User connected: " + str(num_clients) + "\n"
        for i in client_list:
            response += (client_list[i] + ":" + str(i))
            cnt += 1
            if cnt < num_clients:
                response += ", "
        time.sleep(1)
        response_data = {"response": response}
        self.send(response_data)
        print("RESPONSE:\tSend user list to Client " + self.client_name + "(client id = " + str(self.client_id) + "):")
        print(response)

    def _option_todo(self):
        response = "RESPONSE:\tThe requested option has not been implemented yet"
        time.sleep(1)
        response_data = {"response": response}
        self.send(response_data)
        print(response)

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
