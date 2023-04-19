import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)

def parse_command(command): # this functions goes to utils
    # command = "key1=val1 key2=val2"
    #command = dict(s.split("=") for s in command.split()) #{'key': 'val', 'key2': 'val2'}
    try:
        parsed = dict((key, value) for key, value in [i.split('=') for i in command.split()])
    except:
        print('No keywords, using command as a string')
        parsed = str(command)
    return parsed

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', PORT))
server.listen(1)


while True:
    conn, addr = server.accept()
    data = conn.recv(2048)
    message = str(data)
    message = message[2:-1]
    print('Received ', message)
    parsed = parse_command(message)
    print( parsed )
    #if not data:
    #    break
    if 'EXIT' in message:
        print('Exiting..')
        break
    conn.sendall(data)



# conn, addr = server.accept()
# with conn:
#     print('Connected by', addr)
#     while True:
#         data = conn.recv(1024)
#         message = str(data)
#         print('Received ', message)
#         #if not data:
#         #    break
#         if 'EXIT' in message:
#             print('Exiting..')
#             break
#         conn.sendall(data)
