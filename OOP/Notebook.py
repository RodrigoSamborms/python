
import datetime
#Store the next avaible id for all new notes
last_id=0
class Note:
    '''Represent a note in the notebook. Match againts a
    string in searches and store tags for each note
    '''
    def __init__(self, memo, tags=''):
        '''initialize a note with meo and optional
        space-separated tags. Automatically set the note's
        creation date and unique id.'''
        self.memo=memo
        self.tags=tags
        self.creation_date=datetime.date.today()
        global last_id
        last_id +=1
        self.id =last_id
    def match(self, filter):
        '''Determine if this note matches the filter text.
        Return True if i matches, False otherwise.
        Search iss case sensitive and matches both text and
        tags
        '''
        return  filter in self.memo or filter in self.tags
class Notebook:
    '''Represent a collection fo notes that can be tagged,
    modified, and searched.'''
    def __init__(self):
        '''Initialize a notebook with an empty list'''
        self.notes=[]
    def new_note(self,memo,tags=''):
        '''Creates a new note and add it to the list'''
        self.notes.append(Note(memo, tags))
    def _find_note(self, note_id):
        '''Locate the note with the given id.'''
        for note in self.notes:
            if str(note.id) == str(note.id):
                return note
        return None
    def modify_memo(self, note_id, memo):
        '''Find the note with the given id chage its
        memo to the given value'''
        note = self._find_note(note_id)
        if note:
            note.memo=memo
            return True
        return False
    def modify_tags(self, note_id, tags):
        '''Find the note with the given id and changes its
        tags to the given value'''
        for note in self.note_id:
            note.tags=tags
            break
    def search(self, filter):
        '''Find all notes that match the given filter
        string'''
        return [note for note in self.notes if note.match(filter)]
    
