class character:
    def __init__(self, name, strength):
        self.name=name
        self.strength=strength

    def changeStrength(self, difference):
        self.strength=self.strength+difference

    def getStrength(self):
        return self.strength

    def getName(self):
        return self.name

class wizard(character):
    def __init__(self, name, strength, magic):
        character.__init__(self, name, strength)
        self.magic=magic
        
    def heal(self):
        self.strength=self.strength+5

    def getMagic(self):
        return self.magic

wiz = wizard("david", 110110110, 1010101010)
print(wiz.strength)



class sort:
    def __init__(self, array):
        self.array = array
        
class bubble(sort):
    def __init__(self, array):
        sort.__init__(self, array)
        self.__temp = 0

    def ints(self):
        for i in range(0, len(self.array)):
            for y in range(0, len(self.array)-1):
                if self.array[y] > self.array[y+1]:
                    self.__temp = self.array[y]
                    self.array[y] = self.array[y+1]
                    self.array[y+1] = self.__temp
        return self.array

class merge(sort):
    def __init__(self, array):
        sort.__init__(self, array)
        self.__split = int(len(array) / 2)

    def ints(self):
        self.__left = self.array[:self.__split]
        self.__right = self.array[self.__split:]
        self.__left = bubble(self.__left).ints()
        self.__right = bubble(self.__right).ints()
        print(self.__right, self.__left)

print(merge([1, 4, 3, 8, 12, 8, 2, 214]).ints())