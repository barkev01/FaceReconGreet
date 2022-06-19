from typing import List


class Person:
    
    def __init__(self,name : str):
        self._name = name
        self._list = []

    def hello(self):
        print('Hello my name is '+self._name)
        print('this is my list of images')
        print(self._list)

    def setList(self, images : List):
        self._list = images

    def get_name(self) -> str:
        return self._name
    
    def get_list(self) -> List[str]:
        return self._list

#p1 = Person('Barkev')
#print(p1.getName())
#p1.hello()