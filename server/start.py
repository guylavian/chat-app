import subprocess
import os


def start_backend():
    server_path = os.path.join(os.path.dirname(__file__), "src", "server.py")
    print(f"Starting backend server from: {server_path}")

    # Use python3 instead of python
    subprocess.run(["python3", server_path])


if __name__ == "__main__":
    start_backend()
