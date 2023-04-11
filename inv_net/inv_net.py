from data_builder.graph_builder.company_graph_builder import default_company_graph_builder
from data_builder.graph_builder.site_graph_builder import default_site_graph_builder
from data_builder.graph_builder.material_graph_builder import default_material_graph_builder
from inv_net.graph import *
from data_builder.data_template.company_level import *
from data_builder.data_template.site_level import *
from data_builder.data_template.company_detail_data import CompanyDetailData
from utils.system_utils import file_dir_checker


class InvNet:
    def __init__(self, company_graph: Optional[CompanyGraph] = None,
                 site_graph: Optional[SiteGraph] = None,
                 material_graph: Optional[MaterialGraph] = None,
                 detail_data_pool: Optional[dict] = None
                 ):
        self._company_graph = company_graph
        self._site_graph = site_graph
        self._material_graph = material_graph
        if detail_data_pool is None:
            self._detail_data_pool = {}
        else:
            self._detail_data_pool = detail_data_pool

    @property
    def company_graph(self):
        return self._company_graph

    @property
    def site_graph(self):
        return self._site_graph

    @property
    def material_graph(self):
        return self._material_graph

    @property
    def detail_data_pool(self):
        return self._detail_data_pool

    def update_company_graph(self, new_company_graph):
        self._company_graph = new_company_graph

    def update_site_graph(self, new_site_graph):
        self._site_graph = new_site_graph

    def update_material_graph(self, new_material_graph):
        self._material_graph = new_material_graph

    def update_detail_data_pool(self, new_detail_data_pool):
        self._detail_data_pool = new_detail_data_pool

    def write_all_to_file(self, root_file_dir, file_type='json'):
        """
        It writes all the data in the data pool to files

        Args:
          root_file_dir: the directory where you want to save the data
          file_type: the type of file you want to write to. Defaults to json
        """
        file_dir_checker(root_file_dir)
        # get company level data
        company_data = CompanyData()
        company_data.get_from_company_graph(self.company_graph)
        company_relationship_data = CompanyRelationshipData()
        company_relationship_data.get_from_company_graph(self.company_graph)

        # get site level data
        site_data = SiteData()
        site_data.get_from_site_graph(self.site_graph)
        site_relationship_data = SiteRelationshipData()
        site_relationship_data.get_from_site_graph(self.site_graph)

        if file_type == 'csv':
            # write company level data
            company_data.write_to_csv(root_file_dir)
            company_relationship_data.write_to_csv(root_file_dir)
            # write site level data
            site_data.write_to_csv(root_file_dir)
            site_relationship_data.write_to_csv(root_file_dir)
            # write detail data
            for c_id, c_detail in self._detail_data_pool.items():
                file_dir = root_file_dir + '/' + c_id
                c_detail.write_all_to_csv(file_dir)
        else:
            company_data.write_to_json(root_file_dir)
            company_relationship_data.write_to_json(root_file_dir)

            site_data.write_to_json(root_file_dir)
            site_relationship_data.write_to_json(root_file_dir)

            for c_id, c_detail in self._detail_data_pool.items():
                file_dir = root_file_dir + '/' + c_id
                c_detail.write_all_to_json(file_dir)

    def get_all_from_file(self, root_file_dir, file_type='json'):
        company_data = CompanyData()
        company_relationship_data = CompanyRelationshipData()
        site_data = SiteData()
        site_relationship_data = SiteRelationshipData()
        if file_type == 'csv':
            company_data.get_from_csv(root_file_dir)
            company_relationship_data.get_from_csv(root_file_dir)
            site_data.get_from_csv(root_file_dir)
            site_relationship_data.get_from_csv(root_file_dir)
        else:
            company_data.get_from_json(root_file_dir)
            company_relationship_data.get_from_json(root_file_dir)
            site_data.get_from_json(root_file_dir)
            site_relationship_data.get_from_json(root_file_dir)

        self._company_graph = default_company_graph_builder(company_data, company_relationship_data)
        self._site_graph = default_site_graph_builder(site_data, site_relationship_data)

        for c_id in self.company_graph.companies:
            c_detail = CompanyDetailData(company_id=c_id)
            file_dir = root_file_dir + '/' + c_id
            if file_type == 'csv':
                c_detail.get_all_from_csv(file_dir)
            else:
                c_detail.get_all_from_json(file_dir)
            self._detail_data_pool[c_id] = c_detail

        self._material_graph, self._site_graph = default_material_graph_builder(
            self.company_graph, self.site_graph, self.detail_data_pool
        )

    def company_graph_building_from_input(self, company, company_relationship):
        company_data = CompanyData(company)
        company_relationship_data = CompanyRelationshipData(company_relationship)
        self._company_graph = default_company_graph_builder(company_data, company_relationship_data)

    def site_graph_building_from_input(self, site, site_relationship):
        site_data = SiteData(site)
        site_relationship_data = SiteRelationshipData(site_relationship)
        self._site_graph = default_site_graph_builder(site_data, site_relationship_data)

    def material_graph_building_from_input(self, detail_data_pool):
        self._material_graph, self._site_graph = default_material_graph_builder(
            self.company_graph, self.site_graph, detail_data_pool
        )

    def get_company_inv_net(self, c_id):
        """
        It returns the inventory net of a company
        Args:
            c_id:

        Returns:

        """
        sub_company_nodes = [c_id]
        sub_company_edges = [(pred, succ) for (pred, succ) in self.company_graph.edges if succ in sub_company_nodes]
        sub_company_graph = self.company_graph.get_sub_graph_from_sub_edges(sub_company_edges)

        sub_site_nodes = self.company_graph.nodes_pool[c_id].contained_sites
        sub_site_edges = [(pred, succ) for (pred, succ) in self.site_graph.edges if succ in sub_site_nodes]
        sub_site_graph = self.site_graph.get_sub_graph_from_sub_edges(sub_site_edges)

        sub_material_nodes = []
        for s_id in sub_site_nodes:
            sub_material_nodes.extend(list(sub_site_graph.nodes_pool[s_id].contained_materials))
        sub_material_edges = [(pred, succ) for (pred, succ) in self.material_graph.edges if succ in sub_material_nodes]

        sub_material_graph = self.material_graph.get_sub_graph_from_sub_edges(sub_material_edges)

        sub_material_graph.update_topo_info()
        sub_material_graph.update_net_qty()

        sub_detail_data_pool = {c_id: self.detail_data_pool[c_id]}

        sub_inv_net = InvNet(
            company_graph=sub_company_graph,
            site_graph=sub_site_graph,
            material_graph=sub_material_graph,
            detail_data_pool=sub_detail_data_pool
        )
        return sub_inv_net
