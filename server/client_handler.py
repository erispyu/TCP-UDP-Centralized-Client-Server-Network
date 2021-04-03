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
        print("Client " + self.client_name + "(client id = " + str(self.client_id) + ") has successfully connected to the server.")

    def send_menu(self):
        time.sleep(1)
        menu_data = {"menu": self.menu.get(self=self.menu)}
        self.send(menu_data)
        print("Send menu to Client " + self.client_name + "(client id = " + str(self.client_id) + ")")

    def receive_option(self):
        option = self.receive()["option"]

        return option

    def process_client_option(self):
        option = self.receive_option()
        if 1 <= option <= 12:
            print("Client " + self.client_name + "(client id = " + str(self.client_id) + ") requests for option No." + str(option))
        else:
            print("Client " + self.client_name + "(client id = " + str(self.client_id) + ") requests for an invalid option")

    def send(self, data):
        data = pickle.dumps(data)
        self.client_socket.send(data)

    def receive(self):
        data = self.client_socket.recv(4090)
        return pickle.loads(data)

    def run(self):
        self.process_client_info()
        self.send_menu()
        while True:
            self.process_client_option()
        return
