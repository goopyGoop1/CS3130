import socket
import Client_Functions ,Server_Function
import argparse, sys,os

filename = "empolyee.txt"



def recvall(sock):
    data = b''
    while True:
        packet = sock.recv(1024)
        if not packet:
            break
        data += packet
        if data.endswith(b'\0'):
            data = data[:-1]  # Remove the delimiter
            break
    return data


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print("Listening at ", sock.getsockname())
    
    while True:
        print("Waiting for a connection...")
        sc, sockname = sock.accept()
        print(f"Connection established with {sockname}")

        try:
            while True:
                message = recvall(sc)  # Use the connected socket
                if not message:
                    print("Client disconnected.")
                    break
                
                decoded_message = message.decode()
                
                
                # Process the message
                Server_Function.process_message(decoded_message, sc)
                
        except Exception as e:
            print(f"Error during communication: {e}")
        finally:
            sc.close()




def client(server_ip, server_port):
    while True:
        try:
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_ip, server_port))
            print(f"Connected to server at {server_ip}:{server_port}")

            client_input = Client_Functions.run()

            if client_input.isdigit():
                option = int(client_input)
                if option == 1:
                    choice = Client_Functions.addNew()
                elif option == 2:
                    choice = Client_Functions.findEmp()
                elif option == 3:
                    choice = Client_Functions.removeEmp()
                elif option == 4:
                    choice = Client_Functions.printDB()
                elif option == 5:
                    print("Exiting Program")
                    sock.sendall(b"5\0")
                    break
                else:
                    print("Invalid option. Try again.")
                    continue

                
                sock.sendall(bytes(choice, 'utf-8') + b'\0')

                
                response = recvall(sock).decode()
                print(f"Server Response: {response}")

        except Exception as e:
            print("Error during communication:", e)
        
        finally:
            
            sock.close()
            print("Connection closed.\n")









if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)