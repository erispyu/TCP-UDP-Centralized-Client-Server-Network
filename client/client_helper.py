class ClientHelper:

    def __init__(self, client):
        self.client = client
        self.menu_str = None
        self.request_headers = {}
        self.response_headers = {}

    # TODO: Implement your ClientHelper for this project
    def print_client_info(self):
        print("Your client info is: ")
        print("Client Name: " + self.client.get_client_name())
        print("Client ID: " + str(self.client.get_client_id()))

    def cache_menu(self):
        recv_data = self.client.receive()
        menu = recv_data["menu"]
        self.menu_str = menu["menu_str"]
        self.request_headers = menu["request_headers"]
        self.response_headers = menu["response_headers"]
        return

    def process_option(self):
        option = input(self.menu_str)
        if option in self.request_headers:
            request_header = self.request_headers[option]
            request = {"option": request_header["option"]}
            for key in request_header:
                if key != "option":
                    request[key] = input(request_header[key])
            self.client.send({"request": request})

            print(self.get_response(option))
        else:
            print("ERROR: Invalid option typed in!!!\n")
        return

    def get_response(self, option):
        recv_data = self.client.receive()
        return recv_data["response"]

    def run(self):
        self.print_client_info()
        self.cache_menu()

        while True:
            self.process_option()
        return
