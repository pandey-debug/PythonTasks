#Create a Number Guessing Game where:
#  ● The program generates a random number between 1 and 50 using random.
#  ● The user has 5 attempts to guess the number. 
# ● After each guess, calculate the absolute difference using math.fabs() and 
# display how far the guess is from the correct number. explain me this question
import random
import math
a=random.randint(1,50)
#print(a)
d=5
print("Welcome To, THE GUESS GAME")
for i in range(1,d+1):
    
    b=int(input(f"ENTER A NUMBER TO GUESS,  Attempts {d}\n"))
    if b>=1 and b<=50:    
        if b==a:
            print("CONGRATULATIONS, Your Guess wasr Correct")
            print("YOU WON !!!!")
            print("Game Over")    
            break
        else:
            print(f"Wrong Guess! You are {math.fabs(b-a)} more close to the number ")

    else:
        print("ENTER A VALID NUMBER BETWEEN 1&50")  
     
if b!=a:
    print("You Lost All The Attempts")
    print("The Correct Guess Was",a)
    print("Game Over")




     
    

    
    
