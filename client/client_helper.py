
class ClientHelper:

    def __init__(self, client):
        self.client = client

    # TODO: Implement your ClientHelper for this project
    def print_client_info(self):
        print("Your client info is: \n")
        print("Client Name: " + self.client.get_client_name() + "\n")
        print("Client ID: " + str(self.client.get_client_id()) + "\n")

    def start(self):
        self.print_client_info()
        return
