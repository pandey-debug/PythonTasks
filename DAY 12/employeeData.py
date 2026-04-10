#3. Employee Data Copy Issue (Shallow vs Deep Copy)
#A company stores employee data:
#employees = [[101, "A"], [102, "B"], [103, "C"]]
#Scenario:
#● Create a shallow copy of the list.
# Modify one nested list (e.g., change "A" to "Z").
#● Observe changes in both lists.
#Task:
#● Explain why the change reflects in both.
#● Fix it using deep copy.
import copy
employees=[[101, "A"], [102, "B"], [103, "C"]]
updated_emp=copy.copy(employees)
employees[0][1]="Z"
print("Original\n",employees)
print("Updated Using Shallow Copy\n",updated_emp)
#here we used shallow copy so thats the reason it changes both original and updated one
employees_deep=[[101, "A"], [102, "B"], [103, "C"]]
deep_update=copy.deepcopy(employees_deep)
deep_update[0][1]="X"
print("Original\n",employees_deep)
print("Update Using Deep Copy\n",deep_update)



