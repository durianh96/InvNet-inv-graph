from typing import Union, Optional


class Edge:
    def __init__(self, u: str, v: str, desc: Optional[str] = None):
        self._edge_id = (u, v)
        self._u = u  # source node id
        self._v = v  # target node_id
        self._desc = desc
        self._edge_level = None

    @property
    def edge_id(self):
        return self._edge_id

    @property
    def u(self):
        return self._u

    @property
    def v(self):
        return self._v

    @property
    def desc(self):
        return self._desc

    @property
    def edge_type(self):
        return self._edge_level

    @property
    def edge_level(self):
        return self._edge_level

    def update_desc(self, new_desc):
        self._desc = new_desc


class SupplyEdge(Edge):  # supply edge between companies
    def __init__(self, u: str,  # company_id
                 v: str,
                 desc: Optional[str] = None):
        super().__init__(u, v, desc)
        self._edge_level = 'SUPPLY'


class TransitEdge(Edge):  # transit edge between sites
    def __init__(self, u: str,  # site_id
                 v: str,
                 u_company: str,  # source site's company_id
                 v_company: str,  # target site's company_id
                 transit_lt: Union[float, int] = None,
                 desc: Optional[str] = None):
        super().__init__(u, v, desc)
        self._u_company = u_company
        self._v_company = v_company
        if transit_lt is None:
            self._transit_lt = 0
        else:
            self._transit_lt = transit_lt
        self._edge_level = 'TRANSIT'

    @property
    def u_company(self):
        return self._u_company

    @property
    def v_company(self):
        return self._v_company

    @property
    def transit_lt(self):
        return self._transit_lt

    def update_transit_lt(self, new_transit_lt):
        self._transit_lt = new_transit_lt


class MaterialEdge(Edge):  # edge between materials
    def __init__(self, u: str,
                 v: str,
                 u_site: str,  # source node's site_id
                 v_site: str,  # target node's site_id
                 original_qty: Optional[Union[float, int]] = None,
                 decision_ratio: Optional[Union[float, int]] = None,
                 transit_lt: Optional[Union[float, int]] = None,
                 desc: Optional[str] = None):
        super().__init__(u, v, desc)
        self._u_site = u_site
        self._v_site = v_site

        if original_qty is None:
            self._original_qty = 1
        else:
            self._original_qty = original_qty
        if decision_ratio is None:
            self._decision_ratio = 1
        else:
            self._decision_ratio = decision_ratio
        if transit_lt is None:
            self._transit_lt = 0
        else:
            self._transit_lt = transit_lt

        self._edge_level = 'MATERIAL'

    @property
    def u_site(self):
        return self._u_site

    @property
    def v_site(self):
        return self._v_site

    @property
    def original_qty(self):
        return self._original_qty

    @property
    def decision_ratio(self):
        return self._decision_ratio

    @property
    def qty(self):
        return self._original_qty * self._decision_ratio

    @property
    def transit_lt(self):
        return self._transit_lt

    @property
    def material_edge_info(self):
        info = {'edge_id': self._edge_id, 'u': self._u, 'v': self._v, 'u_site': self._u_site,
                'v_site': self._v_site, 'original_qty': self._original_qty,
                'decision_ratio': self._decision_ratio, 'qty': self.qty, 'transit_lt': self._transit_lt,
                'desc': self._desc}
        info = {i: str(v) for i, v in info.items()}
        return info

    def update_original_qty(self, new_original_qty):
        self._original_qty = new_original_qty

    def update_decision_ratio(self, new_decision_ratio):
        self._decision_ratio = new_decision_ratio

    def update_transit_lt(self, new_transit_lt):
        self._transit_lt = new_transit_lt
