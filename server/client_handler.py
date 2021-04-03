import pickle

class ClientHandler:

    def __init__(self, server_instance, client_socket, addr):
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.client_socket = client_socket

        self.client_name = None

    # TODO: implement the ClientHandler for this project.

    def get_client_id(self):
        return self.client_id

    def get_client_name(self):
        return self.client_name

    def process_client_info(self):
        while True:
            client_info = pickle.loads(self.client_socket.recv(4096))
            if not client_info:
                print("No client info")
                break;
            else:
                self.client_name = client_info["client_name"]
                self.client_id = client_info["client_id"]
                print("Client " + self.client_name + "(client id = " + str(self.client_id) + ") has successfully connected to the server.")

    def run(self):
        self.process_client_info()
        return
