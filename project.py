import customer11, manager11

print("1. Manager")
print("2. Customer")

while True:
    try:
        x = int(input("who is using (1/2): "))
        if x == 1 or x == 2:
            break
        else:
            print("Invalid")
    except ValueError:
        print("Invalid")

    
if x == 1:
    manager11.menu_manager()
if x == 2:
    customer11.menu_customer()