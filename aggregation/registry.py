from student import Student

class Registry:
    def __init__(self):
        self.students = []
    
    def add_student(self, name, age, major, gpa):
        student = Student (name, age, major, gpa)
        self.students.append (student)

    def get_average_age (self):
        total = sum (s.age for s in self.students)
        return total / len (self.students)
    
    #read
    def show_students(self):
        for student in self.students:
            print(student)

    #update
    def update_by_name (self, name, new_age):
        for student in self.students:
            if student.name == name:
                student.age = new_age
                print (f"{student.name} is now {student.age} years old.")
                return
            
        print (f"{name} not found.")
        

    
    #delete
    def delete_by_name (self,name):
        for student in self.students:
            if student.name == name:
                print (f"{student.name} is removed.")
                self.students.remove(student)
                return
            
        print (f"{name} not found.")


    