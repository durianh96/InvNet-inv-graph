import json
from typing import Optional
import pandas as pd
from utils.system_utils import file_exist_checker, file_dir_checker


class MakeMaterialData:
    def __init__(self, make_material: Optional[list] = None):
        if make_material is None:
            self.make_material = []
        else:
            self.make_material = make_material

    def get_from_list(self, make_material):
        self.make_material = make_material

    def get_from_json(self, file_dir):
        file_path = file_dir + '/make_material.json'
        if file_exist_checker(file_path):
            with open(file_path) as json_file:
                self.make_material = json.load(json_file)
        else:
            self.make_material = []
            raise FileNotFoundError('Not found desired file')

    def get_from_csv(self, file_dir):
        file_path = file_dir + '/make_material.csv'
        if file_exist_checker(file_path):
            try:
                df = pd.read_csv(file_path)
                self.make_material = list(df.T.to_dict().values())
            except pd.errors.EmptyDataError:
                self.make_material = []
        else:
            self.make_material = []
            raise FileNotFoundError('Not found desired file')

    def write_to_json(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/make_material.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.make_material, json_file, indent=4)

    def get_df(self):
        make_material_df = pd.DataFrame(self.make_material)
        return make_material_df

    def write_to_csv(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/make_material.csv'
        df = self.get_df()
        df.to_csv(file_path, index=False)
