import socket
from tkinter import *
import threading

def send(event):
    global chatEntry,chat, sendButton, connections
    msg=chatEntry.get()
    for connection in connections:
        connection.send(msg.encode('utf-8'))
    chat.insert(END, "YOU - > "+msg+"\n")
    chatEntry.delete(0, END)

root = Tk()
root.geometry("300x300")
root.title("Server")
Label(root, text="-------Server--------").pack(side="top")
chat = Text(root, width=20, height=10)
chat.pack(side="top")

frame = Frame(root)

chatEntry = Entry(frame)
chatEntry.pack(side="left")

sendButton = Button(frame, text="Send")
sendButton.pack(side="left")
sendButton.bind("<Button>", send)
frame.pack(side="top")

class Server:
    def __init__(self, soc ):
        self.client= soc    

    def receive(self):
        global chat
        msg =''
        while msg != 'q':
            print("Receiving...")
            msg = self.client.recv(1024).decode('utf-8')
            chat.insert(END, "Client -> " + msg + "\n")
            for connection in connections:
                connection.send(msg.encode('utf-8'))
        self.client.close()

serverSocket = socket.socket()
serverSocket.bind(('localhost', 3690))
serverSocket.listen(5)

connections = []
def doConnection():
    while True:
        soc,addr = serverSocket.accept()
        connections.append(soc)
        client = Server(soc)
        rec_thread = threading.Thread(target = client.receive)
        rec_thread.start()

loop = threading.Thread(target= doConnection)
loop.start()
root.mainloop()