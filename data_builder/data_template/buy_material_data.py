import json
from typing import Optional
import pandas as pd
from utils.system_utils import file_exist_checker, file_dir_checker


class BuyMaterialData:
    def __init__(self, buy_material: Optional[list] = None):
        if buy_material is None:
            self.buy_material = []
        else:
            self.buy_material = buy_material

    def get_from_list(self, buy_material):
        self.buy_material = buy_material

    def get_from_json(self, file_dir):
        file_path = file_dir + '/buy_material.json'
        if file_exist_checker(file_path):
            with open(file_path) as json_file:
                self.buy_material = json.load(json_file)
        else:
            self.buy_material = []
            raise FileNotFoundError('Not found desired file')

    def get_from_csv(self, file_dir):
        file_path = file_dir + '/buy_material.csv'
        if file_exist_checker(file_path):
            try:
                df = pd.read_csv(file_path)
                self.buy_material = list(df.T.to_dict().values())
            except pd.errors.EmptyDataError:
                self.buy_material = []
        else:
            self.buy_material = []
            raise FileNotFoundError('Not found desired file')

    def write_to_json(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/buy_material.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.buy_material, json_file, indent=4)

    def get_df(self):
        buy_material_df = pd.DataFrame(self.buy_material)
        return buy_material_df

    def write_to_csv(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/buy_material.csv'
        df = self.get_df()
        df.to_csv(file_path, index=False)
