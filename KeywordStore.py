import yaml 
# Store an object with list of keywords.
class KeywordStore:
    def __init__(self):
        self.data={}
    def store(self,item,keywords):
        for kw in keywords:
            if not self.data.has_key(kw):
                self.data[kw]=set()
            self.data[kw].add(item)

    def get(self,keywords):
        result=set()
        for kw in keywords:
            if self.data.has_key(kw):
                result.update(self.data[kw])
        if result == set():
            raise IndexError
        else:
            return result
    def dump(self,file):
        yaml.dump(self.data,file)
    def load(self,file):
        self.data=yaml.load(file)