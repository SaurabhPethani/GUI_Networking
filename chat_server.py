import socket
from tkinter import *
import threading
import _thread
import queue

messageQueue = queue.Queue()

# This function will send message(should not be 'q') typed in Entry field to all clients connected to it 
def send(event):
    global chatEntry,taData, sendButton, connections
    msg=chatEntry.get()
    taData.set('{} \n {}'.format(taData.get(), msg))
    if msg != 'q'and len(connections) >= 1:
        for connection in connections:
            connection.send(msg.encode('utf-8'))
    chatEntry.delete(0, END)

# GUI code starts here
root = Tk()
root.geometry("300x300")
root.title("Server")
Label(root, text="-------Server--------").pack(side="top")
taData = StringVar()
taData.set('')
chat = Label(root, textvariable=taData)
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
        msg = self.client.recv(1024).decode('utf-8')
        taData.set('{} \n {}'.format(taData.get(), msg))
        while msg != 'q':
            messageQueue.enqueue(msg)
            print("Receiving...")
            msg = self.client.recv(1024).decode('utf-8')                
            taData.set('{} \n {}'.format(taData.get(), msg))
        print("removing : ",self.client)
        connections.remove(self.client)
        print("Closing connection")
        self.client.close()

# Initiate Networking
serverSocket = socket.socket()
serverSocket.bind(('localhost', 3690))
serverSocket.listen(5)

connections = []    # stores objects of all clients connected to it


class MessageDispatcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        global messageQueue
        while True:
            msg = messageQueue.dequeue()
            print(msg)
            for connection in connections:
                connection.send(msg.encode())

# doConnection will accept connection from client -> append socket to connections list -> create a thread for that socket-> starts the thread
def doConnection():
    while True:
        soc,addr = serverSocket.accept()
        connections.append(soc)
        client = Server(soc)
        client.start()
_thread.start_new_thread(doConnection,())   # Thread is assigned a task to 'doConnection' which will die when main thread will die
msgDispatch = MessageDispatcher()
msgDispatch.setDaemon(True)
msgDispatch.start()
root.mainloop()     # main thread will capture event objects from event queue and send it to respective objects of components