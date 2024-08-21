from prettytable import PrettyTable
import mysql.connector as my

my_con = my.connect(host="localhost",user="root",password="123456",database="online_shopping")
cursor = my_con.cursor()
"""
# Create Products table
Q1 = '''CREATE TABLE products(
    name VARCHAR(255),
    price FLOAT,
    item_number INT PRIMARY KEY 
    )'''
cursor.execute(Q1)

# Insert products into the Products table one by one
products_data = [
    {"name": "Classic T-Shirt", "price": 19.99, "item_number": 101},
    {"name": "Canvas Backpack", "price": 34.99, "item_number": 102},
    {"name": "Wireless Mouse", "price": 12.99, "item_number": 103},
    {"name": "Stainless Steel Water Bottle", "price": 15.49, "item_number": 104},
    {"name": "HD Webcam", "price": 29.99, "item_number": 105},
    {"name": "Leather Wallet", "price": 22.95, "item_number": 106},
    {"name": "Bluetooth Earbuds", "price": 39.99, "item_number": 107},
    {"name": "Desk Organizer Set", "price": 18.75, "item_number": 108},
    {"name": "Smartphone Stand", "price": 9.99, "item_number": 109},
    {"name": "Coffee Mug Set", "price": 24.50, "item_number": 110},
]

Q2 = "INSERT INTO products (item_number, name, price) VALUES (%s, %s, %s)"

for product in products_data:
    cursor.execute(Q2, (product["item_number"], product["name"], product["price"]))

my_con.commit()
"""




# 1) Display products
def display_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall() # gives a list of tuples

    pretty_products_data = PrettyTable()
    pretty_products_data.field_names = ["name", "price", "item_number"]

    for product in products:
        pretty_products_data.add_row(product) 

    print(pretty_products_data)



# 2) Add to cart
def add_to_cart(add_product, quantity, customer_cart):
    cursor.execute(f"SELECT * FROM {customer_cart} WHERE item_number = {add_product}")
    product_exist = cursor.fetchone()

    if product_exist:
        cursor.execute(f"UPDATE {customer_cart} SET quantity = {quantity + product_exist[3]} WHERE item_number = {add_product} ")
    else:
        cursor.execute(f"SELECT * FROM products WHERE item_number = {add_product}")
        product = cursor.fetchone()
        cursor.execute(f"INSERT INTO {customer_cart} VALUES('{product[0]}', {product[1]}, {product[2]}, {quantity})")

    my_con.commit()

# 3) Remove from cart 
def remove_from_cart(remove_product, quantity, customer_cart):
    cursor.execute(f"SELECT * FROM {customer_cart} WHERE item_number = {remove_product}")
    product_exist = cursor.fetchone()

    if product_exist:
        if quantity == product_exist[3]:
            cursor.execute(f"DELETE FROM {customer_cart} WHERE item_number = {remove_product} ")
        elif quantity < product_exist[3]:
            cursor.execute(f"UPDATE {customer_cart} SET quantity = {product_exist[3] - quantity} WHERE item_number = {remove_product} ")
        else:
            print("you donot have that many product in your cart")

    else:
        print("the item is not there in your cart")

    my_con.commit()


# 4) Display cart
def display_cart(customer_cart):
    cursor.execute(f"SELECT * FROM {customer_cart}")
    customer_cart = cursor.fetchall()

    pretty_cart = PrettyTable()
    pretty_cart.field_names = ["name", "price", "item_number", "quantity"]

    for product in customer_cart:
        pretty_cart.add_row(product)

    print(pretty_cart)


# 5) Calculate total cost
def calculate_total(customer_cart):
    cursor.execute(f"SELECT SUM(price * quantity) FROM {customer_cart}")
    total_cost = cursor.fetchone()[0]

    if total_cost == None:
        print("no item is there in cart: ")
    else:
        print("The total cost is: ", round(total_cost, 2))


# 6) Main menu driven for customer
def menu_customer():
    while True:
        input_str = input("enter your name: ")
        cursor.execute(f"SHOW TABLES FROM online_shopping")
        records = cursor.fetchall()

        if (input_str,) in records:
            print("customer with given name is already present")

        else:
            if " " in input_str:
                customer_cart = "-".join(input_str.split())
            else:
                customer_cart = input_str

            temp_customer_cart = customer_cart
            break



    Q1 = f'''CREATE TABLE {customer_cart}(
    name VARCHAR(255),
    price FLOAT,
    item_number INT PRIMARY KEY,
    quantity INT
    )'''
    cursor.execute(Q1)
    my_con.commit()

    while True:
        print("\nMenu:")
        print("1. Display Products")
        print("2. Add to Cart")
        print("3. Remove from Cart")
        print("4. Display Receipt")
        print("5. Calculate total")
        print("6. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            display_products()

        elif choice == "2":
            try:
                product = int(input("Enter the item_number you want to add: "))
                quantity = int(input("Enter the quantity: "))
                
                if (product not in [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]) or (quantity <= 0):
                    print("Please enter positive values and valid product ID.")
                else:
                    add_to_cart(product, quantity, customer_cart)

            except ValueError:
                print("Invalid input.")

        elif choice == "3":
            try:
                product = int(input("Enter the item_number you want to remove: "))
                quantity = int(input("Enter the quantity: "))
                
                if (product not in [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]) or (quantity <= 0):
                    print("Please enter positive values and valid product ID.")
                else:
                    remove_from_cart(product, quantity, customer_cart)

            except ValueError:
                print("Invalid input.")

        elif choice == "4":
            display_cart(customer_cart)

        elif choice == "5":
            calculate_total(customer_cart)

        elif choice == "6":
            customer_review = customer_cart + "reviews"

            Q7 = f'''CREATE TABLE {customer_review}(
            review_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(55),
            rating INT,
            review_text VARCHAR(120)
            )'''
            cursor.execute(Q7)
            my_con.commit()

            while True:
                try:
                    rating = int(input("Rate your experience (1-very bad to 10-very good): "))
                    review_text = input("Give your feedback (under 100 words): ")
                    if rating >= 1 and rating <= 10 and len(review_text) <= 100:
                        break
                    else:
                        print("Rating should be from 1 and 10 and Feedback should be under 100 words.")

                except ValueError:
                    print("Invalid input.")

            cursor.execute(f"INSERT INTO {customer_review}(customer_name, rating, review_text) VALUES ('{temp_customer_cart}', {rating}, '{review_text}')")
            my_con.commit()

            print("Exiting the program.")
            break

        else:
            print("Invalid choice.")
        
    print("THANK YOU!!!!!")
