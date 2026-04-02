#A student stores daily notes in a file called notes.txt. Write a program that opens the
#file, reads all the contents, and displays them on the screen.

notes=input("Enter Notes to be added")

file=open("notes.txt","a")
file.write(notes+"\n")
file.close()
file=open("notes.txt","r")
'''printing on screen '''
print(file.read())
file.close()
