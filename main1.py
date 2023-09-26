import os
import socket
import tkinter as tk
from tkinter import filedialog, messagebox

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server")
        self.root.geometry("400x200")

        self.filename = ""

        self.start_button = tk.Button(root, text="Start Server", command=self.start_server)
        self.start_button.pack()

        self.select_file_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_file_button.pack()

        self.file_label = tk.Label(root, text="Selected File: None")
        self.file_label.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

    def start_server(self):
        host = socket.gethostname()
        port = 8080

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)

        self.status_label.config(text=f"Server is running on {host}:{port}")

        conn, addr = s.accept()
        file_size = os.path.getsize(self.filename)
        conn.send(str(file_size).encode('utf-8'))
        with open(self.filename, 'rb') as file:
            data = file.read(1024)
            while data:
                conn.send(data)
                data = file.read(1024)
        conn.close()
        self.status_label.config(text="File sent successfully")

    def select_file(self):
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), 
                                                  title='Select File to Send', 
                                                  filetypes=(('All files', '*.*'),))
        self.file_label.config(text=f"Selected File: {os.path.basename(self.filename)}")

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client")
        self.root.geometry("400x200")

        self.server_ip_label = tk.Label(root, text="Server IP:")
        self.server_ip_label.pack()

        self.server_ip_entry = tk.Entry(root)
        self.server_ip_entry.pack()

        self.receive_button = tk.Button(root, text="Receive File", command=self.receive_file)
        self.receive_button.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

    def receive_file(self):
        host = self.server_ip_entry.get()
        port = 8080

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, port))
            file_size = int(s.recv(1024).decode('utf-8'))
            received_data = b""
            while len(received_data) < file_size:
                data = s.recv(1024)
                if not data:
                    break
                received_data += data
            filename = filedialog.asksaveasfilename(defaultextension=".*", filetypes=[("All Files", "*.*")])
            with open(filename, 'wb') as file:
                file.write(received_data)
            self.status_label.config(text="File received successfully")
            messagebox.showinfo("Success", "File received successfully")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        finally:
            s.close()

if __name__ == "__main__":
    root = tk.Tk()

    server_app = ServerApp(root)
    client_app = ClientApp(root)

    root.mainloop()