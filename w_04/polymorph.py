from multipledispatch import dispatch

#employee class with name and base_salary, this is the superclass
class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def calculate_salary(self):
        return self.base_salary
    
#manager subclass 
class Manager (Employee):
    def __init__(self, name, base_salary):
        super().__init__(name, base_salary)
    
    #two types of calculation, one with level of experience
    @dispatch (str)
    def calculate_salary(self, level):
        if level.lower() == "junior":
            return self.base_salary + 10000
        elif level.lower() == "mid":
            return self.base_salary + 20000
        elif level.lower() == "senior":
            return self.base_salary + 30000
        else:
            return self.base_salary
    
    #and one with just flat bonus
    @dispatch (int)
    def calculate_salary(self, bonus):
        return self.base_salary + bonus

#engineer subclass is additional performance index
class Engineer(Employee):
    def __init__(self, name, base_salary, performance):
        super().__init__(name, base_salary)
        self.performance = performance

    #salary based on performance index KPI
    def calculate_salary(self):
        total = self.performance * self.base_salary
        return total
    
#Sales subclass with additonal sales amount
class Salesperson(Employee):
    def __init__(self, name, base_salary, sales):
        super().__init__(name, base_salary)
        self.sales = sales
    
    #salary calculated by adding commission
    def calculate_salary(self):
        commission = self.sales * 0.2
        return self.base_salary + commission
def main():
    #create objects 
    person1 = Manager("Thatoe" , 100000 ) #manager with base salary
    person2 = Engineer ("Tyler", 50000, 1.2) #engineer with KPI
    person3 = Salesperson("AG", 30000, 200000) #sales person with total amount of sales

    print (f"Name: {person1.name}\nSalary for this year: ${person1.calculate_salary('mid')}\n") #salary of mid level manager
    print (f"Name: {person1.name}\nSalary for this year: ${person1.calculate_salary(25000)}\n") #salary of manager with flat bonus
    print (f"Name: {person2.name}\nSalary for this year: ${person2.calculate_salary()}\n") #salary of engineer with KPI
    print (f"Name: {person3.name}\nSalary for this year: ${person3.calculate_salary()}\n") #salary of sales person with commision


if __name__ == "__main__":
    main()
