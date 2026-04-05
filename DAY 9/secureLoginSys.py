#13. Secure Login System (Decorators)
#A web application wants to ensure that users are authenticated before accessing
#sensitive functions. Create a decorator that checks whether the user is logged in before
#allowing access to a function.
def SecureloginSys(func):
    def login_details():
     ids="Tarun"
     Passw="Pandey"
     while True:
        a=input("Enter Your Id Name")
        b=input("Enter Password")
        if a==ids and b==Passw:
            print("Authentication Successful")
            func()
            break
        else:
            print("Authentication Unsuccessful")
            break
    return login_details   
       

@SecureloginSys
def info():
     print("You Can Access " \
            "--> Sensitive INFORMATION")
info()           


                