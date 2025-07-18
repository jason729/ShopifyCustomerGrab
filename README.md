# Shopify Customer Grab

This program pulls customer data from a Shopify store and saves it to a CSV file.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** in the root of the project and add your Shopify credentials:
   ```
   SHOPIFY_API_KEY="YOUR_API_KEY"
   SHOPIFY_PASSWORD="YOUR_API_PASSWORD"
   SHOPIFY_SHOP_NAME="YOUR_SHOP_NAME"
   ```

## Usage

Run the program from the command line:
```bash
python main.py
```

You will be prompted to select a directory to save the `subscribed_customers.csv` file.

Alternatively, you can specify the output directory with the `-o` or `--output` flag:
```bash
python main.py -o /path/to/output/directory
```
