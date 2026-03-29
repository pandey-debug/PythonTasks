subjects=("Maths","Science","English")
students=set(subjects)
record={}

def total_marks(marks):
    if len(marks)==0:
        return 0
    else:
        return marks[0]+marks[1:]
            
        


def add_student():
    try:
        student=str(input("Enter a student name to add"))
        marks=[]
        for sub in subjects:
            m=int(input(f"Enter marks{sub}"))
            marks.append(m)
        students.add(student)
        record[student]=marks
    except ValueError: 
          print("Enter Valid Input")  

    except TypeError: 
          print("Enter Valid Input") 


    except NameError: 
          print("Enter Valid Input")   



def display_students():
    if not  record:
      print("Nothing to show")

    else:
        for student, marks in record.items():
            print(f"Name:{student} Marks:\n{marks}")

      

def avg_marks():
    try:
        name=input("Enter a name")
        if name not  in  record:
            print("no record found")
        
        marks=record[students]
        total=total_marks(marks)
        avg=total/ len(marks)
        print(f"Total Marks of is: {total} ",)
        print(f"Average marks of is: {avg} ",)

    except NameError:
        print("Name Not Found")
    except ZeroDivisionError:
        print("Cannot divide by 0")
    except TypeError:
       print("Marks data type error")

while True:
    print("\n1. Add Student")
    print("2. Display Students")
    print("3. Calculate Average")
    print("4. Exit")
    choice=input("Enter your choice")

    if choice=='1':
        add_student()

    elif choice=='2':
        display_students()
    elif choice=='3':
        avg_marks()    
    elif choice=='4':
        print("Exiting program")
        break   
    else:
        print("Invalid choice! Please try again.")    
    
    