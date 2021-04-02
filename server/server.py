# don't modify this imports.
import socket
from threading import Thread
from clienthandler import ClientHandler


class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10  # keeps 10 clients in queue

    def __init__(self, host="127.0.0.1", port=12000):
        """
        TODO: copy and paste your implementation from lab 3 for self.server socket property
        """
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # your implementation for this socket here
        self.handlers = {}  # initializes client_handlers list

    def _bind(self):
        """
        TODO: copy and paste your implementation from lab 3
        :return: VOID
        """
        self.serversocket.bind((self.host, self.port))

    def _listen(self):
        """
        TODO: copy and paste your implementation from lab 3
        :return: VOID
        """
        try:
            self._bind()
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Listening at " + str(self.host) + "/" + str(self.port))
        except:
            self.serversocket.close()

    def _accept_clients(self):
        """
        #TODO: Modify your implementation from lab 3, so now the
               server can support multiple clients pipelined.
               HINT: you must thread the handler(...) method
        :return: VOID
        """
        while True:
            try:
                clienthandler, addr = self.serversocket.accept()
                Thread(target=self._handler, args=(clienthandler, addr)).start()  # client thread started
            except:
                print("ERROR occurred 1")

    def _handler(self, clienthandler, addr):
        """
        TODO: create an object of the ClientHandler.
              see the clienthandler.py file to see
              the parameters that must be passed into
              the ClientHandler's constructor to create
              the object.
              Once the ClientHandler object is created,
              add it to the dictionary of client handlers initialized
              on the Server constructor (self.handlers)
        :clienthandler: the clienthandler child process that the server creates when a client is accepted
        :addr: the addr list of server parameters created by the server when a client is accepted.
        """
        clienthandler = ClientHandler(self, clienthandler, addr)
        client_id = addr[1]
        clienthandler.run()
        self.handlers[client_id] = clienthandler

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._listen()
        self._accept_clients()


# main execution
if __name__ == '__main__':
    server = Server()
    server.run()
