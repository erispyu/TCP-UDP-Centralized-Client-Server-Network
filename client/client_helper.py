import socket
import pickle


class ClientHelper:

    def __init__(self, client):
        self.client = client
        self.menu_str = None
        self.request_headers = {}
        self.response_headers = {}
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(1)
        self.udp_flag = False

    # TODO: Implement your ClientHelper for this project
    def print_client_info(self):
        print("Your client info is: ")
        print("Client Name: " + self.client.get_client_name())
        print("Client ID: " + str(self.client.get_client_id()) + "\n")

    def cache_menu(self):
        recv_data = self.client.receive()
        menu = recv_data["menu"]
        self.menu_str = menu["menu_str"]
        self.request_headers = menu["request_headers"]
        self.response_headers = menu["response_headers"]
        return

    def process_option(self):
        option_str = input(self.menu_str)
        if option_str in self.request_headers:
            option = int(option_str)
            request_header = self.request_headers[option_str]
            request = {"option": option}
            for key in request_header:
                if key != "option" and key != "udp":
                    request[key] = input(request_header[key])
            self.client.send({"request": request})

            if "udp" in request_header:
                self.udp_socket.bind(self.parse_udp_address(request["sender_address"]))
                self.udp_flag = True
                print(self.response_headers[option_str]["sender_address"] + request["sender_address"])
                message_data = pickle.dumps(request["message"])
                self.udp_socket.sendto(message_data, self.parse_udp_address(request["recipient_address"]))
                print(self.response_headers[option_str]["recipient_address"] + request["recipient_address"] + "\n")

            response_str = self.get_response(option_str)
            if response_str is not None:
                print(response_str)
        else:
            print("ERROR: Invalid option typed in!!!\n")
        return

    def udp_recv(self):
        try:
            recv_data = self.udp_socket.recvfrom(4090)
            if not recv_data:
                return
            message = recv_data[0]
            ip_address, port = recv_data[1]
            print("Receive a direct message from the udp address " + ip_address + ":" + str(port))
            print("Direct Message Content: " + pickle.loads(message) + "\n")
        except socket.timeout:
            return

    def parse_udp_address(self, udp_address):
        split_index = udp_address.index(':')
        ip_addr = udp_address[:split_index]
        port = int(udp_address[split_index + 1:])
        return ip_addr, port

    def get_response(self, option):
        recv_data = self.client.receive()
        return recv_data["response"]

    def run(self):
        self.print_client_info()
        self.cache_menu()

        while True:
            self.process_option()
            if self.udp_flag:
                self.udp_recv()
        return
