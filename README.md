# Python UNIX Socket Server and Client

This project consists of a Python-based server and client using UNIX sockets to communicate. The server provides several utility functions (floor, nroot, reverse, validAnagram, sort) that the client can call.

## Files

- `server_func.py`: Contains the utility functions that the server can execute.
- `server.py`: Implements the server that listens for requests from the client and executes the requested functions.
- `client.py`: Implements the client that sends requests to the server.

## Requirements

- Python 3.x

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. **Run the server**:
    ```bash
    python server.py
    ```

3. **Run the client**:
    ```bash
    python client.py
    ```

## Server Functions

The server supports the following functions:

- `floor(x)`: Returns the largest integer less than or equal to x.
- `nroot(n, x)`: Returns the nth root of x.
- `reverse(s)`: Reverses the given string s.
- `validAnagram(s1, s2)`: Checks if s1 and s2 are anagrams.
- `sort(arr)`: Sorts the given list of strings.

## Example Client Request

The client sends a JSON message to the server. An example request looks like this:
```python
method = "floor"
params = [3.14]

message = {
    "method": method,
    "params": params,
    "id": "1"
}
