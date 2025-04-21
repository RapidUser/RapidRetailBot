from scraper.multi_site_scraper import scrape_products
from analyzer.product_analyzer import analyze_products
from sourcing.supplier_finder import find_suppliers
from listing.listing_manager import prepare_listings
import os

def main():
    print("🚀 Starting RapidRetailBot...")
    products = scrape_products()
    if not products:
        print("❌ No products found.")
        return

    print("✅ Products scraped. Analyzing...")
    analyzed = analyze_products(products)

    print("🔍 Finding suppliers...")
    with_suppliers = find_suppliers(analyzed)

    print("📦 Preparing listings...")
    prepare_listings(with_suppliers)

    print("🎉 Done. Results saved to data/products.csv")

if __name__ == "__main__":
    main()
