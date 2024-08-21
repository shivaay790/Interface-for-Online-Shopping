from prettytable import PrettyTable
import mysql.connector as my

my_con = my.connect(host="localhost",user="root",password="123456",database="online_shopping")
cursor = my_con.cursor()
"""
# Create employee table
employees_data = [
    {"name": "Shivaay", "age": 30, "emp_number": 201},
    {"name": "Shivansh", "age": 25, "emp_number": 202},
    {"name": "Madhubala", "age": 28, "emp_number": 203},
    {"name": "Anuj", "age": 35, "emp_number": 204},
    {"name": "Kartik", "age": 32, "emp_number": 205},
    {"name": "Aarav", "age": 27, "emp_number": 206},
]

Q3 = '''CREATE TABLE employees1(
    name VARCHAR(255),
    age INT,
    emp_number INT 
    )'''
cursor.execute(Q3)

Q4 = "INSERT INTO employees1 (emp_number, name, age) VALUES (%s, %s, %s)"

for employee in employees_data:
    cursor.execute(Q4, (employee["emp_number"], employee["name"], employee["age"]))

my_con.commit()



#  List of products with name, price, item number, and stock
products_data = [
    {"name": "Classic T-Shirt", "price": 19.99, "item_number": 101, "stock": 5000},
    {"name": "Canvas Backpack", "price": 34.99, "item_number": 102, "stock": 3000},
    {"name": "Wireless Mouse", "price": 12.99, "item_number": 103, "stock": 4000},
    {"name": "Stainless Steel Water Bottle", "price": 15.49, "item_number": 104, "stock": 2000},
    {"name": "HD Webcam", "price": 29.99, "item_number": 105, "stock": 2500},
    {"name": "Leather Wallet", "price": 22.95, "item_number": 106, "stock": 3500},
    {"name": "Bluetooth Earbuds", "price": 39.99, "item_number": 107, "stock": 1500},
    {"name": "Desk Organizer Set", "price": 18.75, "item_number": 108, "stock": 1000},
    {"name": "Smartphone Stand", "price": 9.99, "item_number": 109, "stock": 5000},
    {"name": "Coffee Mug Set", "price": 24.50, "item_number": 110, "stock": 6000},
]

Q5 = '''CREATE TABLE products_stock(
    item_number INT PRIMARY KEY,
    name VARCHAR(255),
    price FLOAT,
    stock INT
)'''
cursor.execute(Q5)

Q6 = "INSERT INTO products_stock(item_number, name, price, stock) VALUES (%s, %s, %s, %s)"

for product in products_data:
    cursor.execute(Q6, (product["item_number"], product["name"], product["price"], product["stock"]))

my_con.commit()

"""



# 1) display stock details in a pretty table
def display_stock_products():
    cursor.execute("SELECT * FROM products_stock")
    products = cursor.fetchall()  # gives a list of tuples

    pretty_sproducts_data = PrettyTable()
    pretty_sproducts_data.field_names = ["item_number", "name", "price", "stock"]

    for product in products:
        pretty_sproducts_data.add_row(product)

    print(pretty_sproducts_data)


# 2) checking database details
def database_details():
    cursor.execute(f"SHOW TABLES FROM online_shopping")
    records = cursor.fetchall()
    for table in records:
        print(table[0], end = ', ')

    record_search = input("enter the name of the table to be found: ")
    cursor.execute(f"SELECT * FROM {record_search}")
    records = cursor.fetchall()
    
    if cursor.fetchone():
        feilds = cursor.column_names
    else:
        feilds = []

    pretty_rec = PrettyTable()
    pretty_rec.field_names = feilds
    
    for record in records:
        pretty_rec.add_row(record)

    print(pretty_rec)
    


# 3) display employee details in a pretty table
def display_employees():
    cursor.execute("SELECT * FROM employees1")
    emp = cursor.fetchall()  

    pretty_employees_data = PrettyTable()
    pretty_employees_data.field_names = ["name", "age", "emp_number"]

    for employee in emp:
        pretty_employees_data.add_row(employee)

    print(pretty_employees_data)


# 5) Main menu driven for Manager
def menu_manager():
    while True:
        password = input("enter password: ")
        if password == "glass":
            break
        else:
            print("Invalid password")
            

    if password == "glass":
        while True:
            print("\nMenu:")
            print("1. Display stock")
            print("2. show database details")
            print("3. employee list")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                display_stock_products()
            elif choice == '2':
                database_details()
            elif choice == '3':
                display_employees()
            elif choice == '4':
                break
            else:
                print("Invalid choice.")
            
        print("THANK YOU!!")
    
    
