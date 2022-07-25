import socket
import re
import logging
import time

from requests import head

# As a good practise
logging.basicConfig(level=logging.INFO)

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

class InvalidRequestType(Exception):
    """ If user tries to send put, delete, etc."""
    pass

def token_is_valid(token: str):
    return token == "foo"

class Request:
    """ Convinient request class"""
    @classmethod
    def from_headers(cls, headers: list[str]):
        """ to get request from http lines """
        return cls(headers[0].split(" ")[0], re.findall('([^&])=([^&])', headers[-1]))

    def __init__(self, request_type: str, data: list[tuple[str, str]]):
        self.request_type = request_type
        self.data = data

def main(host: str= SERVER_HOST, port: int = SERVER_PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    logging.info('Listening on port %s ...' % port)

    while True:    
        client_connection, _ = server_socket.accept()

        try:
            mess = client_connection.recv(1024).decode()
            headers = mess.split("\n")
            route = headers[0].split()[1]

            def process_request(request: Request, resource_to_be_provided: str):
                """ ad hoc function """
                if request.request_type == 'GET':
                    response = f'HTTP/1.0 200 OK\n\n<h3>Hello, User</h3> Here is your resourse {resource_to_be_provided}'
                elif request.request_type == 'POST':
                    response = f'HTTP/1.0 200 OK\n\n<h3>Hello, User</h3> Here is your resourse {resource_to_be_provided}' \
                        '\n\nYou\'ve sent me this: ' + '&'.join(f'{k}={v}' for k, v in request.data)
                else:
                    raise InvalidRequestType("Only `GET` and `POST` are allowed on this route")
                return response

            # oppurtunity to use switch case here is temptive
            # but I'm not sure if whoever runs this going to use 3.10+
            if route == '/hello':
                # open route
                request = Request.from_headers(headers)
                response = process_request(request, "Unprotected resourse")

            elif route == "/protected_hello":
                # token-access route
                token = [h.split()[1] for h in headers if h.startswith("Authorization:")][0]
                if token_is_valid(token):
                    response = process_request(request, "Protected resourse")
                else:
                    raise FileNotFoundError(f'route {route} is not served')
            else:
                raise FileNotFoundError(f'route {route} is not served')

        except FileNotFoundError as e:
            logging.error(f"Error {e} processing request")
            response = 'HTTP/1.0 404 Whatever you looking for, It does not belong here :('
        except InvalidRequestType as e:
            logging.error(f"Error {e} processing request")
            response = 'HTTP/1.0 400 I don\'t really understand what you\'ve got to do :|'
        except Exception as e:
            logging.error(f"Error {e} processing request")
            response = 'HTTP/1.0 500 Nobody is perfect, right? :)'
        
        client_connection.sendall(response.encode())
        client_connection.close()


if __name__ == "__main__":
    main()