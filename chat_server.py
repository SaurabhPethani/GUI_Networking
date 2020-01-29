import socket
from tkinter import *
import threading
import _thread

def send(event):
    global chatEntry,chat, sendButton, connections
    msg=chatEntry.get()
    if msg != 'q'and len(connections) >= 1:

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

class Server(threading.Thread):
    def __init__(self, soc ):
        threading.Thread.__init__(self)
        self.client= soc    

    def run(self):
        global chat
        msg =''
        while msg != 'q':
            print("Receiving...")
            msg = self.client.recv(1024).decode('utf-8')
            if msg != 'q':
                chat.insert(END, "Client -> " + msg + "\n")

                for connection in connections:
                    if connection != self.client:
                        connection.send(msg.encode('utf-8'))
        print("removing : ",self.client)
        connections.remove(self.client)
        print("Closing connection")
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
        client.start()

# loop = threading.Thread(target= doConnection)
# loop.start()

_thread.start_new_thread(doConnection,())
root.mainloop()