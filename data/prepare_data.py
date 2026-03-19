import csv
import random
import os

def generate_sample_data(n=100):
    """Generate and clean sample listing data (simulating data.gouv.fr)"""
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # Generate raw data
    raw_rows = []
    for i in range(n):
        raw_rows.append({
            "id": i,
            "price": random.randint(100000, 800000),
            "surface": random.randint(20, 150),
            "description_length": random.randint(10, 300),
            "photo_count": random.randint(0, 15),
            "location_precision": random.choice(["street", "district", "city"]),
            "rooms": random.randint(0, 6)
        })

    # Save raw data
    with open("data/raw/listings.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=raw_rows[0].keys())
        writer.writeheader()
        writer.writerows(raw_rows)

    # Clean: remove listings with surface = 0
    processed_rows = [r for r in raw_rows if r["surface"] > 0]

    # Save processed data
    with open("data/processed/listings_clean.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=processed_rows[0].keys())
        writer.writeheader()
        writer.writerows(processed_rows)

    print(f"Raw: {len(raw_rows)} rows -> Processed: {len(processed_rows)} rows")
    print("Saved to data/raw/listings.csv and data/processed/listings_clean.csv")

if __name__ == "__main__":
    generate_sample_data()