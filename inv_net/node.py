from typing import Union, Optional


class Node:
    """
    Base class for nodes in directed graph.
    A node can represent a company, a warehouse, a factory, a distribution center, a product, etc.

    There are three levels of nodes: company level, site level and material level.
    This base node template stores common topological attributes of three levels.

    Args:
        node_id (str): The unique id for this node.
        desc (Optional[str], optional): The description of this node. Defaults to None.
    """

    def __init__(self, node_id: str, desc: Optional[str] = None):
        self._node_id = node_id
        self._desc = desc
        self._node_type = None
        self._pred_nodes = set()  # set of node's predecessors
        self._succ_nodes = set()  # set of node's successors
        self._incoming_edges_info = {}

    @property
    def node_id(self):
        """The unique id for this node.

        Returns:
            str
        """
        return self._node_id

    @property
    def desc(self):
        """The description of this node.

        Returns:
            str
        """
        return self._desc

    @property
    def node_type(self):
        """The node type. Example: 'COMPANY', 'MATERIAL', etc.

        Returns:
            str
        """
        return self._node_type

    @property
    def pred_nodes(self):
        """The predecessors of this node.

        Returns:
            set
        """
        return self._pred_nodes

    @property
    def succ_nodes(self):
        """The successors of this node.

        Returns:
            set
        """
        return self._succ_nodes

    @property
    def adj_nodes(self):
        """The adjacent nodes of this node.

        Returns:
            set
        """
        return self._pred_nodes | self._succ_nodes

    @property
    def incoming_edges_info(self):
        """The information of edges that point to this node.
        Example:
            {(u1, node_id): {'transit_lt': 2},
            (u2, node_id): {'transit_lt': 3}}

        Returns:
            dict
        """
        return self._incoming_edges_info

    @property
    def in_degree(self):
        """The number of edges pointing to the node.

        Returns:
            int
        """
        return len(self._pred_nodes)

    @property
    def out_degree(self):
        """The number of edges pointing out of the node. 

        Returns:
            int
        """
        return len(self._succ_nodes)

    @property
    def degree(self):
        """The number of edges adjacent to the node.

        Returns:
            int
        """
        return len(self._pred_nodes) + len(self._succ_nodes)

    def update_desc(self, new_desc: str):
        """Updating the description of the node.

        Args:
            new_desc (str)
        """
        self._desc = new_desc

    def add_pred_node(self, new_pred_node: str):
        """Adding a new predecessor.

        Args:
            new_pred_node (str): New predecessor's node id.
        """
        self._pred_nodes.add(new_pred_node)

    def remove_pred_node(self, rm_pred_node: str):
        """Removing a predecessor.

        Args:
            rm_pred_node (str): To remove predecessor's node id.
        """
        self._pred_nodes.discard(rm_pred_node)

    def update_pred_nodes(self, new_pred_nodes: set):
        """Updating the predecessors set of the node.

        Args:
            new_pred_nodes (set): New predecessor's set.
        """
        self._pred_nodes = new_pred_nodes

    def add_succ_node(self, new_succ_node: str):
        """Adding a new successor.

        Args:
            new_succ_node (str): New successor's node id.
        """
        self._pred_nodes.add(new_succ_node)

    def remove_succ_node(self, rm_succ_node: str):
        """Removing a successor.

        Args:
            rm_succ_node (str): To remove successor's node id.
        """
        self._succ_nodes.discard(rm_succ_node)

    def update_succ_nodes(self, new_succ_nodes: set):
        """Updating the successors set of the node.

        Args:
            new_succ_nodes (set): New successor's set.
        """
        self._succ_nodes = new_succ_nodes

    def update_incoming_edges_info(self, new_incoming_edges_info: dict):
        """Updating the incoming edge information of the node.

        Args:
            new_incoming_edges_info (dict): New incoming edge information dict.
        """
        self._incoming_edges_info = new_incoming_edges_info

    def reset_topo_info(self):
        """Resetting the topological information of this node. 
        """
        self._pred_nodes = set()
        self._succ_nodes = set()
        self._incoming_edges_info = {}


