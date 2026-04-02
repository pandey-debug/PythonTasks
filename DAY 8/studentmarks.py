file=open("studentMarks.txt", "w")
n=int(input("How many students? "))
for i in range(n):
    name = input("Enter name: ")
    marks = int(input("Enter marks: "))
    file.write(name + " " + str(marks) + "\n")

file.close()


file=open("studentMarks.txt", "r")


total=0
count=0
print("\nStudent Records:")

for line in file:
    data = line.split()
    if len(data)==2:
        data=line.split()
        print(data[0], data[1])
    
        total= total+int(data[1])
        count=count+1

file.close()


average= total/count
print("Average Marks:", average)