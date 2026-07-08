import pandas as pd
import random

random.seed(42)

first_names = [
    "John","David","James","Michael","Daniel",
    "Robert","Thomas","William","Joseph","Kevin",
    "Emma","Sophia","Olivia","Ava","Charlotte",
    "Mia","Amelia","Harper","Evelyn","Grace"
]

roles = [
    "Manager",
    "Chef",
    "Sous Chef",
    "Waiter",
    "Cashier",
    "Kitchen Porter",
    "Cleaner"
]

shift = [
    "Morning",
    "Afternoon",
    "Evening"
]

status = [
    "Active",
    "On Leave"
]

rows = []

for emp_id in range(1, 101):

    role = random.choice(roles)

    salary = random.randint(1600, 4200)

    experience = random.randint(1, 15)

    performance = random.randint(70, 100)

    attendance = random.randint(80, 100)

    overtime = random.randint(0, 40)

    rows.append([
        emp_id,
        random.choice(first_names),
        role,
        random.choice(shift),
        salary,
        experience,
        performance,
        attendance,
        overtime,
        random.choice(status)
    ])

df = pd.DataFrame(
    rows,
    columns=[
        "Employee_ID",
        "Employee_Name",
        "Role",
        "Shift",
        "Salary",
        "Experience_Years",
        "Performance_Score",
        "Attendance_Percentage",
        "Overtime_Hours",
        "Status"
    ]
)

df.to_csv("data/employees.csv", index=False)

print("✅ employees.csv created successfully!")
print(df.head())
