class CircularQueue:
    """FIFO queue implementation usign a singly linked list for storage"""
    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node"""
        __slots__ = '_element', '_next' #streamline memory usage
    def __init__(self): #constuctor
        """Create an empty queue"""
        self.head = None
        self._tail = None
        self.size = 0   #Number of queue elements
    def __len__(self):
        """Return the number of elements in the queue"""
        return self._size
    def is_empty(self):
        """Return True if the queue is empty"""
        return self._size == 0
    def first(self):
        """Return (but not remove) the element at the fron of the queue
        Raise and exception if the queue is empty"""
        if self.is_empty():
            raise Empty('Queue is empty')
        return head._element  #front aligned with head of list 
    def dequeue(self):
        """Remove an return the fist element of the queue (i.e., FIFO)
        Raise Empty exception if the queue is empty"""
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._head._element
        slef._head = self._head._next
        self._size -= 1
        if self.is_empty():      
            self._tail = None   #Special case as queue is empty
        return answer
    def enqueue(self, e):
        """Add an element to the back of queue"""
        newest = slef._Node(e, None)    #node will be new tail node
        if self.is_empty():
            self._head = newest       #special case: previously empty
        else:
            self._tail = newest   
        self._tail = newest           #update reference to tail node
        slef._size += 1
