#6. Shape Area Calculator (Polymorphism)
#A graphics application needs to calculate the area of different shapes. Create classes
#Circle, Rectangle, and Triangle, each having an area() method. Demonstrate
#polymorphism by calling the same method for different objects.
import math
class Circle():
    def area(self):
        print("Calculate the Area of Circle")
        
        radius=int(input("Enter Radius of circle"))
        self.area_cir=math.pi*radius*radius
        print("Aea of circle is:", self.area_cir)
class Rectangle():
    def area(self):
        print("Area of rectangle")
        self.length=int(input("Enter length"))
        self.width=int(input("Enter width"))
        self.area_rect=self.length*self.width
        print("Aeaa of rectangle is:", self.area_rect)

class Triangle():
    def area(self):
        print("Area of Triangle")
        self.base=int(input("Enter base"))
        self.height=int(input("Enter height"))
        self.area_tri=1/2*(self.base*self.height)
        print("Aeaa of triangle is:", self.area_tri)

shapes = [Circle(), Rectangle(), Triangle()]

for shape in shapes:
    shape.area()