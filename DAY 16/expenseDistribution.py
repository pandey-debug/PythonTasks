#3. Expense Distribution Pie Chart
#Scenario:
#Monthly expenses:
#labels = ["Food", "Rent", "Travel"]
#Task:
#● Create a pie chart
#● Show percentage distribution
import matplotlib.pyplot as plt
labels = ["Food", "Rent", "Travel"]
expenses = [3000, 6000, 2000]  # example values
plt.pie(expenses, labels=labels, autopct='%1.1f%%')
plt.title("Monthly Expense Distribution")
plt.show()