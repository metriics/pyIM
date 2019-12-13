import socket

class User():
    def __init__(self, addr, creds, authed):
        self.addr = addr
        self.creds = creds
        self.authed = authed

    def getCreds(self):
        return self.creds

    def getAddr(self):
        return self.addr

    def getAuthed(self):
        return self.authed

    def setAddr(self, addr):
        self.addr = addr

    def setAuthed(self, authed):
        self.authed = authed


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind(('127.0.0.1', 8080))
serv.listen(5)

registeredUsers = []

while True: # can only handle one connection at a time due to the way we have set up the while loops
    conn, addr = serv.accept()
    client_creds = []

    print(str(addr) + " connected.")

    while True:
        data = conn.recv(4096)
        if not data:
            break

        if (data == b'true'): # client is existing user
            conn.send(b'good to go')  # tell client to send user and pass
            data = conn.recv(4096)
            client_creds = data.decode().split()

            uExists = False
            for user in registeredUsers:
                if user.getCreds() == client_creds:
                    uExists = True
                    user.setAuthed(True)
                    user.setAddr(conn.getpeername())
                    print(user.creds[0] + " logged in.")
            
            if uExists:
                conn.send(b'correct')
            else:
                conn.send(b'wrong user or pass')

        elif data == b'false': # client wants to register as new user
            conn.send(b'good to go')  # tell client to send user and pass
            data = conn.recv(4096)
            client_creds = data.decode().split()

            newUser = User(conn.getpeername(), client_creds, True)

            registeredUsers.append(newUser)
            conn.send(b'saved')

        else:  # check if client is 
            message = data.decode().split()
            uName = message[0]

            for user in registeredUsers:
                if (uName == user.getCreds()[0]) & user.getAuthed(): # user is authed and message will be sent
                    message = message[1:]
                    messageStr = ""
                    for word in message:
                        messageStr += " " + word
                    print(uName + ":" + messageStr)

            # do nothing if user isnt registered and authed


    tempName = ""
    for user in registeredUsers: # if ip was a registered user, deauth them before closing socket
        if conn.getpeername() == user.getAddr():
            user.setAuthed(False)
            tempName = user.getCreds()[0]

    if tempName == "":
        tempName = str(conn.getpeername())
        
    print(tempName + " disconnected.")
    
    conn.close()