import socket
from tkinter import *
import threading
import _thread

# This function will send message(should not be 'q') typed in Entry field to all clients connected to it 
def send(event):
    global chatEntry,chat, sendButton, connections
    msg=chatEntry.get()
    if msg != 'q'and len(connections) >= 1:

        for connection in connections:
            connection.send(msg.encode('utf-8'))
        chat.insert(END, "YOU - > "+msg+"\n")

    chatEntry.delete(0, END)

# GUI code starts here
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
# GUI code ends here

# Server class is used to have a Thread continuously seeking to receive message from connected clients 
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

# Initiate Networking
serverSocket = socket.socket()
serverSocket.bind(('localhost', 3690))
serverSocket.listen(5)

connections = []    # stores objects of all clients connected to it

# doConnection will accept connection from client -> append socket to connections list -> create a thread for that socket-> starts the thread
def doConnection():
    while True:
        soc,addr = serverSocket.accept()
        connections.append(soc)
        client = Server(soc)
        client.start()
_thread.start_new_thread(doConnection,())   # Thread is assigned a task to 'doConnection' which will die when main thread will die
root.mainloop()     # main thread will capture event objects from event queue and send it to respective objects of components