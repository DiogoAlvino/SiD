import Pyro5.api as pyro
import base64
import os
import tkinter as Tk
from tkinter import *
from tkinter import ttk

@pyro.expose
class Client(object):
    def notify(self, message):
        print(f"Notificação recebida: {message}")

    def express_interest(self, file_name, validity_period, file_server):
        file_server.register_interest(file_name, self.uri, validity_period)

    def cancel_interest(self, file_name, file_server):
        file_server.cancel_interest(file_name, self.uri)

    def download_file(self, file_name, file_server):
        file_data_base64 = file_server.download_file(file_name)
        if file_data_base64 is not None:
            file_data = base64.b64decode(file_data_base64)
            with open(file_name, 'wb') as f:
                f.write(file_data)
            print(f'"{file_name}" baixado com sucesso')
        else:
            print(f'O arquivo "{file_name}" não existe no servidor')

def start_client(file_server_uri):
    daemon = pyro.Daemon()
    client = Client()
    client.uri = daemon.register(client)
    file_server = pyro.Proxy(file_server_uri)
    file_server.register_client(client.uri)

    def upload_file_to_server():
        file_name = entry_file_name.get()
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                file_data = f.read()
            file_data_base64 = base64.b64encode(file_data).decode('utf-8')
            file_server.upload_file(file_name, file_data_base64)
            print(f'"{file_name}" enviado com sucesso')
        else:
            print(f'O arquivo "{file_name}" não existe')

    def register_interest():
        file_interest = entry_file_name.get()
        validity_period = 60 * 60 * 2  # default to 2 hours
        client.express_interest(file_interest, validity_period, file_server)
        print(f'Interesse no arquivo: {file_interest} foi marcado')

    def unregister_interest():
        file_interest = entry_file_name.get()
        client.cancel_interest(file_interest, file_server)
        print(f'Interesse no arquivo: {file_interest} foi cancelado')

    def download_file_from_server():
        file_name = entry_file_name.get()
        client.download_file(file_name, file_server)

    def view_files_list():
        files_info = file_server.get_file_info()
        file_names = [file['name'] for file in files_info]
        
        list_window = Toplevel(gui)
        list_window.title("Lista de Arquivos")
        
        listbox = Listbox(list_window)
        for file_name in file_names:
            listbox.insert(END, file_name)
        listbox.pack()

    gui = Tk(className='Cliente')
    gui.geometry("500x500")
    gui.config(bg="lightblue")

    frame = Frame(gui, bg="lightblue")
    frame.pack(expand=True)

    Label(frame, text="Nome do arquivo:", font=("Arial", 14), bg="lightblue").pack()
    entry_file_name = Entry(frame, font=("Arial", 14))
    entry_file_name.pack()

    Button(frame, text="Fazer upload", command=upload_file_to_server, font=("Arial", 14), bg="yellow").pack()
    Button(frame, text="Registrar interesse", command=register_interest, font=("Arial", 14), bg="yellow").pack()
    Button(frame, text="Cancelar interesse", command=unregister_interest, font=("Arial", 14), bg="yellow").pack()
    Button(frame, text="Baixar arquivo", command=download_file_from_server, font=("Arial", 14), bg="yellow").pack()
    Button(frame, text="Visualizar Lista de Arquivos", command=view_files_list, font=("Arial", 14), bg="yellow").pack()

    gui.mainloop()

    daemon.requestLoop()

if __name__ == "__main__":
    file_server_uri = input("Insira o URI do servidor de arquivos: ")
    start_client(file_server_uri)