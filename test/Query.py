
class Query:
    def __init__(self,size = 30):
        self.size = size
        self.query = []
        self.front = 0
        self.rear = -1

    def is_empty(self):
        return self.rear == 0



