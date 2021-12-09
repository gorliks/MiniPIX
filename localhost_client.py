import sys, time, logging
import socket

class LocalHostClient():
    def __init__(self):
        self.HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        self.PORT = 8080
        self.received_data = ""

    def send_message_to_server(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.connect((self.HOST, self.PORT))
            server.sendall(bytes(message, 'utf-8'))
            received_data = server.recv(2048)
            print('Received', repr(received_data))
            if message == 'EXIT':
                print('Here be exiting routines')

            self.response = str(received_data)
            self.response = self.response[2:-1] #remove b'..' bytes from the string beginning and ' from the end

    def get_response(self):
        return self.response
