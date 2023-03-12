from inv_net.inv_net import InvNet
import numpy as np
import plotly.express as px
import dash
import dash_cytoscape as cyto
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Input, Output


class InvNetVisualization:
    def __init__(self, inv_net: InvNet):
        self.inv_net = inv_net
        self.company_graph = inv_net.company_graph
        self.site_graph = inv_net.site_graph
        self.material_graph = inv_net.material_graph

    def draw(self):
        app = self.build()
        app.run_server(debug=True)

    def build(self):
        all_elements = self.get_all_elements()
        all_companies_list = list(self.company_graph.companies)
        node_type_desc = {}
        for n in self.material_graph.nodes_pool.values():
            if n.node_type not in node_type_desc:
                node_type_desc[n.node_type] = set()
            node_type_desc[n.node_type].add(n.desc)
        node_type_desc_txt = [str(node_type) + ': ' + str(node_descs) for node_type, node_descs in
                              node_type_desc.items()]

        company_nodes_dict = {}
        for n in self.material_graph.nodes_pool.values():
            if n.company_id not in company_nodes_dict:
                company_nodes_dict[n.company_id] = set()
            company_nodes_dict[n.company_id].add(n.node_id)

        col_swatch = px.colors.qualitative.Dark24
        def_stylesheet = [
            {
                "selector": "." + str(i),
                "style": {"background-color": col_swatch[i], "line-color": col_swatch[i]},
            }
            for i in range(len(node_type_desc))
        ]
        def_stylesheet += [
            {
                "selector": "node",
                "style": {"width": "data(node_size)", "height": "data(node_size)"},
            },
            {"selector": "edge", "style": {"width": 1, "curve-style": "bezier"}},
        ]

        navbar = dbc.NavbarSimple(
            children=[
                dbc.NavItem(
                    dbc.NavLink(
                        "Document of InvNet",
                        href="",
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "Source Code",
                        href="",
                    )
                ),
            ],
            brand="InvNet Visualization",
            brand_href="#",
            color="dark",
            dark=True,
        )

        node_types_html = list()
        for topic_html in [
            html.Span([node_type_desc_txt[i]], style={"color": col_swatch[i]})
            for i in range(len(node_type_desc_txt))
        ]:
            node_types_html.append(topic_html)
            node_types_html.append(html.Br())

        body_layout = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Markdown(
                                    f"""
                        -----
                        ##### Basic Information:
                        -----
                        This InvNet contains {len(self.company_graph.companies)} companies, {len(self.site_graph.sites)} 
                        sites and {len(self.material_graph.nodes)} material nodes.
                        """
                                )
                            ],
                            sm=12,
                            md=4,
                        ),
                        dbc.Col(
                            [
                                dcc.Markdown(
                                    """
                        -----
                        ##### Material Node Types:
                        -----
                        """
                                ),
                                html.Div(
                                    node_types_html,
                                    style={
                                        "fontSize": 11,
                                        "height": "100px",
                                        "overflow": "auto",
                                    },
                                ),
                            ],
                            sm=12,
                            md=8,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        cyto.Cytoscape(
                                            id="inv_net_graph",
                                            layout={
                                                'name': 'breadthfirst',
                                                'directed': True,
                                                'padding': 10
                                            },
                                            style={"width": "100%", "height": "400px"},
                                            elements=all_elements,
                                            stylesheet=def_stylesheet,
                                            minZoom=0.06,
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Alert(
                                            id="select_node_data",
                                            children="Click on a node to see its details here",
                                            color="secondary",
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Alert(
                                            id="select_edge_data",
                                            children="Click on a edge to see its details here",
                                            color="secondary",
                                        )
                                    ]
                                ),
                            ],
                            sm=12,
                            md=8,
                        ),
                        dbc.Col(
                            [
                                html.H4(["Companies Selected"]),
                                dcc.Dropdown(
                                    id="companies_selected",
                                    options=[
                                        {
                                            "label": c
                                                     + " ("
                                                     + str(len(c_nodes))
                                                     + " material nodes)",
                                            "value": c,
                                        }
                                        for c, c_nodes in company_nodes_dict.items()
                                    ],
                                    # value=all_companies_list,
                                    multi=True,
                                    style={"width": "100%"},
                                ),
                            ],
                            sm=12,
                            md=4,
                        ),
                    ]
                ),
            ],
            style={"marginTop": 20},
        )

        app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        server = app.server
        app.layout = html.Div([navbar, body_layout])

        @app.callback(
            Output("select_node_data", "children"), [Input("inv_net_graph", "selectedNodeData")]
        )
        def display_node_data(datalist):
            contents = "Click on a node to see its details here"
            if datalist:
                if len(datalist) > 0:
                    data = datalist[-1]
                    contents = []
                    contents.append(html.H5("Node id: " + data['id']))
                    table_header = [
                        html.Thead(html.Tr([html.Th("Info"), html.Th("Value")]))
                    ]
                    row_names = ['company_id', 'site_id', 'material_id', 'desc', 'make_or_buy', 'in_degree',
                                 'out_degree',
                                 'pred_nodes', 'succ_nodes', 'lt', 'process_lt', 'cum_lt', 'holding_cost',
                                 'material_cost',
                                 'inv_type', 'node_type', 'former_fill_time', 'sale_sla']
                    table_body = [html.Tbody([html.Tr([html.Td(row_n), html.Td(data[row_n])]) for row_n in row_names])]
                    contents.append(dbc.Table(table_header + table_body, bordered=True))
            return contents

        @app.callback(
            Output("select_edge_data", "children"), [Input("inv_net_graph", "selectedEdgeData")]
        )
        def display_edge_data(datalist):
            contents = "Click on a edge to see its details here"
            if datalist:
                if len(datalist) > 0:
                    data = datalist[-1]
                    contents = []
                    contents.append(html.H5("Edge id: " + data['id']))
                    table_header = [
                        html.Thead(html.Tr([html.Th("Info"), html.Th("Value")]))
                    ]
                    row_names = ['source', 'target', 'u_site', 'v_site', 'original_qty', 'decision_ratio', 'qty',
                                 'transit_lt', 'desc']
                    table_body = [html.Tbody([html.Tr([html.Td(row_n), html.Td(data[row_n])]) for row_n in row_names])]
                    contents.append(dbc.Table(table_header + table_body, bordered=True))
            return contents

        @app.callback(
            Output("inv_net_graph", "elements"),
            [Input("companies_selected", "value")]
        )
        def show_selected_companies_graph(value):
            if value is None:
                value = all_companies_list
            if value == all_companies_list:
                return all_elements
            else:
                selected_nodes = set()
                for c in value:
                    selected_nodes = selected_nodes | company_nodes_dict[c]
                current_nodes_info = self.get_nodes_info(selected_nodes)
                selected_edges = [(u, v) for u, v in self.material_graph.edges if
                                  u in selected_nodes and v in selected_nodes]
                current_edges_info = self.get_edges_info(selected_edges)
                current_elements = current_nodes_info + current_edges_info
                return current_elements

        return app

    def get_all_elements(self):
        nodes_info = self.get_nodes_info(self.material_graph.nodes)
        edges_info = self.get_edges_info(self.material_graph.edges)
        all_elements = nodes_info + edges_info
        return all_elements

    def get_nodes_info(self, nodes):
        nodes_info = []
        for n_id in nodes:
            n = self.material_graph.nodes_pool[n_id]
            nd = {
                'data': {
                    'id': n_id,
                    'label': n_id,
                    'node_size': int(np.sqrt(1 + n.degree) * 10),
                    'ele_type': 'node'
                },
                'classes': n.node_type,
                'selectable': True,
                'grabbable': False,
            }
            nd['data'].update(n.material_node_info)
            nodes_info.append(nd)
        return nodes_info

    def get_edges_info(self, edges):
        edges_info = []
        for u, v in edges:
            e = self.material_graph.edges_pool[(u, v)]
            ed = {
                'data': {
                    'source': u,
                    'target': v,
                    'id': str((u, v)),
                    'label': str((u, v)),
                    'ele_type': 'edge'
                },
                'selectable': True,
                'grabbable': False,
            }
            ed['data'].update(e.material_edge_full_str_info)
            edges_info.append(ed)
        return edges_info





