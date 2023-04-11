from inv_net.edge import TransitEdge
from inv_net.graph import SiteGraph
from inv_net.node import SiteNode
from data_builder.data_template.site_level import SiteData, SiteRelationshipData


def default_site_graph_builder(site_data: SiteData, site_relationship_data: SiteRelationshipData):
    """
    It builds a site graph from the site data and site relationship data.
    
    Args:
      site_data (SiteData): SiteData
      site_relationship_data (SiteRelationshipData): a SiteRelationshipData object, which contains the
    site relationship data.
    
    Returns:
      A SiteGraph object
    """
    _nodes_pool = {}
    for site_id, site_info in site_data.site.items():
        _nodes_pool[site_id] = SiteNode(
            node_id=site_id,
            company_id=site_info['company_id'],
            desc=site_info['desc'],
            address=site_info['address'],
            province=site_info['province'],
            city=site_info['city'],
            district=site_info['district']
        )

    _edges_pool = {}
    for e in site_relationship_data.site_relationship:
        _edges_pool[(e['from'], e['to'])] = TransitEdge(
            u=e['from'],
            v=e['to'],
            desc=e['desc'],
            u_company=site_data.site[e['from']]['company_id'],
            v_company=site_data.site[e['to']]['company_id'],
            transit_lt=e['transit_lt']
        )

    site_graph = SiteGraph(nodes_pool=_nodes_pool, edges_pool=_edges_pool)
    site_graph.update_topo_info()
    return site_graph
