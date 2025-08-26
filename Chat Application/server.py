# server.py
import socket
import threading
import datetime
import os

HOST = "0.0.0.0"   # listen on all interfaces (use server's LAN IP when connecting from another machine)
PORT = 5000

clients = []             # list of active socket objects
usernames = {}           # map socket -> display name
lock = threading.Lock()
HISTORY_FILE = "chat_history.txt"

def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")

def save_history(line):
    # append line to chat_history.txt
    try:
        with lock:
            with open(HISTORY_FILE, "a", encoding="utf-8") as f:
                f.write(line + "\n")
    except Exception:
        pass

def send_to_client(client, text):
    try:
        client.sendall(text.encode("utf-8"))
    except Exception:
        remove_client(client)

def broadcast(text, exclude_client=None):
    line = f"[{timestamp()}] {text}"
    save_history(line)
    with lock:
        for c in list(clients):
            if c is exclude_client:
                continue
            try:
                c.sendall(line.encode("utf-8"))
            except Exception:
                remove_client(c)

def remove_client(client):
    with lock:
        if client in clients:
            name = usernames.get(client)
            try:
                clients.remove(client)
            except ValueError:
                pass
            usernames.pop(client, None)
            try:
                client.close()
            except Exception:
                pass
            if name:
                broadcast(f"{name} has left the chat.")

def handle_client(conn, addr):
    try:
        # Expect the first message from client to be the display name
        conn.settimeout(30)  # if the client does not send name in 30s, drop
        raw = conn.recv(1024)
        if not raw:
            conn.close()
            return
        name = raw.decode("utf-8", errors="ignore").strip()
        if not name:
            name = f"User{addr[1]}"
        conn.settimeout(None)

        with lock:
            clients.append(conn)
            usernames[conn] = name

        # Welcome message for the new user
        send_to_client(conn, f"Welcome {name}! Commands: /users  /pm <name> <msg>  /quit\n")

        # Announce join to others
        broadcast(f"{name} has joined the chat.", exclude_client=conn)

        # Receive loop
        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode("utf-8", errors="ignore").strip()
            if not text:
                continue

            # Commands
            if text.lower().startswith("/quit"):
                send_to_client(conn, "Goodbye!\n")
                remove_client(conn)
                break

            elif text.strip() == "/users":
                with lock:
                    online = ", ".join(usernames.values()) if usernames else "No users"
                send_to_client(conn, f"Online users: {online}\n")

            elif text.startswith("/pm "):
                # format: /pm targetName message...
                parts = text.split(" ", 2)
                if len(parts) < 3:
                    send_to_client(conn, "Usage: /pm <username> <message>\n")
                else:
                    target_name = parts[1]
                    private_msg = parts[2]
                    sent = False
                    with lock:
                        for c, uname in usernames.items():
                            if uname == target_name:
                                try:
                                    c.sendall(f"[{timestamp()}] [PM from {usernames.get(conn)}] {private_msg}".encode("utf-8"))
                                    sent = True
                                except Exception:
                                    remove_client(c)
                                break
                    if not sent:
                        send_to_client(conn, f"User '{target_name}' not found or offline.\n")

            else:
                broadcast(f"{name}: {text}", exclude_client=conn)

    except Exception:
        # On any exception, ensure client is removed
        remove_client(conn)

def main():
    # ensure history file exists
    if not os.path.exists(HISTORY_FILE):
        open(HISTORY_FILE, "a", encoding="utf-8").close()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"Server started on {HOST}:{PORT}  (use 127.0.0.1 if connecting from same machine)")

    try:
        while True:
            conn, addr = server.accept()
            print(f"New connection from {addr}")
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        with lock:
            for c in clients:
                try:
                    c.close()
                except:
                    pass
        server.close()

if __name__ == "__main__":
    main()
