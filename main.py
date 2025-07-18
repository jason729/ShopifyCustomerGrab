import csv
import shopify
import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch credentials from environment variables
API_KEY = os.getenv("SHOPIFY_API_KEY")
API_PASSWORD = os.getenv("SHOPIFY_PASSWORD")
SHOP_NAME = os.getenv("SHOPIFY_SHOP_NAME")

# Set up argument parsing
parser = argparse.ArgumentParser(description="Fetch subscribed Shopify customers and save to a CSV file.")
parser.add_argument("--output", "-o", required=True, help="Directory to save the CSV file.")
args = parser.parse_args()

# Validate the output directory
output_folder = args.output
if not os.path.isdir(output_folder):
    print(f"Error: Output directory '{output_folder}' does not exist.")
    exit(1)

# Print credentials for debugging
print(f"Shop Name: {SHOP_NAME}")
print(f"API Key: {API_KEY}")
print(f"API Password: {API_PASSWORD}")

# Set up the Shopify session
shop_url = f"https://{API_KEY}:{API_PASSWORD}@{SHOP_NAME}.myshopify.com/admin/api/2023-10"
shopify.ShopifyResource.set_site(shop_url)
print(f"Shop URL: {shop_url}")

# Function to fetch all customers with pagination
def fetch_all_customers():
    all_customers = []
    since_id = 0
    page_count = 1  # Track the page number
    total_customers_fetched = 0  # Track the total number of customers fetched

    while True:
        # Fetch a page of customers
        print(f"Fetching page {page_count}...")
        customers = shopify.Customer.find(limit=250, since_id=since_id)
        if not customers:
            break  # No more customers to fetch

        # Add the fetched customers to the list
        all_customers.extend(customers)
        total_customers_fetched += len(customers)
        print(f"Fetched {len(customers)} customers (Total so far: {total_customers_fetched})")

        # Update since_id to the last customer's ID
        since_id = customers[-1].id
        page_count += 1  # Increment the page count

    return all_customers

# Fetch all customers
customers = fetch_all_customers()

# Filter subscribed customers
subscribed_customers = []
for customer in customers:
    # Check if email_marketing_consent exists and is subscribed
    if hasattr(customer, 'email_marketing_consent') and customer.email_marketing_consent:
        if customer.email_marketing_consent.state == 'subscribed':
            subscribed_customers.append(customer)

# Save subscribed customers to a CSV file
output_file_path = os.path.join(output_folder, 'subscribed_customers.csv')
with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Email', 'First Name', 'Last Name'])
    for customer in subscribed_customers:
        writer.writerow([customer.id, customer.email, customer.first_name, customer.last_name])

print(f"Subscribed customers saved to '{output_file_path}'. Total subscribed: {len(subscribed_customers)}")

# Clear the session
shopify.ShopifyResource.clear_session()
