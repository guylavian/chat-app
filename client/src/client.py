import socket
import threading

# Client setup
HOST = '127.0.0.1'
PORT = 9002

def receive_messages(client_socket):
    """Thread to handle incoming messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print("\n" + message)
            else:
                break  # Server closed connection
        except Exception as e:
            print(f"[ERROR] Connection lost: {e}")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Send the user's name to the server
    name = input("Enter your name: ")
    client_socket.sendall(name.encode('utf-8'))

    # Start a thread to handle receiving messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    print("To start chatting, enter the recipient's name.")

    while True:
        try:
            # Input loop for user commands and messages
            if not hasattr(start_client, "recipient_set") or not start_client.recipient_set:
                # Ask for the recipient name if not already set
                recipient_name = input("Enter recipient's name: ")
                client_socket.sendall(recipient_name.encode('utf-8'))
                start_client.recipient_set = True  # Flag to track recipient set
            else:
                # Send a message to the recipient
                message = input("You: ")
                client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")
            client_socket.close()
            break

if __name__ == "__main__":
    start_client()