class CompanyNode(Node):
    """
    The company level base node, a company node might contain serval site nodes.

    Args:
        node_id (str): The unique id for this node, equals to its company id.
        desc (Optional[str], optional): The description of this company node. Defaults to None.
        contained_sites (Optional[set], optional): A company might manage serval sites (facilities). This set contains
        the site id of these sites. Defaults to None.

        contained_dc_sites (Optional[set], optional): The site nodes managed by this company which have outside
        demand. Defaults to None.
        contained_mc_sites (Optional[set], optional): The site nodes managed by this company which have manufacturing
        operation. Defaults to None.
    """

    def __init__(self, node_id: str,
                 desc: Optional[str] = None,
                 contained_sites: Optional[set] = None,
                 contained_dc_sites: Optional[set] = None,
                 contained_mc_sites: Optional[set] = None):
        super().__init__(node_id, desc)
        if contained_sites is None:
            self._contained_sites = set()
        else:
            self._contained_sites = contained_sites
        if contained_dc_sites is None:
            self._contained_dc_sites = set()
        else:
            self._contained_dc_sites = contained_dc_sites
        if contained_mc_sites is None:
            self._contained_mc_sites = set()
        else:
            self._contained_mc_sites = contained_mc_sites

        self._node_type = 'COMPANY'

    @property
    def company_id(self):
        """The company id of this company.

        Returns:
            str
        """
        return self._node_id

    @property
    def contained_sites(self):
        """The site nodes managed by this company.

        Returns:
            set
        """
        return self._contained_sites

    @property
    def contained_dc_sites(self):
        """The site nodes managed by this company which have outside demand.

        Returns:
            set
        """
        return self._contained_dc_sites

    @property
    def contained_mc_sites(self):
        """The site nodes managed by this company which have manufacturing operation.

        Returns:
            set
        """
        return self._contained_mc_sites

    @property
    def suppliers(self):
        """The upstream suppliers of this company.

        Returns:
            set
        """
        return self.pred_nodes

    @property
    def customers(self):
        """The downstream customers of this company.

        Returns:
            str
        """
        return self.succ_nodes

    def update_contained_sites(self, new_contained_sites: set):
        """Updating the contained sites set.

        Args:
            new_contained_sites (set)
        """
        self._contained_sites = new_contained_sites

    def update_contained_dc_sites(self, new_contained_dc_sites: set):
        """Updating the contained demand sites set.

        Args:
            new_contained_dc_sites (set)
        """
        self._contained_dc_sites = new_contained_dc_sites

    def update_contained_mc_sites(self, new_contained_mc_sites: set):
        """Updating the contained manu sites.

        Args:
            new_contained_mc_sites (set)
        """
        self._contained_mc_sites = new_contained_mc_sites


class SiteNode(Node):
    """
    The site level base node. A site node can represent a factory, a warehouse, a distribution center, a sales channel, etc.
    A site node might contain serval material nodes.

    Args:
        node_id (str): The unique id for this node, equals to its site id.
        company_id (str): The company id of this site's owner.
        desc (Optional[str], optional): The description of this site node. Defaults to None.
        loc (Optional[str], optional): The location of this site node. Defaults to None.
        contained_materials (Optional[set], optional): The materials stored in this site. Defaults to None.
    """

    def __init__(self, node_id: str,
                 company_id: str,
                 desc: Optional[str] = None,
                 loc: Optional[str] = None,
                 contained_materials: Optional[set] = None):
        super().__init__(node_id, desc)
        self._loc = loc
        self._company_id = company_id
        if contained_materials is None:
            self._contained_materials = set()
        else:
            self._contained_materials = contained_materials

    @property
    def loc(self):
        """The location of this site node.

        Returns:
            str
        """
        return self._loc

    @property
    def company_id(self):
        """The company id of this site's owner.

        Returns:
            str
        """
        return self._company_id

    @property
    def site_id(self):
        """The site id of this site.

        Returns:
            str
        """
        return self._node_id

    @property
    def contained_materials(self):
        """The materials nodes stored in this site.

        Returns:
            set
        """
        return self._contained_materials

    def add_contained_material(self, new_contained_material: str):
        """Adding a new material node to this site.

        Args:
            new_contained_material (str)
        """
        self._contained_materials.add(new_contained_material)

    def remove_contained_material(self, rm_contained_material: str):
        """Removing a material node from this site.

        Args:
            rm_contained_material (str)
        """
        self._contained_materials.discard(rm_contained_material)

    def update_contained_materials(self, new_contained_nodes: set):
        """Updating the contained material nodes set.

        Args:
            new_contained_nodes (set)
        """
        self._contained_materials = new_contained_nodes


