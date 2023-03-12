import json
from typing import Optional
import pandas as pd
from utils.system_utils import file_exist_checker, file_dir_checker


class SiteMaterialData:
    def __init__(self, site_material: Optional[list] = None):
        if site_material is None:
            self.site_material = []
        else:
            self.site_material = site_material

    def get_from_list(self, site_material):
        self.site_material = site_material

    def get_from_json(self, file_dir):
        file_path = file_dir + '/site_material.json'
        if file_exist_checker(file_path):
            with open(file_path) as json_file:
                self.site_material = json.load(json_file)
        else:
            self.site_material = []
            raise FileNotFoundError('Not found desired file')

    def get_from_csv(self, file_dir):
        file_path = file_dir + '/site_material.csv'
        if file_exist_checker(file_path):
            try:
                df = pd.read_csv(file_path)
                self.site_material = list(df.T.to_dict().values())
            except pd.errors.EmptyDataError:
                self.site_material = []
        else:
            self.site_material = []
            raise FileNotFoundError('Not found desired file')

    def write_to_json(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/site_material.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.site_material, json_file, indent=4)

    def get_df(self):
        site_material_df = pd.DataFrame(self.site_material)
        return site_material_df

    def write_to_csv(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/site_material.csv'
        df = self.get_df()
        df.to_csv(file_path, index=False)
