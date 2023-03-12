import numpy as np
import copy
from utils.graph_algorithms import *
from typing import Optional


class DiGraph:
    def __init__(self, nodes_pool: Optional[dict] = None,
                 edges_pool: Optional[dict] = None,
                 graph_type: Optional[str] = None):
        if nodes_pool is None:  # {node_id: node}
            self._nodes_pool = {}
        else:
            self._nodes_pool = nodes_pool
        if edges_pool is None:  # {(u, v): edge}
            self._edges_pool = {}
        else:
            self._edges_pool = edges_pool

        self._graph_type = graph_type
        self._root_nodes_pool = None
        self._sink_nodes_pool = None

        self._preds_of_node = None
        self._succs_of_node = None
        self._topo_sort = None

        self._graph_level = None  # 'COMPANY'/ 'SITE'/ 'MATERIAL'

    @property
    def nodes_pool(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._nodes_pool

    @property
    def nodes(self):
        return set(self._nodes_pool.keys())

    @property
    def edges_pool(self):
        return self._edges_pool

    @property
    def edges(self):
        return list(self._edges_pool.keys())

    @property
    def root_nodes_pool(self):
        return self._root_nodes_pool

    @property
    def roots(self):
        return set(self._root_nodes_pool)

    @property
    def sink_nodes_pool(self):
        return self._sink_nodes_pool

    @property
    def sinks(self):
        return set(self._sink_nodes_pool)

    @property
    def num_of_nodes(self):
        return len(self._nodes_pool)

    @property
    def num_of_edges(self):
        return len(self._edges_pool)

    @property
    def graph_type(self):
        if self._graph_type is None:
            if is_tree(self.nodes, self.edges):
                self._graph_type = 'TREE'
            else:
                self._graph_type = 'GENERAL'
        return self._graph_type

    @property
    def graph_level(self):
        return self._graph_level

    @property
    def topo_sort(self):
        return self._topo_sort

    @property
    def preds_of_node(self):
        return self._preds_of_node

    @property
    def succs_of_node(self):
        return self._succs_of_node

    def add_node(self, node_info):
        if node_info.node_id not in self._nodes_pool:
            self._nodes_pool[node_info.node_id] = node_info

    def remove_node(self, node_id):
        self._nodes_pool.pop(node_id, None)

    def add_edge(self, edge_info):
        if edge_info.edge_id not in self._edges_pool:
            self._edges_pool[edge_info.edge_id] = edge_info

    def remove_edge(self, edge_id):
        self._edges_pool.pop(edge_id, None)

    def update_topo_info(self):
        self.find_roots()
        self.find_sinks()
        self.find_preds_of_node()
        self.find_succs_of_node()

        if len(self.edges) > 0:
            self._topo_sort = find_topo_sort(self.edges)
        else:
            self._topo_sort = list(self.nodes)

        for j, node_info in self._nodes_pool.items():
            node_info.update_pred_nodes(self._preds_of_node.get(j, set()))
            node_info.update_succ_nodes(self._succs_of_node.get(j, set()))

        self.update_incoming_edges_info()

    def update_incoming_edges_info(self):
        for n_id, n in self._nodes_pool.items():
            inc_edges_info = {(pred, n_id): {} for pred in n.pred_nodes}
            n.update_incoming_edges_info(inc_edges_info)

    def find_roots(self):
        if len(self.edges) > 0:
            root_ids = set([i for i, _ in self.edges]) - set([j for _, j in self.edges])
        else:
            root_ids = set()
        self._root_nodes_pool = {j: self._nodes_pool[j] for j in root_ids}

    def find_sinks(self):
        if len(self.edges) > 0:
            sink_ids = set([j for _, j in self.edges]) - set([i for i, _ in self.edges])
        else:
            sink_ids = self.nodes
        self._sink_nodes_pool = {j: self._nodes_pool[j] for j in sink_ids}

    def find_preds_of_node(self):
        if len(self.edges) > 0:
            self._preds_of_node = find_preds_of_node(list(self._edges_pool.keys()))
        else:
            self._preds_of_node = {}

    def find_succs_of_node(self):
        if len(self.edges) > 0:
            self._succs_of_node = find_succs_of_node(list(self._edges_pool.keys()))
        else:
            self._succs_of_node = {}

    def find_descendants(self, i: str):
        if self._succs_of_node is None:
            self.find_succs_of_node()

        descendants, sub_des_edge_list = find_descendants(self._succs_of_node, i)
        return descendants, sub_des_edge_list

    def find_ancestors(self, j: str):
        if self._preds_of_node is None:
            self.find_preds_of_node()

        ancestors, sub_ans_edge_list = find_ancestors(self._preds_of_node, j)
        return ancestors, sub_ans_edge_list

    def find_sink_descendants(self, i: str):
        des, _ = self.find_descendants(i)
        sink_des = des & self.sinks
        return sink_des

    def find_root_ancestors(self, j: str):
        ans, _ = self.find_ancestors(j)
        root_ans = ans & self.roots
        return root_ans

    #  u -> v existence
    def two_nodes_connectivity(self, u, v):
        des, _ = self.find_descendants(u)
        if v in des:
            return True
        else:
            return False

    def decompose_graph(self, to_remove_edges=None):
        """
        The above function decomposes the graph into subgraphs.
        
        :param to_remove_edges: a list of edges to be removed from the graph
        :return: A list of subgraphs
        """
        if to_remove_edges is None:
            to_remove_edges = []

        new_edges = [e for e in self.edges if e not in to_remove_edges]

        components = find_weakly_connected_components(self.nodes, new_edges)

        if len(components) == 1:
            print('This graph can not be decomposed')
            return [self]
        else:
            print('This graph can be decomposed')
            sub_graph_list = []
            for component in components:
                connected_nodes = component[0]
                sub_edges = component[1]
                sub_graph = self._get_sub_graph(connected_nodes, sub_edges)
                sub_graph_list.append(sub_graph)
            return sub_graph_list

    def get_sub_graph_from_sub_edges(self, sub_edges):
        sub_nodes = set([node for tu in sub_edges for node in tu])
        sub_graph = self._get_sub_graph(sub_nodes, sub_edges)
        return sub_graph

    """
    > Given a list of nodes, return a subgraph of the current graph that contains only those nodes and
    the edges between them
    
    :param sub_nodes: a list of nodes that you want to include in the subgraph
    :return: A subgraph of the original graph.
    """
    def get_sub_graph_from_sub_nodes(self, sub_nodes):
        sub_edges = [(pred, succ) for (pred, succ) in self.edges if (pred in sub_nodes) and (succ in sub_nodes)]
        sub_graph = self._get_sub_graph(sub_nodes, sub_edges)
        return sub_graph

    def _get_sub_graph(self, sub_nodes, sub_edges):
        sub_nodes_pool = {j: copy.deepcopy(self._nodes_pool[j]) for j in sub_nodes}
        sub_edges_pool = {e: copy.deepcopy(self._edges_pool[e]) for e in sub_edges}
        if self._graph_level == 'COMPANY':
            sub_graph = CompanyGraph(nodes_pool=sub_nodes_pool, edges_pool=sub_edges_pool)

        elif self._graph_level == 'SITE':
            sub_graph = SiteGraph(nodes_pool=sub_nodes_pool, edges_pool=sub_edges_pool)

        elif self._graph_level == 'MATERIAL':
            sub_graph = MaterialGraph(nodes_pool=sub_nodes_pool, edges_pool=sub_edges_pool)

        else:
            raise AttributeError

        sub_graph.update_topo_info()

        return sub_graph

    def to_undirected(self):
        un_di_graph = UnDiGraph(self.nodes, self.edges)
        return un_di_graph


class CompanyGraph(DiGraph):
    def __init__(self, nodes_pool: Optional[dict] = None,
                 edges_pool: Optional[dict] = None):
        super().__init__(nodes_pool, edges_pool)
        self._graph_level = 'COMPANY'

    @property
    def companies(self):
        return set(self._nodes_pool.keys())

    @property
    def contained_sites_of_company(self):
        return {c_id: self._nodes_pool[c_id].contained_sites for c_id in self.nodes}

    @property
    def contained_demand_sites_of_company(self):
        return {c_id: self._nodes_pool[c_id].contained_dc_sites for c_id in self.nodes}

    @property
    def contained_manu_sites_of_company(self):
        return {c_id: self._nodes_pool[c_id].contained_mc_sites for c_id in self.nodes}


class SiteGraph(DiGraph):
    def __init__(self, nodes_pool: Optional[dict] = None,
                 edges_pool: Optional[dict] = None):
        super().__init__(nodes_pool, edges_pool)
        self._graph_level = 'SITE'

    @property
    def sites(self):
        return set(self._nodes_pool.keys())

    def update_incoming_edges_info(self):
        for n_id, n in self._nodes_pool.items():
            inc_edges_info = {(pred, n_id): {'transit_lt': self._edges_pool[(pred, n_id)].transit_lt}
                              for pred in n.pred_nodes}
            n.update_incoming_edges_info(inc_edges_info)

    def sites_transit_lt(self, u: str, v: str):
        """
        > Given two nodes, return the minimum transit latency of all paths between them
        
        :param u: str, v: str: the two nodes between which we want to find the shortest path
        :type u: str
        :param v: the number of nodes in the network
        :type v: str
        :return: The minimum transit latency between two nodes.
        """
        if (u, v) in self.edges:
            return self._edges_pool[(u, v)].transit_lt
        elif self.two_nodes_connectivity(u, v):
            if self.succs_of_node is None:
                self.update_topo_info()
            all_paths = find_all_paths(succ_of_node=self.succs_of_node, u=u, v=v)
            min_cum_edge_lt = np.inf
            for path in all_paths:
                path_cum_edge_lt = 0
                for i in range(len(path) - 1):
                    path_cum_edge_lt += self._edges_pool[(path[i], path[i + 1])].transit_lt
                min_cum_edge_lt = min(min_cum_edge_lt, path_cum_edge_lt)
            return min_cum_edge_lt
        else:
            return np.inf


class MaterialGraph(DiGraph):
    def __init__(self, nodes_pool: Optional[dict] = None,
                 # 
                 edges_pool: Optional[dict] = None):
        super().__init__(nodes_pool, edges_pool)
        self._graph_level = 'MATERIAL'
        self._net_qty = None
        self._alter_nodes_pool = None

    @property
    def alter_nodes_pool(self):
        if self._alter_nodes_pool is None:
            self.update_alter_nodes_pool()
        return self._alter_nodes_pool

    @property
    def edge_qty(self):
        return {e_id: e.qty for e_id, e in self._edges_pool.items()}

    @property
    def net_qty(self):
        if self._net_qty is None:
            self.update_net_qty()
        return self._net_qty

    def update_alter_nodes_pool(self):
        self._alter_nodes_pool = {n_id: n for n_id, n in self._nodes_pool.items()
                                  if n.node_type == 'ALTER_MATERIAL'}

    def update_incoming_edges_info(self):
        for n_id, n in self._nodes_pool.items():
            inc_edges_info = {(pred, n_id): {'transit_lt': self._edges_pool[(pred, n_id)].transit_lt,
                                             'decision_ratio': self._edges_pool[(pred, n_id)].decision_ratio}
                              for pred in n.pred_nodes}
            n.update_incoming_edges_info(inc_edges_info)

    def update_default_alter_decision_ratio(self):
        for n_id, n in self.alter_nodes_pool.items():
            n.update_decision_ratio()
            for e_id, e in n.incoming_edges_info.items():
                self._edges_pool[e_id].update_decision_ratio(e['decision_ratio'])

    def update_cum_lt_info(self):
        lt_of_node = {n_id: n.lt for n_id, n in self._nodes_pool.items()}
        preds_of_node = {n_id: n.pred_nodes for n_id, n in self._nodes_pool.items()}
        preds_of_node.update({r: {'start'} for r in self.roots})

        cum_lt_of_node = {n_id: -float('inf') for n_id in self.topo_sort}
        cum_lt_of_node['start'] = 0.0
        longest_pred_of_node = {n_id: set() for n_id in self.topo_sort}

        for n_id in self.topo_sort:
            if self._nodes_pool[n_id].node_type != 'ALTER_MATERIAL':
                for pred in preds_of_node[n_id]:
                    tmp = cum_lt_of_node[pred] + lt_of_node[n_id]
                    if cum_lt_of_node[n_id] < tmp:
                        longest_pred_of_node[n_id] = {pred}
                        cum_lt_of_node[n_id] = tmp
                    elif cum_lt_of_node[n_id] == tmp:
                        longest_pred_of_node[n_id].add(pred)
            else:
                tmp = {e_id[0]: cum_lt_of_node[e_id[0]] + lt_of_node[n_id]
                       for e_id, inc_e_info in self._nodes_pool[n_id].incoming_edges_info.items()
                       if inc_e_info['decision_ratio'] > 0}
                if self._nodes_pool[n_id].alter_time_mode == 'EXP':
                    cum_lt_of_node[n_id] = sum(
                        [t * self._nodes_pool[n_id].incoming_edges_info[(pred, n_id)]['decision_ratio']
                         for pred, t in tmp.items()]
                    )
                elif self._nodes_pool[n_id].alter_time_mode == 'MAX':
                    cum_lt_of_node[n_id] = max(tmp.values())
                elif self._nodes_pool[n_id].alter_time_mode == 'MIN':
                    cum_lt_of_node[n_id] = min(tmp.values())
                longest_pred_of_node[n_id] = set([pred for pred, t in tmp.items() if t == cum_lt_of_node[n_id]])
        cum_lt_of_node.pop('start')

        for n_id, n in self._nodes_pool.items():
            n.update_cum_lt(cum_lt_of_node[n_id])
            n.update_longest_pred(longest_pred_of_node[n_id])

    def update_net_qty(self):
        self._net_qty = cal_net_qty(self.edges, self.edge_qty)


class UnDiGraph:
    def __init__(self, nodes: set, edges: list):
        self.nodes = nodes
        self.edges = edges
        if len(self.edges):
            self.adjs_of_node = find_adjs_of_node(edges)
        else:
            self.adjs_of_node = {node: {} for node in self.nodes}

        self.degree_of_node = {j: len(self.adjs_of_node[j]) for j in nodes}

    def is_fully_connected(self):
        visited = set()

        def _dfs(node):
            if node not in visited:
                visited.add(node)
                for adj in self.adjs_of_node[node]:
                    _dfs(adj)

        _dfs(list(self.nodes)[0])

        return len(visited) == len(self.nodes)

    def remove_nodes(self, rm_nodes: list):
        new_all_nodes = self.nodes - set(rm_nodes)
        new_edge_list = [(i, j) for i, j in self.edges if ((i in new_all_nodes) and (j in new_all_nodes))]
        new_un_di_graph = UnDiGraph(new_all_nodes, new_edge_list)
        return new_un_di_graph

    def cycle_detect_from_source(self, source):
        visited = set()

        def _dfs(u, parent=0):
            visited.add(u)
            for v in self.adjs_of_node[u]:
                if v not in visited:
                    if _dfs(v, u):
                        return True
                elif v != parent:
                    return True
            return False

        return _dfs(source)
