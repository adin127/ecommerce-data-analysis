pip install pandas faker numpy

from faker import Faker
import pandas as pd
import random
import csv
import os
import string
from datetime import datetime
from datetime import timedelta

fake = Faker("id_ID")
random.seed(42)

os.makedirs("datasets", exist_ok=True)

import random
import string

def generate_id(prefix, length=8):
    chars = string.ascii_uppercase + string.digits

    return (
        f"{prefix}-" +
        ''.join(
            random.choices(
                chars,
                k=length
            )
        )
    )

"""## categories"""

category_names = [
    "Electronics",
    "Fashion",
    "Beauty",
    "Books",
    "Sports",
    "Home & Living",
    "Food & Beverage",
    "Automotive",
    "Health",
    "Toys"
]

categories_df = pd.DataFrame({
    "category_id": [f"CAT-{i:02d}" for i in range(1, len(category_names) + 1)],
    "category_name": category_names
})

categories_df.to_csv(
    "datasets/categories.csv",
    index=False
)

print("categories.csv selesai")

"""## customers"""

customer_ids = set()

while len(customer_ids) < 5000:
    customer_ids.add(generate_id("CUS"))

customer_ids = list(customer_ids)

# Simpan ke CSV
with open(
    "datasets/customers.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "customer_id",
        "full_name",
        "email",
        "phone",
        "gender",
        "city",
        "province",
        "created_at"
    ])

    for customer_id in customer_ids:
        writer.writerow([
            customer_id,
            fake.name(),
            fake.unique.email(),
            fake.phone_number(),
            random.choice(["Male", "Female"]),
            fake.city(),
            fake.state(),
            fake.date_time_between(
                start_date="-3y",
                end_date="now"
            )
        ])

print("customers.csv selesai")

"""## seller"""

seller_ids = set()

while len(seller_ids) < 1000:
    seller_ids.add(generate_id("SEL"))

seller_ids = list(seller_ids)

# Simpan ke CSV
with open(
    "datasets/sellers.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "seller_id",
        "seller_name",
        "city",
        "province",
        "created_at"
    ])

    for seller_id in seller_ids:
        writer.writerow([
            seller_id,
            fake.company(),
            fake.city(),
            fake.state(),
            fake.date_time_between(
                start_date="-3y",
                end_date="now"
            )
        ])

print("sellers.csv selesai")

"""## products"""

product_ids = set()

while len(product_ids) < 1000:
    product_ids.add(generate_id("PRD"))

product_ids = list(product_ids)

# Category IDs
category_ids = [f"CAT-{i:02d}" for i in range(1, 11)]

adjectives = [
    "Premium",
    "Smart",
    "Portable",
    "Wireless",
    "Modern",
    "Classic"
]

items = [
    "Laptop",
    "Headphone",
    "Camera",
    "Keyboard",
    "Book",
    "Bag",
    "Shoes",
    "Chair"
]

with open(
    "datasets/products.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "product_id",
        "seller_id",
        "category_id",
        "product_name",
        "brand",
        "price",
        "stock",
        "created_at"
    ])

    for product_id in product_ids:
        writer.writerow([
            product_id,
            random.choice(seller_ids),      # gunakan ID seller yang sudah dibuat
            random.choice(category_ids),    # gunakan ID kategori
            f"{random.choice(adjectives)} {random.choice(items)}",
            fake.company(),
            random.randint(20_000, 10_000_000),
            random.randint(0, 500),
            fake.date_time_between(
                start_date="-2y",
                end_date="now"
            )
        ])

print("products.csv selesai")

"""## orders"""

def generate_order_id():
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )
    return f"ORD-{date_part}-{random_part}"

# Generate unique order IDs
order_ids = set()

while len(order_ids) < 20000:
    order_ids.add(generate_order_id())

order_ids = list(order_ids)

statuses = [
    "Pending",
    "Paid",
    "Shipped",
    "Delivered",
    "Cancelled"
]

