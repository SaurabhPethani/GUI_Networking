import socket
import threading
from tkinter import *

# This function will send the message typed on Entry field to the server
def send(event):
    global chatText,chatEntry, conn
    msg = chatEntry.get()
    conn.send(msg.encode('utf-8'))
    chatText.insert(END, "YOU -> "+msg+"\n")
    chatEntry.delete(0, END)
    if msg == 'q':
        conn.close()
# GUI code starts
root = Tk()
root.geometry("300x300")
root.title("Client")

chatText  =  Text(root, width=30, height=15)
chatText.pack(side="top")

frame = Frame(root)
chatEntry = Entry(frame)
chatEntry.pack(side="left")

chatButton = Button(frame, text="Send")
chatButton.pack(side="left")
chatButton.bind("<Button>", send)
frame.pack(side="top")
## GUI Ends here

# Client class is used to have a Thread continuously seeking to receive message from Server 
class Client(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        global chatText
        print("Running Thread")
        msg=''
        while msg != b'q':
            msg = self.client.recv(1024).decode('utf-8')
            print(type(msg), msg)
            chatText.insert(END, "Server -> "+msg+"\n")
        self.client.close()
        print("Thread Finished")

# Creating Socket enabling client machine to connect to server
conn = socket.socket()
conn.connect(("localhost", 3690))
print("Connected Successfully!")
conn.send("Connected ".encode('utf-8'))
client = Client(conn)   # Creating a Thread of Client socket object once connection gets established
client.start()          # Starting a Thread
print("Running main loop")
root.mainloop()         # main thread will look for events happening on GUI screen and send the Objects from event queue to Object Model(respective Object)
print("Main loop finished")