class ManufacturingCenterNode(SiteNode):
    """
    Class for manufacturing site node.

    Args:
        node_id (str): The unique id for this node, equals to its site id.
        company_id (str): The company id of this site's owner.
        desc (Optional[str], optional): The description of this site node. Defaults to None.
        loc (Optional[str], optional): The location of this site node. Defaults to None.
        contained_materials (Optional[set], optional): The materials stored in this site. Defaults to None.
    """

    def __init__(self, node_id: str,
                 company_id: str,
                 desc: Optional[str] = None,
                 loc: Optional[str] = None,
                 contained_materials: Optional[set] = None):
        super().__init__(node_id, company_id, desc, loc, contained_materials)
        self._node_type = 'MANUFACTURING_CENTER'


class DistributionCenterNode(SiteNode):
    """
    Class for distribution site node.

    Args:
        node_id (str): The unique id for this node, equals to its site id.
        company_id (str): The company id of this site's owner.
        desc (Optional[str], optional): The description of this site node. Defaults to None.
        loc (Optional[str], optional): The location of this site node. Defaults to None.
        contained_materials (Optional[set], optional): The materials stored in this site. Defaults to None.
    """

    def __init__(self, node_id: str,
                 company_id: str,
                 desc: Optional[str] = None,
                 loc: Optional[str] = None,
                 contained_materials: Optional[set] = None):
        super().__init__(node_id, company_id, desc, loc, contained_materials)
        self._node_type = 'DISTRIBUTION_CENTER'


