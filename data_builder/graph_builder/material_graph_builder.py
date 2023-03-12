from data_builder.data_template.company_detail_data import CompanyDetailData
from inv_net.graph import *
from inv_net.node import *
from inv_net.edge import *


def pure_supplier_nodes_building(company_detail_data: CompanyDetailData, site_graph: SiteGraph):
    """
    > For each product in the company's product data, create a material node with the product's material
    id, sale site, and sale price, and add it to the site graph's nodes pool
    
    Args:
      company_detail_data (CompanyDetailData): CompanyDetailData
      site_graph (SiteGraph): the graph object that contains all the nodes and edges
    
    Returns:
      A tuple of two objects.
    """
    product_data = company_detail_data.product_data
    _nodes_pool = {}
    for p in product_data.product:
        node_id = p['material_id'] + '_' + p['sale_site']
        site_graph.nodes_pool[p['sale_site']].add_contained_material(node_id)
        _nodes_pool[node_id] = MaterialNode(
            node_id=node_id,
            company_id=p['company_id'],
            site_id=p['sale_site'],
            material_id=p['material_id'],
            desc='pure_supplier_material_node',
            sale_price=p['sale_price'],
            sale_sla=p['sale_sla'],
            avg_fill_time=p['avg_fill_time']
        )
    return _nodes_pool, site_graph


def nodes_edges_building(company_detail_data: CompanyDetailData, site_graph: SiteGraph):
    """
    It takes in a company_detail_data object, and a site_graph object, and returns a tuple of three
    objects:
    
    1. a dictionary of nodes
    2. a dictionary of edges
    3. the site_graph object
    
    The function is called by the `build_graph` function, which is called by the `build_graphs` function
    
    Args:
      company_detail_data (CompanyDetailData): a CompanyDetailData object
      site_graph (SiteGraph): the graph object that contains all the nodes and edges
    
    Returns:
      A dictionary of nodes and edges
    """
    make_material_data = company_detail_data.make_material_data
    site_material_data = company_detail_data.site_material_data
    bom_data = company_detail_data.bom_data

    site_material_df = site_material_data.get_df()
    material_supplier_sites_dict = site_material_df.groupby(['material_id', 'site_id'])['supply_site'].apply(
        list).to_dict()
    manu_lt_dict = {(m['material_id'], m['manu_site']): m['manu_lt'] for m in make_material_data.make_material}

    _nodes_pool = {}
    _edges_pool = {}

    for m in site_material_data.site_material:
        if len(material_supplier_sites_dict[(m['material_id'], m['site_id'])]) > 1:
            alter_n_id = m['material_id'] + '_' + m['site_id']
            # if alter node not exist, create one
            if alter_n_id not in _nodes_pool.keys():
                site_graph.nodes_pool[m['site_id']].add_contained_material(alter_n_id)
                _nodes_pool[alter_n_id] = AlterMaterialNode(
                    node_id=alter_n_id,
                    company_id=m['company_id'],
                    site_id=m['site_id'],
                    material_id=m['material_id'],
                    desc='alter_material_node',
                    make_or_buy=m['make_or_buy'],
                    holding_cost=m['holding_cost'],
                    material_cost=m['material_cost']
                )
            n_id = m['material_id'] + '_' + m['site_id'] + '_' + m['supply_site']
            # link this material node with alter node
            _edges_pool[(n_id, alter_n_id)] = MaterialEdge(
                u=n_id,
                v=alter_n_id,
                u_site=m['site_id'],
                v_site=m['site_id'],
                original_qty=1,
                desc='multi_decision_edge'
            )
        else:
            n_id = m['material_id'] + '_' + m['site_id']

        site_graph.nodes_pool[m['site_id']].add_contained_material(n_id)

        if m['site_id'] == m['supply_site']:
            # this material is made as this site
            process_lt = manu_lt_dict.get((m['material_id'], m['site_id']), 0)
        else:
            process_lt = 0
            # link this material node with its supplier if has supplier node
            if m['supply_site'] is not None:
                pred_n_id = m['material_id'] + '_' + m['supply_site']
                _edges_pool[(pred_n_id, n_id)] = MaterialEdge(
                    u=pred_n_id,
                    v=n_id,
                    u_site=m['supply_site'],
                    v_site=m['site_id'],
                    original_qty=1,
                    transit_lt=site_graph.sites_transit_lt(m['supply_site'], m['site_id']),
                    desc='material_transit_edge'
                )

        _nodes_pool[n_id] = MaterialNode(
            node_id=n_id,
            company_id=m['company_id'],
            site_id=m['site_id'],
            material_id=m['material_id'],
            desc='material_node',
            make_or_buy=m['make_or_buy'],
            inv_type=m['inv_type'],
            replenish_cycle=m['cycle'],
            process_lt=process_lt,
            holding_cost=m['holding_cost'],
            material_cost=m['material_cost']
        )

    # Building the edges between the components and the assemblies.
    for b in bom_data.bom:
        component_node_id = b['component'] + '_' + b['manu_site']
        assembly_node_id = b['assembly'] + '_' + b['manu_site']
        if np.isnan(b['qty']):
            original_qty = 1
        else:
            original_qty = b['qty']
        _edges_pool[(component_node_id, assembly_node_id)] = MaterialEdge(
            u=component_node_id,
            v=assembly_node_id,
            u_site=b['manu_site'],
            v_site=b['manu_site'],
            original_qty=original_qty,
            desc='bom_edge'
        )

    # product nodes info update
    product_data = company_detail_data.product_data
    for p in product_data.product:
        node_id = p['material_id'] + '_' + p['sale_site']
        desc = _nodes_pool[node_id].desc + '_sale_product'
        _nodes_pool[node_id].update_desc(desc)
        _nodes_pool[node_id].update_sale_price(p['sale_price'])
        _nodes_pool[node_id].update_sale_sla(p['sale_sla'])
        _nodes_pool[node_id].update_avg_fill_time(p['avg_fill_time'])
    return _nodes_pool, _edges_pool, site_graph


def default_material_graph_builder(company_graph: CompanyGraph, site_graph: SiteGraph, detail_data_pool):
    """
    > For each company in the company graph, we build a set of nodes and edges, and then we put them
    into the material graph
    
    Args:
      company_graph (CompanyGraph): CompanyGraph
      site_graph (SiteGraph): SiteGraph
      detail_data_pool: a dict of company_id: company_detail_data
    
    Returns:
      A material graph and a site graph.
    """
    _nodes_pool = {}
    _edges_pool = {}
    for c_id in company_graph.roots:
        c_detail = detail_data_pool[c_id]
        c_nodes, site_graph = pure_supplier_nodes_building(c_detail, site_graph)
        _nodes_pool.update(c_nodes)

    for c_id in company_graph.nodes - company_graph.roots:
        c_detail = detail_data_pool[c_id]
        c_nodes, c_edges, site_graph = nodes_edges_building(c_detail, site_graph)
        _nodes_pool.update(c_nodes)
        _edges_pool.update(c_edges)

    material_graph = MaterialGraph(nodes_pool=_nodes_pool, edges_pool=_edges_pool)
    material_graph.update_topo_info()
    material_graph.update_net_qty()

    for n_id, n in material_graph.nodes_pool.items():
        if n_id in material_graph.roots:
            n_lt = n.process_lt + n.avg_fill_time
        else:
            if len(n.incoming_edges_info) > 0:
                n_lt = n.process_lt + max([e['transit_lt'] for e in n.incoming_edges_info.values()])
            else:
                n_lt = n.process_lt
        n.update_lt(n_lt)

    return material_graph, site_graph
