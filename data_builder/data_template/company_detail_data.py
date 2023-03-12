from typing import Optional
from data_builder.data_template.inventory_data import InventoryData
from data_builder.data_template.order_data import OrderData
from data_builder.data_template.bom_data import BOMData
from data_builder.data_template.buy_material_data import BuyMaterialData
from data_builder.data_template.make_material_data import MakeMaterialData
from data_builder.data_template.site_material_data import SiteMaterialData
from data_builder.data_template.product_data import ProductData


class CompanyDetailData:
    def __init__(self, company_id: str,
                 product_data: Optional[ProductData] = None,
                 buy_material_data: Optional[BuyMaterialData] = None,
                 make_material_data: Optional[MakeMaterialData] = None,
                 bom_data: Optional[BOMData] = None,
                 site_material_data: Optional[SiteMaterialData] = None,
                 order_data: Optional[OrderData] = None,
                 inventory_data: Optional[InventoryData] = None):
        self.company_id = company_id
        if product_data is None:
            self.product_data = ProductData()
        else:
            self.product_data = product_data

        if buy_material_data is None:
            self.buy_material_data = BuyMaterialData()
        else:
            self.buy_material_data = buy_material_data

        if make_material_data is None:
            self.make_material_data = MakeMaterialData()
        else:
            self.make_material_data = make_material_data

        if site_material_data is None:
            self.site_material_data = SiteMaterialData()
        else:
            self.site_material_data = site_material_data

        if bom_data is None:
            self.bom_data = BOMData()
        else:
            self.bom_data = bom_data

        if order_data is None:
            self.order_data = OrderData()
        else:
            self.order_data = order_data

        if inventory_data is None:
            self.inventory_data = InventoryData()
        else:
            self.inventory_data = inventory_data

    def get_all_from_json(self, file_dir):
        self.product_data.get_from_json(file_dir)
        self.buy_material_data.get_from_json(file_dir)
        self.make_material_data.get_from_json(file_dir)
        self.bom_data.get_from_json(file_dir)
        self.site_material_data.get_from_json(file_dir)
        self.order_data.get_from_json(file_dir)
        self.inventory_data.get_from_json(file_dir)

    def get_all_from_csv(self, file_dir):
        self.product_data.get_from_csv(file_dir)
        self.buy_material_data.get_from_csv(file_dir)
        self.make_material_data.get_from_csv(file_dir)
        self.bom_data.get_from_csv(file_dir)
        self.site_material_data.get_from_csv(file_dir)
        self.order_data.get_from_csv(file_dir)
        self.inventory_data.get_from_csv(file_dir)

    def write_all_to_json(self, file_dir):
        self.product_data.write_to_json(file_dir)
        self.buy_material_data.write_to_json(file_dir)
        self.make_material_data.write_to_json(file_dir)
        self.bom_data.write_to_json(file_dir)
        self.site_material_data.write_to_json(file_dir)
        self.order_data.write_to_json(file_dir)
        self.inventory_data.write_to_json(file_dir)

    def write_all_to_csv(self, file_dir):
        self.product_data.write_to_csv(file_dir)
        self.buy_material_data.write_to_csv(file_dir)
        self.make_material_data.write_to_csv(file_dir)
        self.bom_data.write_to_csv(file_dir)
        self.site_material_data.write_to_csv(file_dir)
        self.order_data.write_to_csv(file_dir)
        self.inventory_data.write_to_csv(file_dir)


# class CompanyDetailDataCollector:
#     def __init__(self, company_node: CompanyNode,
#                  product_data: Optional[ProductData] = None,
#                  material_data: Optional[MaterialData] = None,
#                  bom_data: Optional[BOMData] = None,
#                  order_data: Optional[OrderData] = None,
#                  inventory_data: Optional[InventoryData] = None):
#         """
#         This is a detail data collector for one company.
#
#         Args:
#             company_node: The company level node of this company.
#             product_data:
#             material_data:
#             bom_data:
#             order_data:
#             inventory_data:
#         """
#         self.company_node = company_node
#         self.company_id = company_node.node_id
#         if product_data is None:
#             self.product_data = ProductData()
#         else:
#             self.product_data = product_data
#         if material_data is None:
#             self.material_data = MaterialData()
#         else:
#             self.material_data = material_data
#         if bom_data is None:
#             self.bom_data = BOMData()
#         else:
#             self.bom_data = bom_data
#         if order_data is None:
#             self.order_data = OrderData()
#         else:
#             self.order_data = order_data
#         if inventory_data is None:
#             self.inventory_data = InventoryData()
#         else:
#             self.inventory_data = inventory_data

    # def pure_supplier_generating(self, num_products: int,
    #                              intermittent_factor: float,
    #                              order_start_date: str,
    #                              order_end_date: str):
    #     self.product_data = product_generating_randomly(company_node=self.company_node, num_products=num_products)
    #     self.material_data = material_generating_from_product(product_data=self.product_data)
    #     self.order_data = order_generating_from_product(product_data=self.product_data,
    #                                                     intermittent_factor=intermittent_factor,
    #                                                     order_start_date=order_start_date,
    #                                                     order_end_date=order_end_date)
    #
    # def all_generating_from_pred_product(self, site_sort: list,
    #                                      pred_product_data: ProductData,
    #                                      num_materials: int,
    #                                      max_bom_depth: int,
    #                                      num_sink_products: int,
    #                                      num_non_sink_products: int,
    #                                      intermittent_factor: float,
    #                                      order_start_date: str,
    #                                      order_end_date: str,
    #                                      inv_start_date: str,
    #                                      inv_end_date: str):
    #     self.bom_data = bom_generating_from_pred(company_node=self.company_node,
    #                                              site_sort=site_sort,
    #                                              pred_product_data=pred_product_data,
    #                                              num_materials=num_materials,
    #                                              max_bom_depth=max_bom_depth,
    #                                              num_sink_products=num_sink_products)
    #     self.material_data = material_generating_from_pred_product_and_bom(company_node=self.company_node,
    #                                                                        pred_product_data=pred_product_data,
    #                                                                        bom_data=self.bom_data,
    #                                                                        num_non_sink_products=num_non_sink_products)
    #     self.product_data = product_generating_from_material(company_node=self.company_node,
    #                                                          material_data=self.material_data)
    #     self.order_data = order_generating_from_product(product_data=self.product_data,
    #                                                     intermittent_factor=intermittent_factor,
    #                                                     order_start_date=order_start_date,
    #                                                     order_end_date=order_end_date)
    #     self.inventory_data = inventory_generating_from_material(material_data=self.material_data,
    #                                                              inv_start_date=inv_start_date,
    #                                                              inv_end_date=inv_end_date)
