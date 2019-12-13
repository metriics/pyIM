# pyIM
a python instant messenger server and client
![scrsht](https://cdn.discordapp.com/attachments/198128978194726912/654911099929624586/unknown.png)

## A note...
This currently only supports one connection to the server at a time. I'm learning about sockets so for now I don't know how to handle multiple connections. 

An interesting test would be to try to connect between two different machines on the local network. For WAN connections you'd probably need to portforward and use a different port than 8080...

## Usage
IP and port are 127.0.0.1 and 8080 by default, can be changed in both .py files. Currently there is no persistent user storage so all registered users will be erased when the server is shutdown. I don't have any server input from the console so you just need to close the window to shutdown the server. To exit the client, you just send a message that contains only `/exit`

## Requirements
Python 3! That's it. This only uses the socket library included with python. Should run on Windows, macOS and Linux all the same.
