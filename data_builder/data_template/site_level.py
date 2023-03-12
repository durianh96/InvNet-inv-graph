import json
import pandas as pd
from typing import Optional
from utils.system_utils import file_dir_checker, file_exist_checker


class SiteData:
    def __init__(self, site: Optional[dict] = None):
        self.site = site

    def get_from_dict(self, site):
        self.site = site

    def get_from_json(self, file_dir):
        file_path = file_dir + '/site.json'
        file_exist_checker(file_path)
        with open(file_path) as json_file:
            self.site = json.load(json_file)

    def get_from_csv(self, file_dir):
        file_path = file_dir + '/site.csv'
        file_exist_checker(file_path)
        df = pd.read_csv(file_path)
        self.site = df.set_index('site_id').T.to_dict()

    def get_from_site_graph(self, site_graph):
        self.site = {s_id: {'desc': s.desc, 'loc': s.loc, 'company_id': s.company_id, 'site_type': s.node_type}
                     for s_id, s in site_graph.nodes_pool.items()}

    def write_to_json(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/site.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.site, json_file, indent=4)

    def get_df(self):
        site_df = pd.DataFrame(self.site).T.reset_index().rename(columns={'index': 'site_id'})
        return site_df

    def write_to_csv(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/site.csv'
        df = self.get_df()
        df.to_csv(file_path, index=False)


class SiteRelationshipData:
    def __init__(self, site_relationship: Optional[list] = None):
        self.site_relationship = site_relationship

    def get_from_list(self, site_relationship):
        self.site_relationship = site_relationship

    def get_from_json(self, file_dir):
        file_path = file_dir + '/site_relationship.json'
        file_exist_checker(file_path)
        with open(file_path) as json_file:
            self.site_relationship = json.load(json_file)

    def get_from_csv(self, file_dir):
        file_path = file_dir + '/site_relationship.csv'
        file_exist_checker(file_path)
        df = pd.read_csv(file_path)
        self.site_relationship = list(df.T.to_dict().values())

    def get_from_site_graph(self, site_graph):
        self.site_relationship = [{'from': e.u, 'to': e.v, 'desc': e.desc, 'transit_lt': e.transit_lt}
                                  for e in site_graph.edges_pool.values()]

    def write_to_json(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/site_relationship.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.site_relationship, json_file, indent=4)

    def get_df(self):
        site_relationship_df = pd.DataFrame(self.site_relationship)
        return site_relationship_df

    def write_to_csv(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/site_relationship.csv'
        df = self.get_df()
        df.to_csv(file_path, index=False)