class MaterialNode(Node):
    """
    The material level base node. A material node represent a material (raw, semi-product, finished product,
    etc.) at a site. It might be a potential inventory stocking point.

    Args:
        node_id (str): The unique id for this node, default is site_id + '_' + material_id.
        company_id (str): The company id of this material node's owner.
        site_id (str): The site id of this material node's stocking site.
        material_id (str): The material id of this material node.

        desc (Optional[str], optional): The description of this material node. Defaults to None.
        
        make_or_buy (Optional[str], optional): For the owner of this material node, this value equals to 'BUY' means
        this material is buying from outside supplier; if this value is 'MAKE', it means this material is produced by
        this company. Defaults to None.

        inv_type (str, optional): It means whether this material node can hold inventory. 'YES' for can and 'NO' for
        cannot. Defaults to 'YES'.

        replenish_cycle (Optional[Union[float, int]], optional): The replenish (make order or make production plan)
        cycle time of this material node. Defaults to None.

        process_lt (Optional[Union[float, int]], optional): The process lead time for this node, represents the
        duration from the time when all necessary upstream are in stock (finished transit to it) until the downstream
        or outside demand can be served (ready for transit). It might include the warehouse operation time,
        the manufacturing time, etc. Defaults to None.

        lt (Optional[Union[float, int]], optional): The lead time of this node, represents the duration from the time
        when all necessary upstream materials are available (ready for transit to it) until the downstream or outside
        demand can be served (ready for transit). Besides itself process_lt, it might contain the supplier's order
        fill time (for the root nodes of current InvNet), and the transit time between this node and its upstream
        nodes. For a root node of current InvNet, it equals to the former fill time plus itself process lead time.
        For a material node needs serval component to product, it equals to the max transit time of upstream to it
        plus itself process lead time. Defaults to None.

        holding_cost (Optional[Union[float, int]], optional): Unit holding cost rate of this material node,
        it represents the holding cost for this node to keep one unit material for one time unit. Defaults to None.

        material_cost (Optional[Union[float, int]], optional): Unit material cost of this material node. For 'BUY'
        materials, this can be purchase price. Defaults to None.

        sale_price (Optional[Union[float, int]], optional): Sale price for a product material node.  Defaults to
        None. 
        
        sale_sla (Optional[Union[float, int]], optional): Sale service level agreement for a product material
        node, the service time (the duration from the order placed to order can be served) should not larger than
        this value. Defaults to None.

        avg_fill_time (Optional[Union[float, int]], optional): This attribute represents average order fill time for
        its downstream nodes. This attribute is designed to be able to decouple the analysis of the supply chain from
        upstream site (or company) to downstream site (or company).
        It can be obtained through simulation. Defaults to None.
    """

    def __init__(self, node_id: str,
                 company_id: str,
                 site_id: str,
                 material_id: str,
                 desc: Optional[str] = None,
                 make_or_buy: Optional[str] = None,
                 inv_type: Optional[str] = None,
                 replenish_cycle: Optional[Union[float, int]] = None,
                 process_lt: Optional[Union[float, int]] = None,
                 lt: Optional[Union[float, int]] = None,
                 holding_cost: Optional[Union[float, int]] = None,
                 material_cost: Optional[Union[float, int]] = None,
                 sale_price: Optional[Union[float, int]] = None,
                 sale_sla: Optional[Union[float, int]] = None,
                 avg_fill_time: Optional[Union[float, int]] = None,
                 ):
        super().__init__(node_id, desc)
        self._company_id = company_id
        self._site_id = site_id
        self._material_id = material_id
        self._make_or_buy = make_or_buy
        self._inv_type = inv_type
        if replenish_cycle is None:
            self._replenish_cycle = 0
        else:
            self._replenish_cycle = replenish_cycle
        if process_lt is None:
            self._process_lt = 0
        else:
            self._process_lt = process_lt
        self._lt = lt
        self._cum_lt = None
        self._longest_pred = None
        self._holding_cost = holding_cost
        self._material_cost = material_cost
        self._sale_price = sale_price
        self._sale_sla = sale_sla
        if avg_fill_time is None:
            self._avg_fill_time = 0
        else:
            self._avg_fill_time = avg_fill_time
        self._node_type = 'MATERIAL'

    @property
    def company_id(self):
        """The company id of this material node's owner.

        Returns:
            str
        """
        return self._company_id

    @property
    def site_id(self):
        """The site id of this material node's stocking site.

        Returns:
            str
        """
        return self._site_id

    @property
    def material_id(self):
        """The material id of this material node.

        Returns:
            str
        """
        return self._material_id

    @property
    def make_or_buy(self):
        """For the owner of this material node, this value equals to 'BUY' means this material is buying from outside 
        supplier; if this value is 'MAKE', it means this material is produced by this company.

        Returns:
            str -- 'MAKE' or 'BUY'
        """
        return self._make_or_buy

    @property
    def inv_type(self):
        """Whether this material node can hold inventory. 

        Returns:
            str -- 'YES' or 'NO'
        """
        return self._inv_type

    @property
    def replenish_cycle(self):
        """The replenishment (make order or make production plan) cycle time of this material node.

        Returns:
            float
        """
        return self._replenish_cycle

    @property
    def process_lt(self):
        """The process lead time for this node, represents the duration from
        the time when all necessary upstream are in stock (finished transit to it) until the downstream or outside
        demand can be served (ready for transit).
        It might include the warehouse operation time, the manufacturing time, etc.

        Returns:
            float
        """
        return self._process_lt

    @property
    def lt(self):
        """The lead time of this node, represents the duration from the time when all necessary upstream materials are
        available (ready for transit to it) until the downstream or outside demand can be served (ready for transit).
        Besides itself process_lt, it might contain the transit time between this node and its upstream nodes.
        For a root node of current InvNet, it equals to its avg fill time
        For a material node needs serval component to product, it equals to the max transit time of upstream to it
        plus itself process lead time.

        Returns:
            float
        """
        return self._lt

    @property
    def avg_fill_time(self):
        """For a root node (no edges pointed to it) of current InvNet, this attribute represents order fill time of
        outside suppliers. For a non-root node, this value equals to 0.
        This attribute is designed to be able to decouple the analysis of the supply chain from upstream site (or company)
        to downstream site (or company).
        It can be obtained through simulation.

        Returns:
            float
        """
        return self._avg_fill_time

    @property
    def cum_lt(self):
        """The cumulative lead time of this node, represents the shortest duration time from making order from outside
        suppliers until the stock of this node is available.
        The cumulative lead time of current node = process lead time + max cumulative lead time of its predecessors.

        Returns:
            float
        """
        return self._cum_lt

    @property
    def longest_pred(self):
        """Related to the cumulative lead time, it's the set of its predecessors whose cumulative lead time(s)
        are largest.

        Returns:
            set
        """
        return self._longest_pred

    @property
    def holding_cost(self):
        """Unit holding cost rate of this material node, it represents the 
        holding cost for this node to keep one unit material for one time unit.

        Returns:
            float
        """
        return self._holding_cost

    @property
    def material_cost(self):
        """Material cost of this material node.

        Returns:
            float
        """
        return self._material_cost

    @property
    def sale_price(self):
        """Sale price for a product material node.

        Returns:
            float
        """
        return self._sale_price

    @property
    def sale_sla(self):
        """Sale service level agreement for a product material node, the service time
         (the duration from the order placed to order can be served) should not larger than this value.

        Returns:
            float
        """
        return self._sale_sla

    @property
    def material_node_info(self):
        """A dict to contains the attributives' value of this material node.

        Returns:
            dict
        """
        material_node_info = {'node_id': self._node_id, 'company_id': self._company_id, 'site_id': self._site_id,
                              'material_id': self._material_id, 'desc': self._desc, 'node_type': self._node_type,
                              'pred_nodes': self.pred_nodes, 'succ_nodes': self.succ_nodes, 'adj_nodes': self.adj_nodes,
                              'in_degree': self.in_degree, 'out_degree': self.out_degree, 'degree': self.degree,
                              'make_or_buy': self._make_or_buy, 'inv_type': self._inv_type,
                              'replenish_cycle': self._replenish_cycle,
                              'process_lt': self._process_lt, 'former_fill_time': self._avg_fill_time,
                              'lt': self._lt, 'cum_lt': self._cum_lt, 'longest_pred': self._longest_pred,
                              'holding_cost': self._holding_cost, 'material_cost': self._material_cost,
                              'sale_price': self._sale_price, 'sale_sla': self._sale_sla,
                              }
        material_node_info = {i: str(v) for i, v in material_node_info.items()}
        return material_node_info

    def update_inv_type(self, new_inv_type: str):
        """Updating inv type of this material node.

        Args:
            new_inv_type (str)
        """
        self._inv_type = new_inv_type

    def update_replenish_cycle(self, new_replenish_cycle: Union[float, int]):
        """Updating replenish cycle of this material node.

        Args:
            new_replenish_cycle (Union[float, int])
        """
        self._replenish_cycle = new_replenish_cycle

    def update_process_lt(self, new_process_lt: Union[float, int]):
        """Updating process lead time of this material node.

        Args:
            new_process_lt (Union[float, int])
        """
        self._process_lt = new_process_lt

    def update_avg_fill_time(self, new_avg_fill_time: Union[float, int]):
        """Updating former fill time of this material node.

        Args:
            new_avg_fill_time (Union[float, int])
        """
        self._avg_fill_time = new_avg_fill_time

    def update_lt(self, new_lt):
        """Updating lead time of this material node.
        """
        self._lt = new_lt

    def update_cum_lt(self, new_cum_lt: Union[float, int]):
        """Updating cumulative lead time of this material node.

        Args:
            new_cum_lt (Union[float, int])
        """
        self._cum_lt = new_cum_lt

    def update_longest_pred(self, new_longest_pred: set):
        """Updating the longest pred set of this material node.

        Args:
            new_longest_pred (set)
        """
        self._longest_pred = new_longest_pred

    def update_holding_cost(self, new_holding_cost: float):
        """Updating unit holding cost for this material node.

        Args:
            new_holding_cost (float)
        """
        self._holding_cost = new_holding_cost

    def update_material_cost(self, new_material_cost: float):
        """Updating unit material cost for this material node.

        Args:
            new_material_cost (float)
        """
        self._material_cost = new_material_cost

    def update_sale_price(self, new_sale_price: float):
        """Updating sale price for this product material node.

        Args:
            new_sale_price (float)
        """
        self._sale_price = new_sale_price

    def update_sale_sla(self, new_sale_sla: float):
        """Updating sale sla for this product material node.

        Args:
            new_sale_sla (float)
        """
        self._sale_sla = new_sale_sla


