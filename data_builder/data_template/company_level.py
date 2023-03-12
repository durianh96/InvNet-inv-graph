import json
import pandas as pd
from typing import Optional
from utils.system_utils import file_dir_checker, file_exist_checker


class CompanyData:
    def __init__(self, company: Optional[dict] = None):
        self.company = company

    def __call__(self):
        return self.company

    def get_from_dict(self, company):
        self.company = company

    def get_from_json(self, file_dir):
        file_path = file_dir + '/company.json'
        file_exist_checker(file_path)
        with open(file_path) as json_file:
            self.company = json.load(json_file)

    def get_from_csv(self, file_dir):
        file_path = file_dir + '/company.csv'
        file_exist_checker(file_path)
        df = pd.read_csv(file_path)
        self.company = df.set_index('company_id').T.to_dict()

    def get_from_company_graph(self, company_graph):
        company = {}
        for c_id, c in company_graph.nodes_pool.items():
            company[c_id] = {'desc': c.desc, 'contained_sites': {}}
            for s_id in c.contained_dc_sites:
                company[c_id]['contained_sites'][s_id] = 'DISTRIBUTION_CENTER'
            for s_id in c.contained_mc_sites:
                company[c_id]['contained_sites'][s_id] = 'MANUFACTURING_CENTER'

        self.company = company

    def write_to_json(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/company.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.company, json_file, indent=4)

    def get_df(self):
        company_df = pd.DataFrame(self.company).T.reset_index().rename(columns={'index': 'company_id'})
        return company_df

    def write_to_csv(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/company.csv'
        df = self.get_df()
        df.to_csv(file_path, index=False)


class CompanyRelationshipData:
    def __init__(self, company_relationship: Optional[list] = None):
        self.company_relationship = company_relationship
        # company_relationship = [
        #     {'supplier': 'S1', 'buyer': 'A', 'desc': 'x'},
        #     {'supplier': 'S2', 'buyer': 'A', 'desc': 'x'},
        #     {'supplier': 'S3', 'buyer': 'B', 'desc': 'x'},
        #     {'supplier': 'S4', 'buyer': 'B', 'desc': 'x'},
        #     {'supplier': 'A', 'buyer': 'B', 'desc': 'x'},
        # ]

    def get_from_list(self, company_relationship_data):
        self.company_relationship = company_relationship_data

    def get_from_json(self, file_dir):
        file_path = file_dir + '/company_relationship.json'
        file_exist_checker(file_path)
        with open(file_path) as json_file:
            self.company_relationship = json.load(json_file)

    def get_from_csv(self, file_dir):
        file_path = file_dir + '/company_relationship.csv'
        file_exist_checker(file_path)
        df = pd.read_csv(file_path)
        self.company_relationship = list(df.T.to_dict().values())

    def get_from_company_graph(self, company_graph):
        self.company_relationship = [{'supplier': e.u, 'buyer': e.v, 'desc': e.desc}
                                     for e in company_graph.edges_pool.values()]

    def write_to_json(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/company_relationship.json'
        with open(file_path, 'w') as json_file:
            json.dump(self.company_relationship, json_file, indent=4)

    def get_df(self):
        company_relationship_df = pd.DataFrame(self.company_relationship)
        return company_relationship_df

    def write_to_csv(self, file_dir):
        file_dir_checker(file_dir)
        file_path = file_dir + '/company_relationship.csv'
        df = self.get_df()
        df.to_csv(file_path, index=False)
