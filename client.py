import socket
import time as t

class Client():
    def __init__(self):
        self.client = None
        self.address = None
        self.port = None
        self.user = None
        self.passwd = None

    def getConn(self, addr, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = addr
        self.port = port
        self.client.connect((addr, port))

    def authClient(self, existing, user, passwd):
        # send request to authenticate (true for existing user, false for new)
        # get response saying okay, we are now able to send creds. (if something is wrong server-side, cant auth.) 
        # send creds
        # get response saying authenticated, or wrong pass. Or, if new user, acc created.
        # we can now intereact with the server

        # todo: maybe sanitize the arguments so that we dont send more than 4096 bytes

        self.user = user
        self.passwd = passwd

        if (existing):
            self.client.send(b'true')
            response = self.client.recv(4096)

            if (response == b'good to go'):
                userpass = user + " " + passwd
                self.client.send(str.encode(userpass))
                response = self.client.recv(4096)

                if (response == b'correct'):
                    return True

                else:
                    return False

            else:
                return False

        else:
            self.client.send(b'false')
            response = self.client.recv(4096)

            if (response == b'good to go'):
                userpass = user + " " + passwd
                self.client.send(str.encode(userpass))
                response = self.client.recv(4096)

                if (response == b'saved'):
                    return True

                else:
                    return False

            else:
                return False

    def sendMsg(self, msg):
        # send message to server.
        # first, append message to self.user + " " so the server knows who is sending
        # server will respond with recieved if authenticated, or an error if not auth'd
        data = self.user + " " + msg
        data = str.encode(data)

        self.client.send(data)

    def closeConn(self):
        self.client.close()

client = Client()
client.getConn('127.0.0.1', 8080)

uIn = input("Would you like to:\n(L)og in, or\n(R)egister?\n\n> ")
canMsg = False

if uIn == "L":
    tempUser = input("\nUser: ")
    tempPass = input("Pass: ")
    if client.authClient(True, tempUser, tempPass):
        print("Connected!\n")
        canMsg = True
    else:
        print("Incorrect username or password.")

elif uIn == "R":
    tempUser = input("\nUser: ")
    tempPass = input("Pass: ")
    if client.authClient(False, tempUser, tempPass):
        print("Registered!\n")
        canMsg = True
    else:
        print("Ruh roh...")

while canMsg:
    message = input(client.user + "> ")

    if message == "/exit":
        break

    client.sendMsg(message)

client.closeConn()
