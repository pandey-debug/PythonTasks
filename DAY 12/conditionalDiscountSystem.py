#4. Conditional Discount System (List Comprehension)
#A shop has prices:
#prices = [100, 200, 300, 400]
#Scenario:
#● Apply a 10% discount only if price > 200.
#Task:
#● Use list comprehension with condition to create updated price list.
prices = [100, 200, 300, 400]
updated_prices=[x*0.9 if x>200 else x for x in prices]
print(updated_prices)