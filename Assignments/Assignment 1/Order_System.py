# Name: Touseef Ali
# Batch: 2
# Roll: 405895

import csv
import os
from datetime import datetime
from functools import wraps

if not os.path.exists('products.csv'):
    with open('products.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'price'])
        writer.writerows([
            [1, 'Laptop', 1200],
            [2, 'Phone', 800],
            [3, 'Headphones', 150],
            [4, 'Mouse', 40],
            [5, 'Keyboard', 60]
        ])

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('log.txt', 'a') as log_file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f'[{timestamp}] Executed {func.__name__}\n')
        return result
    return wrapper

class Order:
    discount_rate = 0.0 

    def __init__(self):
        self.items = []
    
    @log_action
    def add_item_by_id(self, product_id, quantity):
        if not Order.is_valid_product_id(product_id):
            with open('log.txt', 'a') as log_file:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_file.write(f'[{timestamp}] Invalid product ID attempt: {product_id}\n')
            return False
        
        with open('products.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['id']) == product_id:
                    name = row['name']
                    price = float(row['price'])
                    self.items.append((product_id, name, price, quantity))
                    total = price * quantity
                    with open('log.txt', 'a') as log_file:
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        log_file.write(f'[{timestamp}] Added item: {name} (x{quantity}) - Total: {total}\n')
                    return True
        return False
    
    @log_action
    def calculate_total(self):
        total = sum(price * quantity for _, _, price, quantity in self.items)
        discount_amount = total * Order.discount_rate
        final_total = total - discount_amount
        with open('log.txt', 'a') as log_file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f'[{timestamp}] Calculated total with discount: {final_total}\n')
        return final_total
    
    @classmethod
    @log_action
    def set_discount(cls, discount_rate):
        cls.discount_rate = discount_rate / 100.0
        with open('log.txt', 'a') as log_file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f'[{timestamp}] Discount set to {discount_rate}%\n')
    
    @staticmethod
    def is_valid_product_id(product_id):
        with open('products.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['id']) == product_id:
                    return True
        return False

if __name__ == "__main__":
    order = Order()
    order.add_item_by_id(1, 2) 
    order.add_item_by_id(4, 3)
    order.add_item_by_id(99, 1)  
    Order.set_discount(10)
    total = order.calculate_total()
    print(f"Final Order Total: ${total:.2f}")
    print("\nLog file contents:")
    with open('log.txt', 'r') as log_file:
        print(log_file.read())