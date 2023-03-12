import json
from typing import Optional
import pandas as pd
from utils.system_utils import file_exist_checker, file_dir_checker


class OrderData:
    def __init__(self, order: Optional[list] = None):
        if order is None:
            self.order = []
        else:
            self.order = order

        self.order_df = None
        self.order_grouped = None
        self.material_sale_sites = None
        if order is not None:
            self.info_update()

    def get_from_list(self, order):
        self.order = order
        self.info_update()

    def get_from_json(self, file_dir):
        file_path = file_dir + '/order.json'
        if file_exist_checker(file_path):
            with open(file_path) as json_file:
                self.order = json.load(json_file)
        else:
            self.order = []
            raise FileNotFoundError('Not found desired file')

        if len(self.order) > 0:
            self.info_update()

    def get_from_csv(self, file_dir):
        file_path = file_dir + '/order.csv'
        if file_exist_checker(file_path):
            try:
                df = pd.read_csv(file_path)
                self.order = list(df.T.to_dict().values())
            except pd.errors.EmptyDataError:
                self.order = []
        else:
            self.order = []
            raise FileNotFoundError('Not found desired file')

        if len(self.order) > 0:
            self.info_update()

    def write_to_json(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/order.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.order, json_file, indent=4)

    def write_to_csv(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/order.csv'
        df = self.get_df()
        df.to_csv(file_path, index=False)

    def info_update(self):
        self.get_df()
        self.get_order_grouped()
        self.get_material_sale_sites()

    def get_df(self):
        order_df = pd.DataFrame(self.order)
        self.order_df = order_df
        return order_df

    def get_order_grouped(self):
        if self.order_df is None:
            order_df = self.get_df()
        else:
            order_df = self.order_df
        order_grouped = order_df.groupby(['material_id', 'fulfill_site'])[[
            'order_date', 'order_qty']].apply(lambda x: x.values.tolist()).to_dict()
        self.order_grouped = order_grouped
        return order_grouped

    def get_material_sale_sites(self):
        if self.order_df is None:
            order_df = self.get_df()
        else:
            order_df = self.order_df
        material_sale_sites = order_df.groupby('material_id')['fulfill_site'] \
            .apply(lambda x: set(x.values.tolist())).to_dict()
        self.material_sale_sites = material_sale_sites
        return material_sale_sites

    def get_material_site_order(self, material_id, site_id):
        if self.order_grouped is None:
            self.get_order_grouped()
        material_site_order = self.order_grouped.get((material_id, site_id), [])
        material_site_order = [(date, qty) for date, qty in material_site_order if qty > 0]
        return material_site_order

    def get_agg_order_df(self, agg_para='D'):
        order_df = self.get_df()
        order_df['order_date'] = pd.to_datetime(order_df['order_date'])
        agg_order_df = order_df.groupby(['material_id', 'fulfill_site'])[[
            'order_date', 'order_qty']].resample(agg_para, on='order_date').sum().reset_index()
        return agg_order_df
