import json
import os

class SaveProducts:
    def __init__(self, products_buffer, save_path='data/products.json'):
        self.products_buffer = products_buffer
        self.save_path = save_path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

    def update(self):
        print(f"[*] Saving {len(self.products_buffer)} products locally.")
        product_dicts = [product.ReturnJson() for product in self.products_buffer]

        with open(self.save_path, 'w') as f:
            json.dump(product_dicts, f, indent=2)

        print(f"[✔] Saved to {self.save_path}")