weights = [
    10,
    20,
    20,
    45,
    5
]

# Menyimpan informasi order untuk tabel lain
order_info = {}

with open(
    "datasets/orders.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "order_id",
        "customer_id",
        "order_date",
        "order_status"
    ])

    for order_id in order_ids:

        customer_id = random.choice(customer_ids)

        order_date = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )

        order_status = random.choices(
            statuses,
            weights=weights,
            k=1
        )[0]

        # Simpan untuk digunakan di payments & shipments
        order_info[order_id] = {
            "customer_id": customer_id,
            "order_date": order_date,
            "order_status": order_status
        }

        writer.writerow([
            order_id,
            customer_id,
            order_date,
            order_status
        ])

print("orders.csv selesai")

status_mapping = {
    "Pending": {
        "payment": "Pending",
        "shipment": "Preparing"
    },
    "Paid": {
        "payment": "Paid",
        "shipment": "Preparing"
    },
    "Shipped": {
        "payment": "Paid",
        "shipment": "Shipped"
    },
    "Delivered": {
        "payment": "Paid",
        "shipment": "Delivered"
    },
    "Cancelled": {
        "payment": "Refunded",
        "shipment": "Cancelled"
    }
}

"""## order items"""

with open(
    "datasets/order_items.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "subtotal"
    ])

    # Loop seluruh order yang sudah dibuat
    for order_id in order_ids:

        # Setiap order memiliki 2–4 produk
        n_items = random.randint(2, 4)

        for _ in range(n_items):

            quantity = random.randint(1, 5)

            unit_price = random.randint(
                20_000,
                10_000_000
            )

            subtotal = quantity * unit_price

            writer.writerow([
                generate_id("OIT"),          # ID unik
                order_id,                    # FK ke orders
                random.choice(product_ids),  # FK ke products
                quantity,
                unit_price,
                subtotal
            ])

print("order_items.csv selesai")

"""## payments"""

with open(
    "datasets/payments.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "payment_id",
        "order_id",
        "payment_method",
        "payment_status",
        "payment_date"
    ])

    for order_id, info in order_info.items():

        payment_status = status_mapping[
            info["order_status"]
        ]["payment"]

        payment_date = None

        if payment_status == "Paid":
            payment_date = (
                info["order_date"] +
                timedelta(
                    minutes=random.randint(1, 180)
                )
            )

        elif payment_status == "Refunded":
            payment_date = (
                info["order_date"] +
                timedelta(
                    days=random.randint(1, 5)
                )
            )

        writer.writerow([
            generate_id("PAY"),
            order_id,
            random.choice(payment_methods),
            payment_status,
            payment_date
        ])

print("payments.csv selesai")

"""## shippments"""

with open(
    "datasets/shipments.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "shipment_id",
        "order_id",
        "courier",
        "shipping_cost",
        "shipment_status",
        "shipped_date",
        "delivered_date"
    ])

    couriers = [
        "JNE",
        "J&T Express",
        "SiCepat",
        "AnterAja",
        "Ninja Express"
    ]

    for order_id, info in order_info.items():

        shipment_status = status_mapping[
            info["order_status"]
        ]["shipment"]

        shipped_date = None
        delivered_date = None

        if shipment_status == "Shipped":

            shipped_date = (
                info["order_date"] +
                timedelta(days=random.randint(1, 2))
            )

        elif shipment_status == "Delivered":

            shipped_date = (
                info["order_date"] +
                timedelta(days=random.randint(1, 2))
            )

            delivered_date = (
                shipped_date +
                timedelta(days=random.randint(2, 5))
            )

        writer.writerow([
            generate_id("SHP"),
            order_id,
            random.choice(couriers),
            random.randint(10000, 50000),
            shipment_status,
            shipped_date,
            delivered_date
        ])

print("shipments.csv selesai")

!zip -r ecommerce_dataset.zip /content/datasets

from google.colab import files
files.download(
    "ecommerce_dataset.zip"
)
