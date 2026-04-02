#A user wants to save grocery items in a file grocery.txt. Write a Python program that
#takes multiple items from the user and writes them into the file, with each item on a
#new line.
file= open("groceryList.txt","w")
n=int(input("how many items need to be added"))
for i in range(n):
    e=input(f" ITEM NO: {i+1}\n")
    file.write(e+"\n")

print("ITEM ADDED IN GROCERY LIST")
file.close()

file=open("groceryList.txt","r")
print(file.read())
file.close()

