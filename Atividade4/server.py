import Pyro5.api
import base64
import time

files = []
clients = {}
interests = {}

@Pyro5.api.expose
class FileServer(object):
    def register_client(self, client_uri):
        clients[client_uri] = set()
        print(f'Cliente conectado - URI: {client_uri}')

    def register_interest(self, file_name, client_uri, validity):
        if file_name not in interests:
            interests[file_name] = set()
        interests[file_name].add((client_uri, time.time() + validity))
        print(f'O cliente da URI {client_uri} deseja o arquivo {file_name}')

    def cancel_interest(self, file_name, client_uri):
        if file_name in interests:
            interests[file_name] = {(uri, valid_until) for uri, valid_until in interests[file_name] if uri != client_uri}
            print(f'Interesse no arquivo {file_name} do cliente {client_uri} foi cancelado.')
        else:
            print("Não foram encontradas solicitações de interesse para este arquivo e cliente.")

    def upload_file(self, file_name, file_data_base64):
        print('Requisição de upload de arquivo!')
        file_data = base64.b64decode(file_data_base64)
        file_obj = {"name": file_name, "data": file_data}
        files.append(file_obj)

        if file_name in interests:
            for interest in interests[file_name].copy():
                client_uri, valid_until = interest
                if time.time() <= valid_until:
                    client = Pyro5.api.Proxy(client_uri)
                    client.notify(f"O arquivo '{file_name}' foi enviado")
                    print(f'Notificação enviada para: {client}')
                    interests[file_name].remove(interest)

    def get_file_info(self):
        print('Solicitação de informações de arquivo')
        files_info = [{"name": file["name"], "size": len(file["data"])} for file in files]
        return files_info
    
    def download_file(self, file_name):
        print('Baixando arquivo solicitado!')
        for file_obj in files:
            if file_obj["name"] == file_name:
                return base64.b64encode(file_obj["data"]).decode('utf-8')
        return None


def start_server():
    daemon = Pyro5.api.Daemon()
    uri = daemon.register(FileServer)
    print(f'Servidor pronto em: {uri}')
    daemon.requestLoop()


if __name__ == "__main__":
    start_server()
