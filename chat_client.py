import socket
import threading
from tkinter import *

def send(event):
    global chatText,chatEntry, conn
    msg = chatEntry.get()
    conn.send(msg.encode('utf-8'))
    chatText.insert(END, "YOU -> "+msg+"\n")
    chatEntry.delete(0, END)
    if msg == 'q':
        conn.close()

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

conn = socket.socket()

conn.connect(("localhost", 3690))
print("Connected Successfully!")
conn.send("Connected ".encode('utf-8'))
client = Client(conn)
client.start()
print("Running main loop")
root.mainloop()
print("Main loop finished")