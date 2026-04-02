#9. Online Shopping System (Multilevel Inheritance)
#An e-commerce company organizes products using multiple levels. Create classes
#Product → ElectronicProduct → MobilePhone using multilevel inheritance and
#display product details.
class product:
    def detailsA(self):
        print("Hi" )

class ElectronicProduct(product):
    def ElectronicP_details(self):
        print("Im electronic product")

class Mobile(ElectronicProduct):
    def mobile_details(self):
        print("Iam Mobile")

c=Mobile()
c.mobile_details()
c.ElectronicP_details()
c.detailsA()        