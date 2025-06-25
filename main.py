from productfinder import ProductFinder
from save_local import SaveProducts
from commoncrawler import search_domain, record_is_product, record_status_bad

def main():
    domain = "amazon.com"
    index_list = ["2019-04"]

    record_list = []
    for index in index_list:
        record_list += search_domain(domain, index)

    print(f"[*] Total raw records: {len(record_list)}")

    cleaned_list = list(filter(record_status_bad, record_list))
    product_records = list(filter(record_is_product, cleaned_list))

    print(f"[*] Product pages found: {len(product_records)}")

    product_finder = ProductFinder(product_records)
    products = product_finder.update()

    saver = SaveProducts(products)
    saver.update()

if __name__ == "__main__":
    main()
