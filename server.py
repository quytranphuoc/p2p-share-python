
# import socket
# import threading
# import os
# import tkinter as tk
# from tkinter import filedialog, messagebox

# connected_clients = []
# shared_files = []

# def start_server():
#     host = socket.gethostname()
#     port = 8080

#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((host, port))
#     s.listen(5)

#     status_label.config(text=f"Server is running on {host}:{port}")

#     while True:
#         conn, addr = s.accept()
#         connected_clients.append(conn)
#         thread = threading.Thread(target=handle_client, args=(conn,))
#         thread.start()

# def handle_client(conn):
#     try:
#         while True:
#             message = conn.recv(1024).decode('utf-8')
#             if message == 'request_files':
#                 send_shared_files(conn)
#             elif message.startswith('send_file'):
#                 filename = message.split(':')[1]
#                 send_file_to_client(filename, conn)
#     except Exception as e:
#         print(f"Error: {str(e)}")
#     finally:
#         conn.close()
#         connected_clients.remove(conn)

# def send_shared_files(conn):
#     file_list = "\n".join(shared_files)
#     conn.send(file_list.encode('utf-8'))

# def send_file_to_client(filename, conn):
#     try:
#         with open(filename, 'rb') as file:
#             data = file.read(1024)
#             while data:
#                 conn.send(data)
#                 data = file.read(1024)
#     except Exception as e:
#         print(f"Error: {str(e)}")

# def share_file():
#     global filename
#     filename = filedialog.askopenfilename(initialdir=os.getcwd(), 
#                                           title='Select File to Share', 
#                                           filetypes=(('All files', '*.*'),))
#     shared_files.append(os.path.basename(filename))
#     status_label.config(text=f"Shared File: {os.path.basename(filename)}")

# root = tk.Tk()
# root.title("Server")
# root.geometry("400x300")

# filename = ""

# start_button = tk.Button(root, text="Start Server", command=start_server)
# start_button.pack()

# share_button = tk.Button(root, text="Share File", command=share_file)
# share_button.pack()

# status_label = tk.Label(root, text="")
# status_label.pack()

# root.mainloop()
import socket
import threading
import os
import tkinter as tk
from tkinter import filedialog, messagebox

connected_clients = []
shared_files = []
chat_messages = []

def start_server():
    host = socket.gethostname()
    port = 8080

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)
    except socket.error as e:
        print(e)
        sys.exit(1)

    status_label.config(text=f"Server is running on {host}:{port}")

    while True:
        conn, addr = s.accept()
        connected_clients.append(conn)
        try:
            thread = threading.Thread(target=handle_client, args=(conn,))
            thread.start()
        except Exception as e:
            print(e)
            conn.close()

def handle_client(conn):
    try:
        while True:
            message = conn.recv(1024).decode('utf-8')
            if message == 'request_files':
                send_shared_files(conn)
            elif message.startswith('send_file'):
                filename = message.split(':')[1]
                send_file_to_client(filename, conn)
            elif message.startswith('chat'):
                chat_message = message.split(':')[1]
                chat_messages.append(chat_message)
                broadcast_chat_message(chat_message)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        conn.close()
        connected_clients.remove(conn)

def send_shared_files(conn):
    file_list = "\n".join(shared_files)
    conn.send(file_list.encode('utf-8'))

def send_file_to_client(filename, conn):
    try:
        with open(filename, 'rb') as file:
            data = file.read(1024)
            while data:
                conn.send(data)
                data = file.read(1024)
    except Exception as e:
        print(f"Error: {str(e)}")

def broadcast_chat_message(message):
    for client_conn in connected_clients:
        try:
            client_conn.send(f'chat:{message}'.encode('utf-8'))
        except Exception as e:
            print(f"Error: {str(e)}")

def share_file():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), 
                                          title='Select File to Share', 
                                          filetypes=(('All files', '*.*'),))
    shared_files.append(os.path.basename(filename))
    status_label.config(text=f"Shared File: {os.path.basename(filename)}")

root = tk.Tk()
root.title("Server")
root.geometry("450x650+500+200")
root.configure(bg="#f4fdfe")
root.readprofile(False,False)

filename = ""

start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.pack()

share_button = tk.Button(root, text="Share File", command=share_file)
share_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

chat_label = tk.Label(root, text="Chat:")
chat_label.pack()

chat_text = tk.Text(root, height=5, width=40)
chat_text.pack()

def send_chat_message():
    message = chat_entry.get()
    chat_messages.append(message)
    chat_text.insert(tk.END, f"You: {message}\n")
    chat_text.see(tk.END)
    chat_entry.delete(0, tk.END)
    broadcast_chat_message(message)

chat_entry = tk.Entry(root, width=30)
chat_entry.pack()

send_chat_button = tk.Button(root, text="Send", command=send_chat_message)
send_chat_button.pack()

root.mainloop()
