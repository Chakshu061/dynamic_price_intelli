from bs4 import BeautifulSoup
from product import Product
import requests
import json
import re
import productfinder_helper

## Edited and adapted from David Cedar(2017)

class ProductFinder:
    
    record_list = list()
    save_thread = list()
    
    def __init__(self, record_list):
        self.record_list = record_list

    def update(self):  # ← This must be indented to be part of the class
        i = 0
        for record in self.record_list:
            i += 1
            if len(record['url']) > 23 and record['url'].count('%') < 5 and record['url'].count('artist-redirect') < 1:
                print("[{} of {}]".format(i, len(self.record_list)))

                html_content = productfinder_helper.download_page(record)
                
                if html_content is None:
                    print("[!] Skipping record: could not retrieve page content")
                    continue

                print("[*] Retrieved {} bytes for {}".format(len(html_content), record['url']))

                product, errs = productfinder_helper.extract_product(html_content, record['url'])
                print("Product: ", product)
                print("errs: ", errs)

                if product:
                    self.save_thread.append(product)
                    print("[Success Append]")
                    if errs:
                        print("[Errors:]")
                        for err in errs:
                            print(" *  {}".format(err))
                else:
                    print("Failed to EXTRACT Product")

        return self.save_thread
