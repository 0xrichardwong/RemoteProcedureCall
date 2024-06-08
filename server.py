import socket
import os
import server_func
import json

string_callable = {
    "floor": server_func.floor,
    "nroot": server_func.nroot,
    "reverse": server_func.reverse,
    "validAnagram": server_func.validAnagram,
    "sort": server_func.sort
}

result = {
    "results": "-1",
    "id": "-1"
}

# Request handling function
def handle_request(function_name, params):
    if function_name in string_callable:
        func = string_callable[function_name]
        if function_name == "sort":
            return func(params)  # Pass the whole list as a single parameter
        else:
            return func(*params)  # Unpack parameters for other functions
    else:
        raise ValueError(f"Function {function_name} not found")

# Request handling function 2
def server_response(data_dict):
    result["id"] = data_dict["id"]
    result["results"] = handle_request(data_dict["method"], data_dict["params"])
    return result

def main():
    # Create a UNIX socket in stream mode
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Define the path for the UNIX socket where this server will wait for connections
    server_address = '/tmp/socket_file'

    # Unlink (remove) the server address if it already exists to avoid connection issues
    try:
        os.unlink(server_address)
    except FileNotFoundError:
        pass

    print('Starting up on {}'.format(server_address))

    # Bind the socket to the server address
    sock.bind(server_address)

    # Listen for incoming connections on the socket
    sock.listen(1)

    # Continuously wait for client connections in an infinite loop
    while True:
        # Accept a connection from a client
        connection, client_address = sock.accept()
        try:
            print('Connection from', client_address)

            # Start a loop to keep the server waiting for new data
            while True:
                # Read data from the connection
                # The number 256 specifies the maximum amount of data to be read at once
                data = connection.recv(256)

                # The received data is in binary format, so convert it to a string
                # 'utf-8' is the encoding used for the string
                data_str = data.decode('utf-8')

                # Print the received data
                print('Received ' + data_str)

                # If there is data (i.e., a message from the client), process it
                if data:
                    # Process the received message
                    data_dict = json.loads(data_str)
                    server_response(data_dict)  # Updated to pass data_dict to server_action
                    json_result = json.dumps(result)
                    bytes_result = json_result.encode('utf-8')

                    # Send the processed message back to the client
                    connection.sendall(bytes_result)
                else:
                    # If no data is received from the client, end the loop
                    print('No data from', client_address)
                    break

        # Finally, close the connection
        finally:
            print("Closing current connection")
            connection.close()

main()
