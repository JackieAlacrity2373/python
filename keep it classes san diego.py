class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def myfunc(self):
        print("Hello my name was " + self.name)
    def myfunc2(self):
        print("My name is now " + self.name)


p1 = Person("Jack", 27)

p1.myfunc()
print("give me a new name")
p1.name = input()
p1.myfunc2()
