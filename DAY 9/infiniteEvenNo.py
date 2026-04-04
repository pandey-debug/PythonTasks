#15. Infinite Even Number Generator (Generators)
#Create a generator function that continuously generates even numbers starting from
#2. The program should print the first N even numbers using this generator.

def even_numbers(n):
    for i in range(n):
       if i % 2 == 0:
           yield i
for num in even_numbers(10):
    print(num)