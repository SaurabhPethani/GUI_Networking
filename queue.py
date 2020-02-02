import threading

class Queue:
    def __init__(self):
        self.q = []
        self.condition = threading.Condition()
    
    def enqueue(self, msg):
        with( self.condition):
            self.q.append(msg)
            self.condition.notify()
    
    def dequeue(self):
        with(self.condition):
            if self.isEmpty():
                self.condition.wait()
            msg = self.q[0]
            del self.q[0]
            return msg

    def isEmpty(self):
        return (len(self.q) == 0)