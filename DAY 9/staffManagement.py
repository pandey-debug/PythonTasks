#10. University Staff Management (Hierarchical Inheritance)
#A university has different staff types such as Professor, LabAssistant, and
#Administrator. All inherit from a base class Staff. Implement hierarchical inheritance
#to manage and display their information.
class Staff:
    def Information(self):
        print("STAFF:--This is Base Class")

class Professor(Staff):
    def Details(self):
        print("HERE THE DETAILS OF PROFESSORS WILL BE DISPLAYED")

class LabAssistant(Staff):
    def lab_detail(self):
        print("HERE THE DETAILS OF LABASSISTANT WILL BE DISPLAYED")

class Administator(Staff):
    def admin_detail(sef):
        print("HERE THE DETAILS OF ADMIN WILL BE DISPLAYED")


p=Professor()
l=LabAssistant()
a=Administator()
p.Information()
p.Details()
l.Information()
l.lab_detail()
a.Information()
a.admin_detail()


