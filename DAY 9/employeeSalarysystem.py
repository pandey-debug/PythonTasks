class employee:
    def data(self):
        self.name=input("enter a name ")
        self.salary=int(input("Enter salary"))

class manager(employee):
    def display(self):
        print("DETAILS\n")
        print("Employee",self.name)
        print("Salary",self.salary)

b=manager()
b.data()
b.display()