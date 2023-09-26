# import socket
# import tkinter as tk
# from tkinter import filedialog, messagebox

# def request_shared_files():
#     host = server_ip_entry.get()
#     port = 8080

#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect((host, port))
        
#         s.send('request_files'.encode('utf-8'))
#         file_list = s.recv(1024).decode('utf-8')
        
#         file_listbox.delete(0, tk.END)
#         shared_files = file_list.split("\n")
#         for file in shared_files:
#             file_listbox.insert(tk.END, file)
        
#         s.close()
        
#         status_label.config(text="Received file list")
#     except Exception as e:
#         status_label.config(text=f"Error: {str(e)}")
#         messagebox.showerror("Error", str(e))

# def delete_selected_file():
#     selected_index = file_listbox.curselection()
#     if selected_index:
#         selected_file = file_listbox.get(selected_index[0])
        
#         host = server_ip_entry.get()
#         port = 8080
        
#         try:
#             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             s.connect((host, port))
            
#             s.send(f'delete_file:{selected_file}'.encode('utf-8'))
            
#             s.close()
#             status_label.config(text=f"Deleted file: {selected_file}")
#             file_listbox.delete(selected_index)
#             messagebox.showinfo("Success", f"Deleted file: {selected_file}")
#         except Exception as e:
#             status_label.config(text=f"Error: {str(e)}")
#             messagebox.showerror("Error", str(e))

# root = tk.Tk()
# root.title("Client")
# root.geometry("400x400")

# server_ip_label = tk.Label(root, text="Server IP:")
# server_ip_label.pack()

# server_ip_entry = tk.Entry(root)
# server_ip_entry.pack()

# request_button = tk.Button(root, text="Request Shared Files", command=request_shared_files)
# request_button.pack()

# file_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
# file_listbox.pack()

# delete_button = tk.Button(root, text="Delete Selected File", command=delete_selected_file)
# delete_button.pack()

# status_label = tk.Label(root, text="")
# status_label.pack()

# root.mainloop()

import socket
import tkinter as tk
from tkinter import filedialog, messagebox

def request_shared_files():
    host = server_ip_entry.get()
    port = 8080

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        s.send('request_files'.encode('utf-8'))
        file_list = s.recv(1024).decode('utf-8')
        
        file_listbox.delete(0, tk.END)
        shared_files = file_list.split("\n")
        for file in shared_files:
            file_listbox.insert(tk.END, file)
        
        s.close()
        
        status_label.config(text="Received file list")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        messagebox.showerror("Error", str(e))

def delete_selected_file():
    selected_index = file_listbox.curselection()
    if selected_index:
        selected_file = file_listbox.get(selected_index[0])
        
        host = server_ip_entry.get()
        port = 8080
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            
            s.send(f'delete_file:{selected_file}'.encode('utf-8'))
            
            s.close()
            status_label.config(text=f"Deleted file: {selected_file}")
            file_listbox.delete(selected_index)
            messagebox.showinfo("Success", f"Deleted file: {selected_file}")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

def receive_chat_message():
    host = server_ip_entry.get()
    port = 8080

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        while True:
            message = s.recv(1024).decode('utf-8')
            if message.startswith('chat'):
                chat_message = message.split(':')[1]
                chat_text.insert(tk.END, f"Server: {chat_message}\n")
                chat_text.see(tk.END)
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Client")
root.geometry("450x650+500+200")

server_ip_label = tk.Label(root, text="Server IP:")
server_ip_label.pack()

server_ip_entry = tk.Entry(root)
server_ip_entry.pack()

request_button = tk.Button(root, text="Request Shared Files", command=request_shared_files)
request_button.pack()

file_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
file_listbox.pack()

delete_button = tk.Button(root, text="Delete Selected File", command=delete_selected_file)
delete_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

chat_label = tk.Label(root, text="Chat:")
chat_label.pack()

chat_text = tk.Text(root, height=5, width=40)
chat_text.pack()

chat_entry = tk.Entry(root, width=30)
chat_entry.pack()

receive_chat_button = tk.Button(root, text="Receive Chat", command=receive_chat_message)
receive_chat_button.pack()

root.mainloop()
