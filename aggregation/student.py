class Student:
    def __init__(self, name, age, major, gpa):
        self.name = name
        self.age = age
        self.major = major
        self.gpa = gpa

    def __repr__(self):
        return f"name: {self.name}, age: {self.age}, major: {self.major}, gpa: {self.gpa:.2f}"
