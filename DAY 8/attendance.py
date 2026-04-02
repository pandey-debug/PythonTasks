#A teacher wants to store student attendance in a file named attendance.txt. Write a
#Python program that takes a student name as input and appends it to the file. Then
#display the contents of the file.



std_name=input("Enter student name")
file=open("attendance.txt","a")
file.write(std_name+"\n")
file.close()



print("ATTENDANCE LIST")
file=open("attendance.txt","r")
print(file.read())
file.close()

