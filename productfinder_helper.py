import requests
import argparse
import time
import json
from io import StringIO, BytesIO
import gzip
from bs4 import BeautifulSoup
from product import Product
import re

def download_page(record):
    offset, length = int(record['offset']), int(record['length'])
    offset_end = offset + length - 1

    prefix = 'https://data.commoncrawl.org/'
    url = prefix + record['filename']
    print(f"Downloading: {url}")

    headers = {
        'Range': f'bytes={offset}-{offset_end}',
        'User-Agent': 'Mozilla/5.0',
        'Accept-Encoding': 'identity',
    }

    try:
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        if response.status_code != 206:
            print(f"[!] Failed to fetch bytes. Status: {response.status_code}. Skipping record.")
            return None

        raw_data = BytesIO(response.raw.read())
        f = gzip.GzipFile(fileobj=raw_data)
        data = f.read()
        _, _, response_body = data.decode("utf-8", "ignore").split('\r\n', 2)

        return response_body

    except Exception as e:
        print(f"[!] Exception while downloading page: {e}")
        return None


def search_table(parsed, att, target):
    table_1 = parsed.find("table", attrs=att)
    if table_1 is None:
        return (False, None)
    table_1_rows = table_1.find_all('tr')
    found = False
    value = ""
    for row in table_1_rows:
        ths = row.find_all("th")
        tds = row.find_all("td")
        rn = ths[0].get_text()
        if target in rn:
            value = tds[0].get_text().strip()
            if len(value) > 2:
                found = True
    return (found, value) if found else (False, None)


def check_page(parsed):
    parser = parsed
    found, asin = search_table(parser, {"id": "productDetails_detailBullets_sections1"}, "ASIN")
    if found:
        return (True, asin)

    check_asin_2 = parser.find("b", text="ASIN:")
    check_asin_3 = parser.find("b", text="ASIN: ")
    check_asin_4 = parser.find("b", text="asin:")
    check_asin_5 = parser.find("b", text="asin: ")

    if not any([check_asin_2, check_asin_3, check_asin_4, check_asin_5]):
        print("Page is Not a Product")
        return (False, None)

    asin = None
    for tag in [check_asin_2, check_asin_3, check_asin_4, check_asin_5]:
        if tag:
            asin = tag.findParent().text[5:]
            break

    print("Page is a Product")
    return (True, asin)


def extract_product(html_content, url):
    string_buffer = ""
    errs = []

    parser = BeautifulSoup(html_content, "html.parser")

    # Check if the page is a product
    truth, asin = check_page(parser)
    if not truth:
        errs.append("Not product")
        return (False, errs)

    product = Product()
    product.SetUrl(url)

    # Title extraction
    title_tag = parser.find("span", attrs={"id": "productTitle"}) or parser.find("span", attrs={"id": "btAsinTitle"})
    if title_tag:
        product.SetTitle(title_tag.get_text(strip=True))
    elif url:
        product.SetTitle(url.strip("https://www.amazon.com/").split("/dp")[0])
        print("Title fallback: ", product.title)
    else:
        errs.append("Could not find Title")

    # ✅ Clean price extraction
    price_tags = [
        parser.find("span", attrs={"id": "priceblock_saleprice"}),
        parser.find("span", attrs={"id": "priceblock_ourprice"}),
        parser.find("span", attrs={"id": "priceblock_dealprice"}),
        parser.find("span", class_="a-price-whole"),
        parser.find("span", class_="a-offscreen"),
    ]

    price = None
    for tag in price_tags:
        if tag:
            raw = tag.get_text(strip=True)
            cleaned = raw.replace("$", "").replace(",", "").strip()
            try:
                price_float = float(cleaned)
                price = f"${price_float:.2f}"
                break
            except ValueError:
                continue

    if price:
        product.SetPrice(price)
    else:
        errs.append("Could not find valid Price")

    # ASIN
    product.SetSourceID(asin)

    # Rating
    rating_tag = parser.find("span", attrs={"id": "acrCustomerReviewText"})
    if rating_tag:
        rating_raw = rating_tag.get_text().split()[0].replace(",", "")
        if rating_raw.isdigit():
            product.SetRating(rating_raw)
        else:
            errs.append("Invalid rating format")

    # Final validation
    if product.FormCompleted():
        return (product, errs)
    else:
        return (False, errs)


# Test runner
if __name__ == '__main__':
    print("Script Starting")
    html = open("test_html/amazon3.html")
    url = "https://www.amazon.com/100-Wisconsin-CHEDDAR-CHEESE-Packages/dp/B00FROANTC"
    products = []
    product, errs = extract_product(html, url)
    if product:
        products.append(product)
        product.Print()
        print("[Success Append]")
    else:
        print("Returned False")
    if errs:
        print("[Errors:]")
        for err in errs:
            print(" *  {}".format(err))
    print("Script Finished")
