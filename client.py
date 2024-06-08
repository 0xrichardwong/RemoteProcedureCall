# The sys module is a built-in Python module that provides access to some variables
# used or maintained by the interpreter and to functions that interact strongly with the interpreter.
import socket
import sys
import random
import json

method = "validAnagram"
params = ['abc', 'cba']

message = {
    "method": method,
    "params": params,
    "id": "1"
}
json_message = json.dumps(message)
bytes_message = json_message.encode('utf-8')

def main():
    # Create a TCP/IP socket.
    # A socket is an endpoint for sending or receiving data across a computer network.
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Connect the socket to the address where the server is listening.
    server_address = '/tmp/socket_file'
    print('Connecting to {}'.format(server_address))

    # Attempt to connect to the server.
    # If there is an issue, print an error message and exit the program.
    try:
        sock.connect(server_address)
    except socket.error as err:
        print(err)
        # sys.exit() can be used to exit the Python program immediately.
        # The argument 1 indicates that the program exited with an error.
        sys.exit(1)

    # Once connected to the server, send the message.
    try:
        # Define the message to send.
        # Data must be sent in byte format for socket communication.
        sock.sendall(bytes_message)

        # Set a timeout of 2 seconds for the response from the server.
        # If no response is received within this time, the program proceeds to the next step.
        sock.settimeout(2)

        # Wait for a response from the server and display it if received.
        try:
            while True:
                # Receive data from the server.
                # The maximum amount of data to be received at once is 256 bytes.
                data = str(sock.recv(256))

                # If data is received, display it; otherwise, break the loop.
                if data:
                    print('Server response: ' + data)
                else:
                    break

        # If no response is received within 2 seconds, a timeout error occurs, and an error message is displayed.
        except(TimeoutError):
            print('Socket timeout, ending listening for server messages')

    # After all operations are complete, close the socket to end the communication.
    finally:
        print('Closing socket')
        sock.close()

main()
