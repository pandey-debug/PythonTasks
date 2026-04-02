#Vehicle Management System (Inheritance)
#A transport company manages different vehicles. Create a base class Vehicle with
#attributes like brand and speed. Create derived classes Car and Bike that inherit from
#Vehicle and display their details.
class Vehicle:
    car_brand="TATA SAFARI"
    car_speed="270 KMPH"
    bike_brand="HERO"
    bike_speed="120 KMPH"
class car(Vehicle) :
    def car_details(self):
          print(f"BRAND:{self.car_brand} AND TOP SPEED OF {self.car_speed}") 
class bike(Vehicle):    
    def bike_details(self):
         print(f"BRAND:{self.bike_brand} And Top Speed Is {self.bike_speed}")


c=car()
b=bike()
c.car_details()
b.bike_details()