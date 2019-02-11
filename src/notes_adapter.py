"""LogicAdapter for notes.

Syntax:
    take note <name>
    <note text>
    end note
"""
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot import utils
from note_store import NoteStore

def remove_start(original,remove):
    if original.startswith(remove):
        return original[len(remove):].strip()
    else:
        return original

class NotesAdapter(LogicAdapter):
    START_NOTE='take note'
    END_NOTE='end note'

    def __init__(self, chatbot, **kwargs):
        super(NotesAdapter, self).__init__(chatbot,**kwargs)
        self.taking_note=False
        notes_store=kwargs.get('notes_store','note_store.DictNoteStore')
        utils.validate_adapter_class(notes_store, NoteStore)
        self.store=utils.initialize_class(notes_store, **kwargs)

    def can_process(self, statement):
        return self.taking_note or statement.text.startswith(self.START_NOTE)
    def process(self, statement):
        response=self.process_statement(statement)
        if isinstance(response,Statement):
            response.confidence=1
            return response
        else:
            return Statement(response)
            
    def process_statement(self,statement):
        if not self.taking_note:
            return self.start_note(statement)
        if statement.text.startswith(self.END_NOTE):
            return self.store_note(statement)
        self.current_note['content'].append(statement.text)
        return Statement('line added')

    def start_note(self, statement):
        self.taking_note=True
        note_name=remove_start(statement.text,self.START_NOTE)
        if not note_name:
            note_name=self.store.unique_name()
        found=self.store.find(note_name)
        if found:
            self.current_note=found
            return Statement(found["content"][-1])
        else:
            self.current_note={'name':note_name,'content':[]}
            return Statement("New note: {}".format(note_name))
    def store_note(self,statement):
        result=self.store.store(self.current_note)
        if not result:
            self.current_note=None
            self.taking_note=False
            return Statement("Note stored")
        else:
            return Statement("Storing failed with {}. Try again.".format(result))
