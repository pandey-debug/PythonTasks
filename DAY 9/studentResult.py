#7. Student Result Generator (Method Overloading Concept)
#A school system calculates student results differently depending on available data.
#Create a Result class where a method can calculate the result using either two
#subjects or three subjects
class Result():
    def calculate(self,stu1,stu2,stu3=None):
        if stu3==None:
            total=stu1+stu2
            avg=total/2
            print("AVERAGE OF TWO STUDENTS:",avg)
        else:
            total=stu1+stu2+stu3
            avg=total/3
            print("AVERAGE OF THREE STUDENTS",total)


r=Result()

while True:
    print("\n1. Enter marks for 2 subjects")
    print("2. Enter marks for 3 subjects")
    print("3. Exit")

    choice=int(input("ENTER YOUR CHOICE"))

    if choice==1:
        stu1=int(input("ENTER MARKS FOR FIRST STUDENT"))
        stu2=int(input("ENTER MARKS FOR SECOND STUDENT"))
        r.calculate(stu1,stu2)

    elif choice==2:
        stu1=int(input("ENTER MARKS FOR FIRST STUDENT"))
        stu2=int(input("ENTER MARKS FOR SECOND STUDENT")  )
        stu3=int(input("ENTER MARKS FOR THIRD STUDENT") ) 
        r.calculate(stu1,stu2,stu3)   

    elif choice==3:
        print("EXITING PROGRAM")
        break     

    else:
        print("ENTER VALID CHOICE")