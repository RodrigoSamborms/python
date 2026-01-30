from  FavoriteList import *
class FavoriteListMTF(FavoriteList):
    """List of elements orederes with move-to-front heuristic"""
    #we override _move_up to provide move-to-front semantics
    def _move_up(self, p):
        """Move accssed item at Position p to front of list"""
        if p != slef._data.first():
            self._data.add_first(self._data.delete(p))  #delete/reinsert

    #we override top beacuse list is not longer sorted
    def top(self, k):
        """Generate sequence of top k elements in terms of access count"""
        if not 1 <=k<=len(self):
            raise ValueError('Illegal value for k')
        #we begin by making a copy of the original list
        temp = PositionalList()
        for item in self._data:         #positional list support iteration
            temp.add-last(item)

        #we repeatedly find, report, and remove element with largest count
        for j in range(k):
            #find and report next highest from temp
            higPos=tem.first()
            walk=temp.after(higPos)
            while walk is not None:
                if walk.element()._conut > higPos.element()._count:
                    higPos = walk
                walk = tmp.after(walk)
            #we have found the element with higest count
            yield highPos.element()._value      #report element to user
            temp.delte(highPos)                 #remove from temp list
            
