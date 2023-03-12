from inv_net.inv_net import InvNet
from visualization.vis import InvNetVisualization

root_file_dir = 'data/case1'

inv_net = InvNet()
inv_net.get_all_from_file(root_file_dir)

material_graph = inv_net.material_graph


vis = InvNetVisualization(inv_net)
vis.draw()