class AlterMaterialNode(MaterialNode):
    """
    A class for material node with alternative choices.

    Scenario of alternation:
        1. Multiple suppliers.
        2. A 'MAKE' material can use multiple components to make production.

    The incoming edges are alternative edges. The demand propagation and production can be controlled by
    'decision ratio' parameter.

    Suppose a node has two alternative predecessors(components) to make production.
    The decision ratio of one edge is 0, and the other is 1.
    That means the demand information can only propagate to the edge with 1 decision ratio, and we can not use the
    zero one to make production.
    If these two edges' decision ratio are both 0.5. Then in demand propagation scenario, the demand of node will
    be divided equally between the two components. And both components can be used to make production.

    Args:
        node_id (str): The unique id for this node, default is site_id + '_' + material_id.
        company_id (str): The company id of this material node's owner.
        site_id (str): The site id of this material node's stocking site.
        material_id (str): The material id of this material node.

        desc (Optional[str], optional): The description of this material node. Defaults to None.
        
        make_or_buy (Optional[str], optional): For the owner of this material node, this value equals to 'BUY' means
        this material is buying from outside supplier; if this value is 'MAKE', it means this material is produced by
        this company. Defaults to None.

        holding_cost (Optional[Union[float, int]], optional): Unit holding cost rate of this material node,
        it represents the holding cost for this node to keep one unit material for one time unit. Defaults to None.

        material_cost (Optional[Union[float, int]], optional): Unit material cost of this material node. For 'BUY'
        materials, this can be purchase price. Defaults to None.

        sale_price (Optional[Union[float, int]], optional): Sale price for a product material node.  Defaults to
        None. 
        
        sale_sla (Optional[Union[float, int]], optional): Sale service level agreement for a product material
        node, the service time (the duration from the order placed to order can be served) should not larger than
        this value. Defaults to None.

        alter_time_mode (str, optional): This value controls that use which mode ('MIN', 'MAX', 'EXP') to calculate lead time.
        Defaults to 'MAX'.
    """

    def __init__(self, node_id: str,
                 company_id: str,
                 site_id: str,
                 material_id: str,
                 desc: Optional[str] = None,
                 make_or_buy: Optional[str] = None,
                 holding_cost: Optional[Union[float, int]] = None,
                 material_cost: Optional[Union[float, int]] = None,
                 sale_price: Optional[Union[float, int]] = None,
                 sale_sla: Optional[Union[float, int]] = None,
                 avg_fill_time: Optional[Union[float, int]] = None,
                 alter_time_mode: str = 'MAX'):

        super().__init__(node_id, company_id, site_id, material_id, desc, make_or_buy, holding_cost,
                         material_cost, sale_price, sale_sla, avg_fill_time)
        self._holding_cost = holding_cost
        self._material_cost = material_cost
        self._inv_type = 'NO'
        self._replenish_cycle = 0
        self._process_lt = 0
        self._lt = 0
        self._node_type = 'ALTER_MATERIAL'
        self._alter_time_mode = alter_time_mode

    @property
    def alter_time_mode(self):
        """This value controls that use which mode ('MIN', 'MAX', 'EXP') to calculate lead time.

        Returns:
            str
        """
        return self._alter_time_mode

    @property
    def choices(self):
        """The alternative choices and current decision ratio of this alter node.

        Returns:
            dict -- Example: {pred1: 0.5, pred2: 0.5}
        """
        return {pred: self._incoming_edges_info[(pred, self._node_id)]['decision_ratio'] for pred in self.pred_nodes}

    @property
    def active_choices(self):
        """The active (decision ratio > 0) alternative choices and current decision ratio of this alter node.

        Returns:
            The active choices are the choices that have a decision ratio greater than 0.
            dict -- Example: {pred1: 0.5, pred2: 0.5, pred3: 0}
        """
        return {pred: self._incoming_edges_info[(pred, self._node_id)]['decision_ratio']
                for pred in self.pred_nodes
                if self._incoming_edges_info[(pred, self._node_id)]['decision_ratio'] > 0}

    def update_decision_ratio(self, decision_ratio: Optional[dict] = None):
        """Updating decision ratio on alternative edges. 
        If the input is None, then take average on all incoming edges.

        Args:
            decision_ratio (Optional[dict], optional): The dict for new decision ratio. 
            Example: {pred1, 0.5, pred2: 0.5}. Defaults to None.
        """
        if decision_ratio is None:
            decision_ratio = {(pred, self._node_id): 1 / len(self.pred_nodes) for pred in self._pred_nodes}
        for e_id, ratio in decision_ratio.items():
            self._incoming_edges_info[e_id]['decision_ratio'] = ratio

