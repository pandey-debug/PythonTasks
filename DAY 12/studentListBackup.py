#Student List Backup (Shallow Copy)
#A teacher has a list of student marks:
#marks = [50, 60, 70, 80]
#Scenario:
#She creates a backup using assignment:
#backup = marks
#Task:
#● Modify the first element in marks.
#● Observe the change in backup.
#● Explain why both lists are affected.
import copy
marks=[50, 60, 70, 80]
backup=marks #here the marks=backup because already given and tif we chane anything to the marks the backup will also be changed
backup[0]=90
print(backup)
print(marks)

