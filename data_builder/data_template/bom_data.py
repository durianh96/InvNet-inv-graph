import json
from typing import Optional
import pandas as pd
from utils.system_utils import file_exist_checker, file_dir_checker


class BOMData:
    def __init__(self, bom: Optional[list] = None):
        if bom is None:
            self.bom = []
        else:
            self.bom = bom

    def __call__(self):
        return self.bom

    @property
    def used_in_manu_site_of_material(self):
        material_ids = set([b['component'] for b in self.bom]) | set([b['assembly'] for b in self.bom])
        used_in_manu_site_of_material = {material_id: set() for material_id in material_ids}
        for b in self.bom:
            used_in_manu_site_of_material[b['component']].add(b['manu_site'])
            used_in_manu_site_of_material[b['assembly']].add(b['manu_site'])
        return used_in_manu_site_of_material

    def get_from_list(self, bom):
        self.bom = bom

    def get_from_json(self, file_dir):
        file_path = file_dir + '/bom.json'
        if file_exist_checker(file_path):
            with open(file_path) as json_file:
                self.bom = json.load(json_file)
        else:
            self.bom = []
            raise FileNotFoundError('Not found desired file')

    def get_from_csv(self, file_dir):
        file_path = file_dir + '/bom.csv'
        if file_exist_checker(file_path):
            try:
                df = pd.read_csv(file_path)
                self.bom = list(df.T.to_dict().values())
            except pd.errors.EmptyDataError:
                self.bom = []
        else:
            self.bom = []
            raise FileNotFoundError('Not found desired file')

    def write_to_json(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/bom.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.bom, json_file, indent=4)

    def get_df(self):
        bom_df = pd.DataFrame(self.bom)
        return bom_df

    def write_to_csv(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/bom.csv'
        df = self.get_df()
        df.to_csv(file_path, index=False)
