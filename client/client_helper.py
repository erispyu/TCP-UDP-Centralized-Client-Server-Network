
class ClientHelper:

    def __init__(self, client):
        self.client = client
        self.menu = None

    # TODO: Implement your ClientHelper for this project
    def print_client_info(self):
        print("Your client info is: ")
        print("Client Name: " + self.client.get_client_name())
        print("Client ID: " + str(self.client.get_client_id()))

    def cache_menu(self):
        recv_data = self.client.receive()
        self.menu = recv_data["menu"]
        return

    def send_option(self):
        option = int(input(self.menu))
        self.client.send({"option": option})
        return

    def get_response(self):
        recv_data = self.client.receive()
        return recv_data["response"]

    def run(self):
        self.print_client_info()
        self.cache_menu()

        while True:
            self.send_option()
            response = self.get_response()
            print(response)
        return
