import json
from typing import Optional
import pandas as pd
from utils.system_utils import file_exist_checker, file_dir_checker


class ProductData:
    def __init__(self, product: Optional[list] = None):
        if product is None:
            self.product = []
        else:
            self.product = product

    def get_from_list(self, product):
        self.product = product

    def get_from_json(self, file_dir):
        file_path = file_dir + '/product.json'
        if file_exist_checker(file_path):
            with open(file_path) as json_file:
                self.product = json.load(json_file)
        else:
            self.product = []
            raise FileNotFoundError('Not found desired file')

    def get_from_csv(self, file_dir):
        file_path = file_dir + '/product.csv'
        if file_exist_checker(file_path):
            df = pd.read_csv(file_path)
            self.product = list(df.T.to_dict().values())
        else:
            self.product = []
            raise FileNotFoundError('Not found desired file')

    def write_to_json(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/product.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.product, json_file, indent=4)

    def get_df(self):
        product_df = pd.DataFrame(self.product)
        return product_df

    def write_to_csv(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/product.csv'
        df = self.get_df()
        df.to_csv(file_path, index=False)
