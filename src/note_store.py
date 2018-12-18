# Note Store
class NoteStore:
    """Abstract base class for NoteStore
    """
    def __init__(self):
        pass
    def find(self,note):
        raise NotImplementedError("Method `find` not implemented.")
    def store(self,note):
        raise NotImplementedError("Method `store` not implemented.")
    def unique_name(self):
        raise NotImplementedError("Method `unique_name` not implemented.")

class DictNoteStore(NoteStore):
    NAME_FORMAT="Note %d"
    def __init__(self):
        self.__dict__={}
        self.id_number=0

    def find(self,note):
        if note in self.__dict__:
            return self.__dict__[note]
        else:
            return None

    def store(self,note):
        key=note['name']
        self.__dict__[key]=note

    def unique_name(self):
        name=self.NAME_FORMAT %(self.id_number,)
        while name in self.__dict__:
            self.id_number+=1
            name=self.NAME_FORMAT %(self.id_number,)
        return name
