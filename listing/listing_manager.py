import csv

def prepare_listings(products):
    print("📝 Creating product listing drafts...")
    with open("data/products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
