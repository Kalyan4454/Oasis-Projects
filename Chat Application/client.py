# client.py
import socket
import threading
import sys

DEFAULT_SERVER = "127.0.0.1"
DEFAULT_PORT = 5000

def receive_loop(sock):
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("\n[Disconnected from server]")
                break
            print(data.decode("utf-8", errors="ignore"))
    except Exception as e:
        print("\n[Connection closed]", e)
    finally:
        try:
            sock.close()
        except:
            pass
        os._exit(0)

def main():
    server = input(f"Server IP (default {DEFAULT_SERVER}): ").strip() or DEFAULT_SERVER
    port_input = input(f"Server port (default {DEFAULT_PORT}): ").strip()
    try:
        port = int(port_input) if port_input else DEFAULT_PORT
    except ValueError:
        print("Invalid port. Using default.")
        port = DEFAULT_PORT

    display_name = input("Choose a display name: ").strip()
    if not display_name:
        print("Display name required. Exiting.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server, port))
    except Exception as e:
        print("Could not connect to server:", e)
        return

    # send display name as the first message
    try:
        sock.sendall(display_name.encode("utf-8"))
    except Exception as e:
        print("Failed to send display name:", e)
        sock.close()
        return

    # start receiver thread
    thread = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
    thread.start()

    try:
        while True:
            msg = input()
            if not msg:
                continue
            try:
                sock.sendall(msg.encode("utf-8"))
            except Exception:
                print("Failed to send. Connection might be closed.")
                break
            if msg.lower().startswith("/quit"):
                break
    except KeyboardInterrupt:
        try:
            sock.sendall("/quit".encode("utf-8"))
        except:
            pass
    finally:
        try:
            sock.close()
        except:
            pass

if __name__ == "__main__":
    main()
