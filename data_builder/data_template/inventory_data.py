import json
from typing import Optional
import pandas as pd
from utils.system_utils import file_exist_checker, file_dir_checker


class InventoryData:
    def __init__(self, inventory: Optional[list] = None):
        if inventory is None:
            self.inventory = []
        else:
            self.inventory = inventory

    def get_from_list(self, inventory):
        self.inventory = inventory

    def get_from_json(self, file_dir):
        file_path = file_dir + '/inventory.json'
        if file_exist_checker(file_path):
            with open(file_path) as json_file:
                self.inventory = json.load(json_file)
        else:
            self.inventory = []
            raise FileNotFoundError('Not found desired file')

    def get_from_csv(self, file_dir):
        file_path = file_dir + '/inventory.csv'
        if file_exist_checker(file_path):
            try:
                df = pd.read_csv(file_path)
                self.inventory = list(df.T.to_dict().values())
            except pd.errors.EmptyDataError:
                self.inventory = []
        else:
            self.inventory = []
            raise FileNotFoundError('Not found desired file')

    def write_to_json(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/inventory.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.inventory, json_file, indent=4)

    def get_df(self):
        inventory_df = pd.DataFrame(self.inventory)
        return inventory_df

    def write_to_csv(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/inventory.csv'
        df = self.get_df()
        df.to_csv(file_path, index=False)
