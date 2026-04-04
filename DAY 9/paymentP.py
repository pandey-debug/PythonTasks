#11. Payment System (Runtime Polymorphism)
##An online store supports multiple payment methods: CreditCard, UPI, and
#NetBanking. Create a base class Payment with a method process_payment() and
#override it in each payment type.

class Payments:
    def process_payments(self):
        print("Payment an be done through different ways")

class Credit_Card(Payments):
    def process_payments(self):
        print("Payment Recieved through Credit card")
        

class Upi(Payments):
    def process_payments(self):
        print("Payment Recieved through UPI")

class NetBanking(Payments):
    def process_payments(self):
        print("Payment Recieved through NetBanking")

while True:
    print("1.Credit_Card")
    print("2.UPI")
    print("3.NetBanking")
    print("4.Cancel")

    choice=int(input("Enter Method Of Payment"))
    if choice==1:
        print("Processing Payment through Credit Card\n")
        c=Credit_Card()
        c.process_payments()
        break  
    elif choice==2:
        print("Processing Payment through UPI\n")
        u=Upi()
        u.process_payments()
        break
    elif choice==3:
        print("Processing Payment through Net Banking\n")
        n=NetBanking()
        n.process_payments()
        break
    elif choice==4:
        print("Transaction Failed\n")
        break
    else:
        print("Payment Failed")
       