import pandas as pd
import random

# Set seed for reproducibility
random.seed(42)

# Items by category
inventory_items = {
    "Main Course": [
        "Chicken Burger",
        "Veg Burger",
        "Pizza",
        "Pasta",
        "Biryani",
        "Fried Rice",
        "Noodles",
        "Grilled Chicken",
        "Paneer Curry",
        "Steak"
    ],
    "Beverages": [
        "Coke",
        "Pepsi",
        "Sprite",
        "Coffee",
        "Tea",
        "Orange Juice",
        "Lemonade",
        "Milkshake"
    ],
    "Desserts": [
        "Ice Cream",
        "Brownie",
        "Cheesecake",
        "Chocolate Cake",
        "Donut"
    ],
    "Snacks": [
        "French Fries",
        "Garlic Bread",
        "Chicken Wings",
        "Nachos",
        "Spring Rolls"
    ]
}

suppliers = [
    "Fresh Foods Ltd",
    "Global Traders",
    "Food Supply Co",
    "Prime Distributors",
    "Quality Foods",
    "ABC Suppliers"
]

inventory = []

for category, items in inventory_items.items():

    for item in items:

        stock = random.randint(10, 300)

        reorder = random.randint(20, 60)

        unit_price = round(random.uniform(1.50, 25.00), 2)

        supplier = random.choice(suppliers)

        inventory.append([
            item,
            category,
            stock,
            reorder,
            supplier,
            unit_price
        ])

df = pd.DataFrame(
    inventory,
    columns=[
        "Item",
        "Category",
        "Stock",
        "Reorder_Level",
        "Supplier",
        "Unit_Price"
    ]
)

# Add Stock Status column
df["Stock_Status"] = df["Stock"].apply(
    lambda x: "Low Stock" if x < 50 else "In Stock"
)

# Save CSV
df.to_csv("data/inventory.csv", index=False)

print("Inventory dataset created successfully!")
print(df.head())