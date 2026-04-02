class student:
    def display(self):
        print("Name",self.name)
        print("Roll No",self.roll)
        print("Marks",self.marks)

s1=student()
s2=student()
s3=student()

s1.name=input("Enter name: ")
s1.roll=int(input("Enter roll number: "))
s1.marks=int(input("Enter marks: "))

s2.name=input("Enter name: ")
s2.roll=int(input("Enter roll number: "))
s2.marks=int(input("Enter marks: "))

s3.name=input("Enter name: ")
s3.roll=int(input("Enter roll number: "))
s3.marks=int(input("Enter marks: "))

print("\nStudent Details:")
s1.display()
s2.display()
s3.display()


