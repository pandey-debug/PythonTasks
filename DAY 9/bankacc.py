#3. Employee Salary System (Simple Inheritance)
#A company has two types of employees: Employee and Manager. Create a base class
#Employee containing name and salary. Create a derived class Manager that inherits
#from Employee and displays the employee details.

class BankAccount:
    
    def __init__(self):
        self.accntnmbr=9988678
        self.balance=99099

    def deposits(self,Deposite_amt):
        self.balance+=Deposite_amt
        print("Amount Deposited Rs",Deposite_amt)
        print("Total Available Balance",self.balance)

    def withdraw(self,Withdraw_amt):
        if Withdraw_amt>self.balance:
            print("Insufficient Funds")

        else:
            self.balance-=Withdraw_amt
            print("Balance after Withdrawal",self.balance)
    

    def display(self):
        print("Account no :",self.accntnmbr)
        print("Balance Available:",self.balance)
Deposite_amt=int(input("Enter Amount To Deposite"))
Withdraw_amt=int(input("Enter Amount To Withdraw"))

B=BankAccount()
B.deposits(Deposite_amt)
B.withdraw(Withdraw_amt)
B.display()
