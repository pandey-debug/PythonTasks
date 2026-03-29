products={"Pen":10,"Notebook":50,"Pencil":5}
cart_list=[]
product_cat=set()

def total_bill(cart_list):
    if len(cart_list)==0:
        return 0
    item,qunatity= cart_list[0]
    return (products[item] * qunatity)+ total_bill(cart_list[1:])


def display_products():
    print("AVAILABLE PRODUCTS")
    for item,price in products.items():
        print(f"{item} : {price}") 

def add_items():
    try:
        name= input("Enter product name\n")
        if name not in products:
            return NameError

        quantity=int(input("Enter a quantity"))  
        cart_list.append((name,quantity))  
    except ValueError:
        print("Invalid input! enter numeric quantity")
    except NameError:
        print("product not found")
    except TypeError:
        print("Wrong data type")            

def view_bill():
    try:
        if not cart_list:
            print("cart is empty")
            return
        
        print("")
        for item,quantity in cart_list:
           print(f"{item} x {quantity}")

        total=total_bill(cart_list)
        print("Total Bill:",total)   

    except ZeroDivisionError:
        print("Calculation error.")
    except TypeError:
        print("Wrong data type in cart.")      




while True:
    print("\n1. Display Products")
    print("2. Add Item to Cart")
    print("3. View Total Bill")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        display_products()
    elif choice == '2':
        add_items()
    elif choice == '3':
        view_bill()
    elif choice == '4':
        print("Exiting program...")
        break
    else:
        print("Invalid choice! Please try again.")
