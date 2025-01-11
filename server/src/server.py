import socket
import threading

# Server setup
HOST = '127.0.0.1'
PORT = 9002

clients = {}  # {name: socket}
active_chats = {}  # {sender: recipient}


def handle_client(client_socket):
    # Receive client's name
    name = client_socket.recv(1024).decode('utf-8')
    clients[name] = client_socket
    print(f"[NEW CONNECTION] {name} connected.")

    try:
        while True:
            # If not in active chat, ask for recipient
            if name not in active_chats:
                recipient_name = client_socket.recv(1024).decode('utf-8')
                if recipient_name not in clients:
                    client_socket.sendall(f"[ERROR] {recipient_name} is not connected.".encode('utf-8'))
                    continue

                # Register bi-directional chat session immediately
                active_chats[name] = recipient_name
                if recipient_name not in active_chats:
                    active_chats[recipient_name] = name  # Ensure Bob also sees Alice as active

                # Notify the recipient about the new chat session
                recipient_socket = clients[recipient_name]
                recipient_socket.sendall(f"[INFO] {name} wants to start a chat with you. Respond to {name} with their name to start.".encode('utf-8'))

            # Forward messages based on active_chats
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # Exit loop if the client disconnects

            if name in active_chats:
                recipient_name = active_chats[name]
                if recipient_name in clients:  # Check if the recipient is still connected
                    recipient_socket = clients[recipient_name]
                    print(f"[{name} -> {recipient_name}] {message}")
                    recipient_socket.sendall(f"{name}: {message}".encode('utf-8'))
                else:
                    # Handle case where recipient disconnects
                    client_socket.sendall(f"[ERROR] {recipient_name} is no longer connected.".encode('utf-8'))
                    # Clean up the active session
                    del active_chats[name]
                    if recipient_name in active_chats:
                        del active_chats[recipient_name]
            else:
                client_socket.sendall("[ERROR] No active chat session. Start a new chat.".encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] {name} disconnected. Error: {e}")
    finally:
        print(f"[DISCONNECT] {name} disconnected.")
        del clients[name]
        if name in active_chats:
            # Remove the bi-directional session
            recipient_name = active_chats[name]
            del active_chats[name]
            if recipient_name in active_chats:
                del active_chats[recipient_name]
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)  # Allow multiple connections
    print(f"[LISTENING] Server is running on {HOST}:{PORT}")

    while True:
        client_socket, _ = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()