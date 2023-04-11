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
        self._node_level = None
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
    def node_level(self):
        """The node type. Example: 'COMPANY', 'MATERIAL', etc.

        Returns:
            str
        """
        return self._node_level

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

        contained_demand_sites (Optional[set], optional): The site nodes managed by this company which have outside
        demand. Defaults to None.
        contained_manu_sites (Optional[set], optional): The site nodes managed by this company which have manufacturing
        operation. Defaults to None.
    """

    def __init__(self, node_id: str,
                 desc: Optional[str] = None,
                 contained_sites: Optional[set] = None,
                 contained_demand_sites: Optional[set] = None,
                 contained_manu_sites: Optional[set] = None):
        super().__init__(node_id, desc)
        if contained_sites is None:
            self._contained_sites = set()
        else:
            self._contained_sites = contained_sites
        if contained_demand_sites is None:
            self._contained_demand_sites = set()
        else:
            self._contained_demand_sites = contained_demand_sites
        if contained_manu_sites is None:
            self._contained_manu_sites = set()
        else:
            self._contained_manu_sites = contained_manu_sites

        self._node_level = 'COMPANY'

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
    def contained_demand_sites(self):
        """The site nodes managed by this company which have outside demand.

        Returns:
            set
        """
        return self._contained_demand_sites

    @property
    def contained_manu_sites(self):
        """The site nodes managed by this company which have manufacturing operation.

        Returns:
            set
        """
        return self._contained_manu_sites

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

    def update_contained_demand_sites(self, new_contained_demand_sites: set):
        """Updating the contained demand sites set.

        Args:
            new_contained_demand_sites (set)
        """
        self._contained_demand_sites = new_contained_demand_sites

    def update_contained_manu_sites(self, new_contained_manu_sites: set):
        """Updating the contained manu sites.

        Args:
            new_contained_manu_sites (set)
        """
        self._contained_manu_sites = new_contained_manu_sites


class SiteNode(Node):
    """
    The site level base node. A site node can represent a factory, a warehouse, a distribution center, a sales channel, etc.
    A site node might contain serval material nodes.

    Args:
        node_id (str): The unique id for this node, equals to its site id.
        company_id (str): The company id of this site's owner.
        desc (Optional[str], optional): The description of this site node. Defaults to None.
        address (Optional[str], optional): The location of this site node. Defaults to None.
        contained_materials (Optional[set], optional): The materials stored in this site. Defaults to None.
    """

    def __init__(self, node_id: str,
                 company_id: str,
                 desc: Optional[str] = None,
                 address: Optional[str] = None,
                 province: Optional[str] = None,
                 city: Optional[str] = None,
                 district: Optional[str] = None,
                 contained_materials: Optional[set] = None):
        super().__init__(node_id, desc)
        self._company_id = company_id
        self._address = address
        self._province = province
        self._city = city
        self._district = district
        if contained_materials is None:
            self._contained_materials = set()
        else:
            self._contained_materials = contained_materials

        self._node_level = 'SITE'

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
    def address(self):
        """The location of this site node.

        Returns:
            str
        """
        return self._address

    @property
    def province(self):
        return self._province

    @property
    def city(self):
        return self._city

    @property
    def district(self):
        return self._district

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

    def update_contained_materials(self, new_contained_materials: set):
        """Updating the contained material nodes set.

        Args:
            new_contained_materials (set)
        """
        self._contained_materials = new_contained_materials


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

        cycle (Optional[Union[float, int]], optional): The replenish (make order or make production plan)
        cycle time of this material node. Defaults to None.

        process_lt (Optional[Union[float, int]], optional): The process lead time for this node, represents the
        duration from the time when all necessary upstream are in stock (finished transit to it) until the downstream
        or outside demand can be served (ready for transit). It might include the warehouse operation time,
        the manufacturing time, etc. Defaults to None.

        holding_cost (Optional[Union[float, int]], optional): Unit holding cost rate of this material node,
        it represents the holding cost for this node to keep one unit material for one time unit. Defaults to None.

        material_cost (Optional[Union[float, int]], optional): Unit material cost of this material node. For 'BUY'
        materials, this can be purchase price. Defaults to None.

        sale_sla (Optional[Union[float, int]], optional): Sale service level agreement for a product material
        node, the service time (the duration from the order placed to order can be served) should not larger than
        this value. Defaults to None.

    """

    def __init__(self, node_id: str,
                 company_id: str,
                 site_id: str,
                 material_id: str,
                 desc: Optional[str] = None,
                 inv_type: Optional[str] = None,
                 cycle: Optional[Union[float, int]] = None,
                 alter_type: Optional[str] = None,
                 process_lt: Optional[Union[float, int]] = None,
                 holding_cost: Optional[Union[float, int]] = None,
                 material_cost: Optional[Union[float, int]] = None,
                 is_fg: Optional[bool] = None,
                 sale_sla: Optional[Union[float, int]] = None):
        super().__init__(node_id, desc)
        self._company_id = company_id
        self._site_id = site_id
        self._material_id = material_id
        if inv_type is None:
            self._inv_type = 'YES'
        else:
            self._inv_type = inv_type
        if cycle is None:
            self._cycle = 0
        else:
            self._cycle = cycle
        if alter_type is None:
            self._alter_type = 'NO'
        else:
            self._alter_type = alter_type
        if process_lt is None:
            self._process_lt = 0
        else:
            self._process_lt = process_lt
        self._holding_cost = holding_cost
        self._material_cost = material_cost
        if is_fg is None:
            self._is_fg = False
        else:
            self._is_fg = is_fg
        self._sale_sla = sale_sla
        self._node_level = 'MATERIAL'

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
    def inv_type(self):
        """Whether this material node can hold inventory.

        Returns:
            str -- 'YES' or 'NO'
        """
        return self._inv_type

    @property
    def alter_type(self):
        """
        Whether this material node has alternative incoming edges.
        """
        return self._alter_type

    @property
    def cycle(self):
        """The replenishment (make order or make production plan) cycle time of this material node.

        Returns:
            float
        """
        return self._cycle

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
    def is_fg(self):
        return self._is_fg

    @property
    def sale_sla(self):
        return self._sale_sla

    @property
    def material_node_info(self):
        """A dict to contains the attributives' value of this material node.

        Returns:
            dict
        """
        material_node_info = {'node_id': self._node_id, 'company_id': self._company_id, 'site_id': self._site_id,
                              'material_id': self._material_id, 'desc': self._desc, 'inv_type': self._inv_type,
                              'cycle': self._cycle, 'alter_type': self._alter_type, 'process_lt': self._process_lt,
                              'holding_cost': self._holding_cost, 'material_cost': self._material_cost,
                              'is_fg': self._is_fg, 'sale_sla': self._sale_sla,
                              'pred_nodes': self.pred_nodes, 'succ_nodes': self.succ_nodes, 'adj_nodes': self.adj_nodes,
                              'in_degree': self.in_degree, 'out_degree': self.out_degree, 'degree': self.degree}
        material_node_info = {i: str(v) for i, v in material_node_info.items()}
        return material_node_info

    def update_inv_type(self, new_inv_type: str):
        """Updating inv type of this material node.

        Args:
            new_inv_type (str)
        """
        self._inv_type = new_inv_type

    def update_alter_type(self, new_alter_type: str):
        self._alter_type = new_alter_type

    def update_cycle(self, new_cycle: Union[float, int]):
        """Updating replenish cycle of this material node.

        Args:
            new_cycle (Union[float, int])
        """
        self._cycle = new_cycle

    def update_process_lt(self, new_process_lt: Union[float, int]):
        """Updating process lead time of this material node.

        Args:
            new_process_lt (Union[float, int])
        """
        self._process_lt = new_process_lt

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

    def update_is_fg(self, new_is_fg: bool):
        self._is_fg = new_is_fg

    def update_sale_sla(self, new_sale_sla):
        self._sale_sla = new_sale_sla
