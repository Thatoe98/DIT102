'''
Name - Thatoe Nyi
ID- 6708351
Class - DIT102
'''
class Student:
    def __init__(self, name, ID, major, age):
        self.name = name
        self.ID = ID
        self.__major= major
        self.__age = age

    def get_major (self):
        return self.__major
    
    def get_age (self):
        return self.__age
    
    def iterate_age (self):
        self.__age += 1

    def change_major (self, major):
        self.__major = major

    def display_info (self):
        major = self.get_major()
        age = self.get_age()
        return f"{self.name} of ID {self.ID} is {age} years old and in {major} major."


def main():
    student = Student("Thatoe Nyi", 6708351, "Computer Science", 26)
    print(student.display_info())

    student.iterate_age()
    student.change_major("DIT")

    print ("Info has been changed.")
    print(student.display_info())

if __name__ == "__main__":
    main()