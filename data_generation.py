import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Employee details
owners = ["Alice", "Bob", "Charlie"]  # Permanent owners
employees_2015_2021 = ["David", "Eva"]  # Employees from 2015-2021
employees_2021_2025 = ["Frank", "Grace", "Hannah"]  # Employees from 2021-2025


# Function to get employees based on year
def get_employees(year):
    if year <= 2021:
        return owners + employees_2015_2021
    else:
        return owners + employees_2021_2025


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
def get_price(product_name, year):
    category = products[product_name]
    if year < 2020:
        if category == "Donut":
            return 0.50
        elif category == "Hot Foods":
            return 1.50
        elif category == "Drinks":
            return 1.25
    else:
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
    "Back to School": {
        "discount": 0.25
    },  # 25% off everything during first week of September
}


# Function to determine payment method
def get_payment_method(year):
    start_year = 2015
    end_year = 2025
    card_percentage_start = 0.60
    card_percentage_end = 0.80
    total_years = end_year - start_year
    year_index = year - start_year
    card_percentage = card_percentage_start + (
        card_percentage_end - card_percentage_start
    ) * (year_index / total_years)
    return "Card" if np.random.rand() < card_percentage else "Cash"


# Number of transactions per year
transactions_per_year = {
    2015: 15000,
    2016: 17000,
    2017: 19000,
    2018: 21000,
    2019: 23000,
    2020: 12000,  # COVID year
    2021: 29000,
    2022: 35000,
    2023: 38000,
    2024: 43000,
}

# Generate the dataset
data = []

for year in range(2015, 2025):
    num_transactions = transactions_per_year[year]
    employees = get_employees(year)
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    date_range = (end_date - start_date).days + 1

    for _ in range(num_transactions):
        # Generate transaction timestamp
        days_offset = np.random.randint(0, date_range)
        transaction_date = start_date + timedelta(
            days=days_offset,
            hours=np.random.randint(0, 24),
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
        )
        timestamp = transaction_date.strftime("%Y-%m-%d %H:%M:%S")

        # Select employee
        employee_name = random.choice(employees)

        # Determine number of items in transaction
        num_items = np.random.randint(1, 6)  # Between 1 and 5 items

        # Determine payment method
        payment_method = get_payment_method(year)

        # Check for promotions
        promo_name = ""
        discount_rate = 0.0
        apply_promo = np.random.rand() < 0.33  # 33% chance

        if apply_promo:
            # Select promotion
            possible_promos = ["BOGO", "WINTER SPECIAL", "Back to School"]
            promo_name = random.choice(possible_promos)

            # Check if promotion is valid on this date
            if promo_name == "WINTER SPECIAL":
                if transaction_date.month in [12, 1, 2]:
                    discount_rate = promotions[promo_name]["discount"]
                else:
                    promo_name = ""
            elif promo_name == "Back to School":
                if transaction_date.month == 9 and transaction_date.day <= 7:
                    discount_rate = promotions[promo_name]["discount"]
                else:
                    promo_name = ""
            elif promo_name == "BOGO":
                discount_rate = None  # Special handling for BOGO

        # Generate items
        for _ in range(num_items):
            product_name = random.choice(product_list)
            category = products[product_name]
            price_per_unit = get_price(product_name, year)
            quantity = np.random.randint(1, 5)  # Between 1 and 4 units
            discount_amount = 0.0

            # Apply discount
            if promo_name:
                if promo_name == "BOGO" and category in ["Donut", "Hot Foods"]:
                    free_items = quantity // 2
                    discount_amount = free_items * price_per_unit
                elif promo_name == "WINTER SPECIAL":
                    discount_amount = quantity * price_per_unit * discount_rate
                elif promo_name == "Back to School":
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
df.to_csv("donut_shop_transactions.csv", index=False)

print("Dataset generated and saved to 'donut_shop_transactions.csv'")
