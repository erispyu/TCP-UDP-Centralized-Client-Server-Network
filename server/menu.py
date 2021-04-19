#######################################################################################
# File:             menu.py
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# IMPORTANT:        This file can only resides on the server side.
# Usage :           menu = Menu() # creates object
#
########################################################################################

class Menu:
    """
    IMPORTANT MUST READ: The Menu class is the user interface that acts as a communication bridge between the user
    and the Client-Server architecture of this application. The Menu is always located on the Server side (machine running the server).
    However, it must be printed on the Client console by the ClientHelper object. In order to accomplish this, students
    must create a
    """

    @staticmethod
    def get(self):
        """
        TODO: shows the following menu on the client side
        ****** TCP/UDP Network ******
        ------------------------------------
        Options Available:
        1.  Get users list
        2.  Send a message
        3.  Get my messages
        4.  Send a direct message with UDP protocol
        5.  Broadcast a message with CDMA protocol
        6.  Create a secure channel to chat with your friends using PGP protocol
        7.  Join an existing channel
        8.  Create a Bot to manage a future channel
        9.  Get the Routing Table of this client with Link State Protocol
        10. Get the Routing Table of this network with Distance Vector Protocol
        11. Turn web proxy server on (extra-credit)
        12. Disconnect from server

        Your option <enter a number>:
        """
        menu = "****** TCP/UDP Network ******\n" \
               "------------------------------------\n" \
               "Options Available:\n" \
               "1.  Get users list\n" \
               "2.  Send a message\n" \
               "3.  Get my messages\n" \
               "4.  Send a direct message with UDP protocol\n" \
               "5.  Broadcast a message with CDMA protocol\n" \
               "6.  Create a secure channel to chat with your friends using PGP protocol\n" \
               "7.  Join an existing channel\n" \
               "8.  Create a Bot to manage a future channel\n" \
               "9.  Map the network\n" \
               "10.  Get the Routing Table of this client with Link State Protocol\n" \
               "11. Get the Routing Table of this network with Distance Vector Protocol\n" \
               "12. Turn web proxy server on (extra-credit)\n" \
               "13. Disconnect from server\n" \
               "\n" \
               "Your option <enter a number>: "
        # your code here
        return menu

    @staticmethod
    def option(self):
        """
        TODO: Ask the user to select an option from the menu
              Note. you must handle exceptions for options chosen that are not in the allowed range
        :return: an integer representing the option chosen by the user from the menu
        """
        option = 0
        return option

    @staticmethod
    def request_headers(self):
        """
        TODO: In this method students implement the headers of the menu. That's it, the options the server expect
              for each requests from the client related to this menu. For example, the headers for option 2,
              the expected headers in a client request are {'option':<integer>, 'message':<string>, 'recipient':<integer>}
        """
        headers = {
            "1": {"option": 1},
            "2": {"option": 2, "message": "Enter your message: ", "recipient": "Enter recipient id: "},
            "3": {"option": 3},
            "4": {"option": 4,
                  "udp": None,
                  "sender_address": "Enter the address to bind your UDP client (e.g 127.0.0.1:6000): ",
                  "recipient_address": "Enter the recipient address: ",
                  "message": "Enter the message: "},
            "5": {"option": 5, "message": "Enter the message: "},
            "6": {"option": 6, "channel_id": "Enter the channel id: ", "channel": None},
            "7": {"option": 7, "channel_id": "Enter channel id you'd like to join: "}
        }
        return headers

    @staticmethod
    def response_headers(self):
        """
        TODO: In this method students implement the headers of the menu. That's it, the options the server sends to
              the client for each response related to this menu. For example, the headers for the response of option 3
              are {'option':<integer>, 'messages':<Python Dictionary>}
        """
        headers = {
            "1": {"option": 1, "response_str": None},
            "4": {"option": 1, "sender_address": "UDP client running and accepting other clients at udp address ", "recipient_address": "Message sent to udp address: "}
        }
        return headers

    walsh_transform_1 = [1, 1, 1, 1, 1, 1, 1, 1]
    walsh_transform_2 = [1, 1, 1, 1, -1, -1, -1, -1]
