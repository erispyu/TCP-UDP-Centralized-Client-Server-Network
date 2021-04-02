class ClientHelper:

    def __init__(self, client, server_ip, server_port):
        self.client = client
        self.server_ip = server_ip
        self.server_port = server_port
        student_name = 'Zhuofu Liu'  # TODO: your name
        student_id = 920673504  # TODO: your student id
        github_username = 'zhuofu0513'  # TODO: your github username

    def create_request(self, name, id, github_username):
        """
        TODO: create request with a Python dictionary to save the parameters given in this function
              the keys of the dictionary should be 'student_name', 'github_username', and
              'sid'.
        :return: the request created
        """
        request = {'student_name': name, 'github_username': github_username, 'sid': id}
        return request

    def send_request(self, request):
        """
        TODO: send the request passed as a parameter
        :request: a request representing data deserialized data.
        """
        self.client.send(request)

    def process_response(self):
        """
        TODO: process a response from the server
              Note the response must be received and deserialized before being processed.
        :response: the serialized response.
        """
        deserialized_data = self.client.receive()
        return deserialized_data

    def start(self):
        """
        TODO: create a request with your student info using the self.request(....) method
              send the request to the server, and then process the response sent from the server.
        """
        request = self.create_request('Zhuofu Liu', 920673504, 'zhuofu0513')
        self.send_request(request)
        response = self.process_response()
        print('{} has successfully connected to {}/{}'.format(response, self.server_ip, self.server_port))
