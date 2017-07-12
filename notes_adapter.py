"""LogicAdapter for notes.

Syntax:
    start note <name>
    <note text>
    end note
"""
from chatterbot.logic import LogicAdapter

def remove_start(original,remove):
    if original.startswith(remove):
        return original[len(remove):].strip()
    else:
        return original

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


class NotesAdapter(LogicAdapter):
    START_NOTE='take note'
    END_NOTE='end note'

    def __init__(self,**kwargs):
        super(NotesAdapter, self).__init__(**kwargs)
        self.taking_note=False

    def can_process(self, statement):
        return self.taking_note or statement.text.startswith(self.START_NOTE)
    def process(self, statement):
        if not self.taking_note:
            return self.start_note(statement)
        if statement.text.startswith(self.END_NOTE):
            return self.store_note(statement)
        self.current_note['content'].append(statement.text)
        return 1,Statement('line added')
    def start_note(self, statement):
        self.taking_note=True
        note_name=remove_start(statement.text,self.START_NOTE)
        if not note_name:
            note_name=self.store.unique_name()
        found=self.store.find(note_name)
        if found:
            self.current_note=found
            return 1,Statement(found["content"][-1])
        else:
            self.current_note={'name':note_name,content:[]}
            return 1,Statement("New note: %s" % (note_name,))
    def store_note(self,statement):
        result=self.store.store(self.current_note)
        if not result:
            self.current_note=None
            self.taking_note=False
            return 1,Statement("Note stored")
        else:
            return 1,Statement("Storing failed with %s. Try again." %(result,))
