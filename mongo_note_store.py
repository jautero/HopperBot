from note_store import NoteStore
from pymongo import MongoClient

class MongoNoteStore(NoteStore):
    def __init__(self,**kwargs):
        self.database_name = self.kwargs.get(
            'database', 'chatterbot-database'
        )
        self.database_uri = self.kwargs.get(
            'database_uri', 'mongodb://localhost:27017/'
        )

        # Use the default host and port
        self.client = MongoClient(self.database_uri)

        # Specify the name of the database
        self.database = self.client[self.database_name]

        # Mongo colection of notes
        self.notes = self.database['notes']
        self.notes.create_index('name',unique=True)

    
