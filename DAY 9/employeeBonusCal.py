#17. Employee Bonus Calculator (Decorators & OOP)
#A company wants to apply a bonus calculation automatically before displaying the
#salary. Create an Employee class and use a decorator that modifies the salary by
#adding a bonus before displaying it
def Bonus(func):
    def salary(self):
        bonus=15000
        self.salary+=bonus
        func(self)
        print("Your salary is credited with bonus")
    return salary
class Employee:
    def __init__(self, salary):
        self.salary = salary
    @Bonus
    def display_salary(self):
        print("Salary after bonus:", self.salary)


emp=Employee(15000)
emp.display_salary()    
