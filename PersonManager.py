from numpy import str0
import Person

class PersonManager:

    def __init__(self):
        self._list = []

    def addPerson(self,p : Person):
        self._list.append(p)

    def getList(self):
        return self._list

    def getPersonByName(self, name : str) -> Person:
        for persons in self._list:
            if(persons.get_name() == name):
                return persons

            
