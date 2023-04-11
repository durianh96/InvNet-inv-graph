import ast
from data_builder.data_template.company_level import CompanyData, CompanyRelationshipData
from inv_net.edge import SupplyEdge
from inv_net.graph import CompanyGraph
from inv_net.node import CompanyNode


def default_company_graph_builder(company_data: CompanyData, company_relationship_data: CompanyRelationshipData):
    _nodes_pool = {}
    for company_id, company_info in company_data.company.items():
        if type(company_info['contained_sites']) == str:
            company_info['contained_sites'] = ast.literal_eval(company_info['contained_sites'])
        contained_sites = set(company_info['contained_sites'].keys())
        contained_demand_sites = {site for site, site_type in company_info['contained_sites'].items()
                                  if site_type == 'demand'}
        contained_manu_sites = {site for site, site_type in company_info['contained_sites'].items()
                                if site_type == 'manu'}
        _nodes_pool[company_id] = CompanyNode(
            node_id=company_id,
            desc=company_info['desc'],
            contained_sites=contained_sites,
            contained_demand_sites=contained_demand_sites,
            contained_manu_sites=contained_manu_sites
        )
    _edges_pool = {}
    for e in company_relationship_data.company_relationship:
        _edges_pool[(e['supplier'], e['buyer'])] = SupplyEdge(
            u=e['supplier'],
            v=e['buyer'],
            desc=e['desc']
        )
    company_graph = CompanyGraph(nodes_pool=_nodes_pool, edges_pool=_edges_pool)
    company_graph.update_topo_info()
    return company_graph
