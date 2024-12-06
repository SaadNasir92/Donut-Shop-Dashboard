import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Employee details

owners = ["Alice", "Bob", "Charlie"]  # Permanent owners
employees_2021_2025 = ["Frank", "Grace", "Hannah"]  # Employees from 2021-2025
employees_2025 = owners + employees_2021_2025

# Product details
products = {
    "Daring Donut": "Donut",
    "Donut Odyssey": "Donut",
    "Glaze": "Donut",
    "Boston Creme": "Donut",
    "Blueberry": "Donut",
    "Strawberry": "Donut",
    "Chocolate": "Donut",
    "Chocolate Sprinkle": "Donut",
    "Cinnamon Swirl": "Donut",
    "Glaze Donut Hole": "Donut",
    "Chocolate Donut Hole": "Donut",
    "Blueberry Donut Hole": "Donut",
    "Frosted Donut": "Donut",
    "Frosted Donut Sprinkle": "Donut",
    "Jalapeno Hot Dog": "Hot Foods",
    "Croissant Hot Dog": "Hot Foods",
    "Biscuits": "Hot Foods",
    "Ham and Cheese": "Hot Foods",
    "Small Hot Dog": "Hot Foods",
    "Sprite": "Drinks",
    "Coke": "Drinks",
    "Diet Coke": "Drinks",
    "Starbucks Mocha": "Drinks",
    "Starbucks Caramel": "Drinks",
    "Redbull": "Drinks",
    "Coffee": "Drinks",
    "Tropicana": "Drinks",
}

product_list = list(products.keys())


# Pricing details
def get_price(product_name):
    category = products[product_name]
    if category == "Donut":
        return 1.00
    elif category == "Hot Foods":
        return 3.00
    elif category == "Drinks":
        return 2.00


# Promotions
promotions = {
    "BOGO": {"discount": None},  # Buy One Get One Free
    "WINTER SPECIAL": {"discount": 0.50},  # 50% off everything
}


# Function to determine payment method
def get_payment_method():
    card_percentage = 0.80  # 80% card payments in 2025
    return "Card" if np.random.rand() < card_percentage else "Cash"


# Generate the dataset
data = []
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 1, 12)
current_date = start_date

while current_date <= end_date:
    num_transactions = np.random.randint(100, 151)  # 100–150 transactions per day
    for _ in range(num_transactions):
        # Generate transaction timestamp
        transaction_date = current_date + timedelta(
            hours=np.random.randint(0, 24),
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
        )
        timestamp = transaction_date.strftime("%Y-%m-%d %H:%M:%S")

        # Select employee
        employee_name = random.choice(employees_2025)

        # Determine number of items in transaction
        num_items = np.random.randint(1, 6)  # 1–5 items

        # Determine payment method
        payment_method = get_payment_method()

        # Check for promotions
        promo_name = ""
        discount_rate = 0.0
        apply_promo = np.random.rand() < 0.33  # 33% chance

        if apply_promo:
            promo_name = random.choice(list(promotions.keys()))
            discount_rate = (
                promotions[promo_name]["discount"] if promo_name != "BOGO" else 0.0
            )

        # Generate items
        for _ in range(num_items):
            product_name = random.choice(product_list)
            category = products[product_name]
            price_per_unit = get_price(product_name)
            quantity = np.random.randint(1, 5)  # 1–4 units
            discount_amount = 0.0

            # Apply discount
            if promo_name:
                if promo_name == "BOGO" and category in ["Donut", "Hot Foods"]:
                    free_items = quantity // 2
                    discount_amount = free_items * price_per_unit
                elif promo_name == "WINTER SPECIAL":
                    discount_amount = quantity * price_per_unit * discount_rate

            # Calculate amounts
            subtotal = (quantity * price_per_unit) - discount_amount
            tax_amount = subtotal * 0.0625  # Tax rate is 6.25%
            total_amount = subtotal + tax_amount

            # Append to data
            data.append(
                {
                    "Employee Name": employee_name,
                    "Product Name": product_name,
                    "Category": category,
                    "Date": timestamp,
                    "Subtotal": round(subtotal, 2),
                    "Tax Amount": round(tax_amount, 2),
                    "Total Amount": round(total_amount, 2),
                    "Payment Method": payment_method,
                    "Discount Amount": round(discount_amount, 2),
                    "Promo Name": promo_name,
                    "Quantity": quantity,
                    "Price per Unit": round(price_per_unit, 2),
                }
            )
    current_date += timedelta(days=1)

# Create DataFrame
df = pd.DataFrame(data)

# Reorder columns
df = df[
    [
        "Employee Name",
        "Product Name",
        "Category",
        "Date",
        "Subtotal",
        "Tax Amount",
        "Total Amount",
        "Payment Method",
        "Discount Amount",
        "Promo Name",
        "Quantity",
        "Price per Unit",
    ]
]

# Save to CSV
df.to_csv("datasets/donut_shop_transactions_jan12.csv", index=False)
